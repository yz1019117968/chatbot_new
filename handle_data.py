import os

import tensorflow as tf
import numpy as np
from flask import Flask,request
from SequenceToSequence import Seq2Seq
import DataProcessing
from CONFIG import BASE_MODEL_DIR, MODEL_NAME, data_config, model_config
import random
import pickle


def handle_data():
    du = DataProcessing.DataUnit(**data_config)
    fullset = np.array(du.data)
    index_test = np.random.choice(fullset.shape[0], 13503, replace=False)
    testset = fullset[index_test]
    index_full = np.arange(fullset.shape[0])
    index_rest = np.delete(index_full,index_test)
    restset = fullset[index_rest]
    index_validate = np.random.choice(restset.shape[0], 13503, replace=False)
    validateset = restset[index_validate]
    index_rest_full = np.arange(restset.shape[0])
    index_rest_rest = np.delete(index_rest_full,index_validate)
    trainset = restset[index_rest_rest]
    # in_corpus_data = random.sample(list(trainset),13503)
    # print(in_corpus_data)
    print(testset.shape)
    print(validateset.shape)
    print(trainset.shape)
    pickle.dump(
        (trainset, validateset,testset,du),
        open('dataset.pkl', 'wb')
    )


if __name__ == '__main__':
    handle_data()
