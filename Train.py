import DataProcessing
import os
import tensorflow as tf
from SequenceToSequence import Seq2Seq
from tqdm import tqdm
import numpy as np
from CONFIG import BASE_MODEL_DIR, MODEL_NAME, data_config, model_config, \
    n_epoch, batch_size, keep_prob
import pickle
from matplotlib import pyplot as plt
# 是否在原有模型的基础上继续训练
continue_train = False


def train():
    """
    训练模型
    :return:
    """
    du = DataProcessing.DataUnit(**data_config)
    save_path = os.path.join(BASE_MODEL_DIR, MODEL_NAME)
    trainset,_,_,_ = pickle.load(open('dataset.pkl', 'rb'))
    steps = int(len(list(trainset)) / batch_size) + 1
    print(trainset.shape)
    # 创建session的时候设置显存根据需要动态申请
    tf.reset_default_graph()
    config = tf.ConfigProto()
    # config.gpu_options.per_process_gpu_memory_fraction = 0.9
    config.gpu_options.allow_growth = True

    with tf.Graph().as_default():
        with tf.Session(config=config) as sess:
            # 定义模型
            model = Seq2Seq(batch_size=batch_size,
                            encoder_vocab_size=du.vocab_size,
                            decoder_vocab_size=du.vocab_size,
                            mode='train',
                            **model_config)

            init = tf.global_variables_initializer()
            sess.run(init)
            if continue_train:
                model.load(sess, save_path)
            loss_list = []

            for epoch in range(1, n_epoch + 1):
                costs = []
                bar = tqdm(range(steps), total=steps,
                           desc='epoch {}, loss=0.000000'.format(epoch))
                for time in bar:
                    x, xl, y, yl = du.next_batch(batch_size,list(trainset))
                    max_len = np.max(yl)
                    y = y[:, 0:max_len]
                    cost, lr = model.train(sess, x, xl, y, yl, keep_prob)
                    costs.append(cost)
                    if epoch == 1 and time == 0:
                        loss_list.append(np.mean(costs))
                    if time == steps-1:
                        loss_list.append(np.mean(costs))
                    bar.set_description('epoch {} loss={:.6f} lr={:.6f}'.format(epoch, np.mean(costs), lr))
            epoch_list =list(range(0,n_epoch+1))
            plt.xlabel('Epoch Number')
            plt.ylabel('Loss Value')
            plt.plot(epoch_list,loss_list)
            plt.show()
            model.save(sess, save_path=save_path)


if __name__ == '__main__':
    train()
