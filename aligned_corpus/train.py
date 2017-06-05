# -*- coding: utf-8 -*-
"""
Created on MAY 18 2017

@author: Shiran Dudy
"""
import sys
import numpy as np
from keras.models import model_from_json
from model import seq2seqC
from keras.preprocessing import sequence
from sklearn.utils import shuffle
import pickle
from analyze import compare, accuracy

"""this code learns how to 
reconstruct EN from SMS on aligned corpus"""
path = sys.argv[1]+"/"
models = sys.argv[2]+"/"
uniq_smsf = sys.argv[3]
uniq_enf = sys.argv[4]
uniq_sms = int(open(uniq_smsf, "r").readlines()[0].strip())
uniq_en = int(open(uniq_enf, "r").readlines()[0].strip())

pad = 12
max_sample_length = 151 # num of max char. in a sentence(including </s>)
model = seq2seqC(max_length=max_sample_length+pad, vocab_size=uniq_sms+1, embedding_size=100, units=uniq_en+1)

for i in range(5):
  X_train = []
  y_train = []
  for fold in range(5):
    filename = path+"fold_"+str(fold)
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
    compare(y_hat, y_test)
    accuracy(y_hat, y_test)
  # serialize model to JSON at the end of training
  model_json = model.to_json()
  with open(models+"model_"+str(i)+".json", "w") as json_file:
    json_file.write(model_json)
  # serialize weights to HDF5
  model.save_weights(models+"model_"+str(i)+".h5")
  print "Saved model to disk"
  

