# -*- coding: utf-8 -*-
"""
Created on MAY 18 2017

@author: Shiran Dudy
"""
from __future__ import division
import numpy as np
from keras.models import model_from_json
from model import seq2seqC
from keras.preprocessing import sequence
import pdb
from sklearn.utils import shuffle
import pickle

"""this code aims to learn how to 
reconstruct EN from SMS on aligned corpus"""
pad = 12
max_sample_length = 151 # num of max char. in a sentence(including </s>)
model = seq2seqC(max_length=max_sample_length+pad, vocab_size=64, embedding_size=100, units=61)
path = TBD

for i in range(5):
  X_train = []
  y_train = []
  for fold in range(5):
    filename = path+str(fold)
    file = open(filename,"r")
    the_dict = pickle.load(file)
    if fold==i:
      X_test = the_dict["X"]
      y_test = the_dict["y"]
    else:
      X_train.extend(the_dict["X"])
      y_train.extend(the_dict["y"])
  X_train = np.array(X_train)
  X_test = np.array(X_test)
  y_train = np.array(y_train)
  y_test = np.array(y_test)
  X_train = sequence.pad_sequences(X_train, padding="post", maxlen=max_sample_length+pad)
  X_test = sequence.pad_sequences(X_test, padding="post", maxlen=max_sample_length+pad)
  y_train = sequence.pad_sequences(y_train, padding="post", maxlen=max_sample_length)
  y_test = sequence.pad_sequences(y_test, padding="post", maxlen=max_sample_length)
  
  # train
  for j in range(3):
    model.fit(X_train, y_train, epochs=10, batch_size=50)
    X_train, y_train = shuffle(X_train, y_train, random_state=1)
    # test after every epoch
    y_hat = model.predict(X_test)
    for th, tr in zip(y_hat[30][:20], y_test[30][:20]):
      print "argmax is ",np.argmax(th)
      print "argmax real is ",np.argmax(tr)
      print "max is ", np.max(th)
      print "max real is ", np.max(tr)
    cor=0
    res=0
    otok=0
    token=0
    sent=0
    for y_h_sam,y_t_sam in zip(y_hat, y_test):
    # counts num corr of sentences
      flags=1
      for y1_tok,y2_tok in zip(y_h_sam,y_t_sam):
        # get rid of zeros
        y1_z = (y1_tok>0.5).astype('int32')
        if y1_z.all()==y2_tok.all() and sum(y2_tok)==0:
          continue
        if np.argmax(y1_tok)==np.argmax(y2_tok):
          cor+=1
          res+=1
        else:
          flags=0
          res+=1
      if flags:
        sent+=1
    print "correct chars accuracy", cor, cor/res*100
    print "completely correct segments's accuracy", sent, sent/len(y_test)*100

  # serialize model to JSON at the end of training
  fol = "../attn/"
  model_json = model.to_json()
  with open(fol+"model_"+str(i)+".json", "w") as json_file:
    json_file.write(model_json)
  # serialize weights to HDF5
  model.save_weights(fol+"../attn/model_"+str(i)+".h5")
  print "Saved model to disk"
  

