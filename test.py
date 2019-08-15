import os
from tqdm import tqdm
import tensorflow as tf
import numpy as np
from nltk.translate.bleu_score import corpus_bleu,sentence_bleu
from SequenceToSequence import Seq2Seq
import DataProcessing
from CONFIG import BASE_MODEL_DIR, MODEL_NAME, data_config, model_config
import pickle
def getSampleQA(validateset):
    q = []
    r = []
    for dialogue in validateset:
        q.append(dialogue[0])
        r.append(list(dialogue[1]))
    return q,r
def test():
        trainset, validateset, _, du = pickle.load(open('dataset.pkl', 'rb'))
        q,r = getSampleQA(trainset)
        save_path = os.path.join(BASE_MODEL_DIR, MODEL_NAME)
        batch_size = 1
        steps = int(len(list(validateset)) / batch_size) + 1
        tf.reset_default_graph()
        model = Seq2Seq(batch_size=batch_size,
                        encoder_vocab_size=du.vocab_size,
                        decoder_vocab_size=du.vocab_size,
                        mode='decode',
                        **model_config)
        # 创建session的时候允许显存增长
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        with tf.Session(config=config) as sess:
            init = tf.global_variables_initializer()
            sess.run(init)
            model.load(sess, save_path)
            bar = tqdm(range(steps), total=steps,
                       desc='time:0')
            cGram1 = []
            cGram2 = []
            cGram3 = []
            cGram4 = []
            for time in bar:
                x, xl,references = du.next_batch_test(batch_size, list(q),list(r),time)
                # print(xl[0:2])
                # print(x[0:2])
                pred = model.predict(
                    sess, np.array(x),
                    np.array(xl)
                )
                result = du.transform_indexs(pred[0])
                # print(result)
                # print("references {}".format(references))
                candidates = list(result)
                # print("candidate:{}".format(candidates))
                cGram1.append(sentence_bleu(references, candidates, weights=(1, 0, 0, 0)))
                cGram2.append(sentence_bleu(references, candidates, weights=(0.5, 0.5, 0, 0)))
                cGram3.append(sentence_bleu(references, candidates, weights=(0.33, 0.33, 0.33, 0)))
                cGram4.append(sentence_bleu(references, candidates, weights=(0.25, 0.25, 0.25, 0.25)))
                bar.set_description('time={}'.format(time))
            print('Cumulative 1-gram: %f' % np.mean(cGram1))
            print('Cumulative 2-gram: %f' % np.mean(cGram2))
            print('Cumulative 3-gram: %f' % np.mean(cGram3))
            print('Cumulative 4-gram: %f' % np.mean(cGram4))

if __name__ == '__main__':
    test()