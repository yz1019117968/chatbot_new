import os
import tensorflow as tf
import numpy as np
from flask import Flask,request
from SequenceToSequence import Seq2Seq
import DataProcessing
from CONFIG import BASE_MODEL_DIR, MODEL_NAME, data_config, model_config



def chatbot_api(infos):
    du = DataProcessing.DataUnit(**data_config)
    save_path = os.path.join(BASE_MODEL_DIR, MODEL_NAME)
    batch_size = 1
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
        while True:
            q = infos
            if q is None or q.strip() == '':
                return "请输入聊天信息"
                continue
            q = q.strip()
            indexs = du.transform_sentence(q)
            print("index: {}".format(indexs))
            x = np.asarray(indexs).reshape((1, -1))
            print(x)
            xl = np.asarray(len(indexs)).reshape((1,))
            pred = model.predict(
                sess, np.array(x),
                np.array(xl)
            )
            result = du.transform_indexs(pred[0])
            return result




app = Flask(__name__)
@app.route('/api/chatbot', methods=['get'])
def ask_chatbot():
    infos = request.args['infos']
    print("info:{}".format(infos))
    result = chatbot_api(infos)
    return result

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)


