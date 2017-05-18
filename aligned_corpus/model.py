# -*- coding: utf-8 -*-
"""
Created on MAY 18 2017

@author: Shiran Dudy
"""
from keras.models import Model
from keras.layers import Conv1D, Dense, Dropout, Input
from keras.layers.embeddings import Embedding

def seq2seqC(max_length=150, vocab_size=60, embedding_size=10, units=66):

    _input = Input(shape=(max_length,), dtype='int32')

    # get the embedding layer
    embedded = Embedding(
            input_dim=vocab_size,
            output_dim=embedding_size,
            input_length=max_length
        )(_input)

    # 1 d conv layers    
    conv = Conv1D(filters=units+30, kernel_size=6, strides=1, activation='relu', padding='valid')(embedded)
    x = Conv1D(units, 8, activation='softmax', padding='valid')(conv)

    # form the model
    seq2seqConv = Model(_input, x)
    seq2seqConv.compile(optimizer='adam', loss='categorical_crossentropy')

    print seq2seqConv.summary()
    return seq2seqConv
