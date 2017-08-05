# -*- coding: utf-8 -*-
"""
Created on MAY 18 2017

@author: Shiran Dudy
"""
from __future__ import division
import sys
from keras.models import model_from_json
from keras.preprocessing import sequence
import pickle
import numpy as np

# settings
folds = 5
max_sample_length = 151
pad  = 12
path2folds = sys.argv[1]+"/fold_" 
path2model = sys.argv[2]+"/model_"
path2dict = sys.argv[1]+"/decoding"
path2eval = sys.argv[3]

# load dicts from decoding file
pkl_dict = open(path2dict, 'rb')
the_dict = pickle.load(pkl_dict)
num2sms = the_dict["num2sms"] 
num2en = the_dict["num2en"]

for fold in xrange(folds):
  m_path = path2model+str(fold)+".json"
  w_path = path2model+str(fold)+".h5"
  # load model
  json_file = open(m_path, "r")
  loaded_model_json = json_file.read()
  json_file.close()
  loaded_model = model_from_json(loaded_model_json)
  # load weights
  loaded_model.load_weights(w_path)
  loaded_model.compile(loss='categorical_crossentropy', optimizer='adam')
  # load X_test and y_test
  fold_file = path2folds+str(fold)
  file = open(fold_file, "r")
  the_dict = pickle.load(file)
  X_test_a = np.array(the_dict["X"])
  y_test = np.array(the_dict["y"])
  X_test = sequence.pad_sequences(X_test_a, padding="post", maxlen=max_sample_length+pad) 
  y_test = sequence.pad_sequences(y_test, padding="post",maxlen=max_sample_length)
  # predict English
  y_hat = loaded_model.predict(X_test)
  # analyze results
  all_same_a = 0
  all_subs_a = 0
  idx_same_a = 0
  idx_subs_a = 0
  x = 0
  f = open(path2eval+"/qual_out_"+str(fold),"wb")
  for sent_pred, sent_real, sent_x in zip(y_hat, y_test, X_test_a):
    # for each token in y
    sym_pred = []
    sym_real = []
    corr_idx = []
    # compare EN_pred to EN_real symbols
    for j, (y_pred, y_real) in enumerate(zip(sent_pred, sent_real)):
      y1_z = (y_pred>0.5).astype('int32')
      if y1_z.all()==y_real.all() and sum(y_real)==0:
        continue
      prd = np.argmax(y_pred)
      rl = np.argmax(y_real)
      # list correct indecies (ignore 0)
      if prd == rl:
        corr_idx.append(j)
      # convert to ys symbols
      sym_pred.append(num2en[prd])
      sym_real.append(num2en[rl])

    # convert X to symbols with dicts
    sym_sms = []
    idx_same = []
    idx_subs = []
    # how many pred has in common with SMS (since the corpus is aligned)
    for x in sent_x[int(pad/2):]: # disregard padding
      sym_sms.append(num2sms[x])
      
    # count same and subs correct predictions
    for idx in corr_idx:
      try:
        sym_sms[idx]
        if sym_sms[idx]==sym_pred[idx]:
          idx_same.append(idx)
        else:
          idx_subs.append(idx)
      except:
        idx_subs.append(idx)
   
    # count overall same and subs
    


    all_same = []
    all_subs = []
    for idx, (rl, sms) in enumerate(zip(sym_real, sym_sms)):
      if rl==sms:
        all_same.append(idx)
      else:
        all_subs.append(idx)
    # if one is longer than the other - the rest are subs
    if len(sym_real)>len(sym_sms) or len(sym_real)<len(sym_sms):
      for i in range(idx+1,abs(len(sym_real)-len(sym_sms))):
        idx_subs.append(i)

    all_same_a+=len(all_same)
    all_subs_a+=len(all_subs)
    idx_same_a+=len(idx_same)
    idx_subs_a+=len(idx_subs)
    
    # prepare a display
    mrk1_st = "\033[91m\033[1m"
    mrk1_ed = "\033[0;0m"
    for idx in idx_same:
      sym = sym_pred[idx]
      new_sym = mrk1_st+sym+mrk1_ed
      sym_pred[idx] = new_sym
      sym = sym_sms[idx]
      new_sym = mrk1_st+sym+mrk1_ed
      sym_sms[idx] = new_sym

    mrk2_st = "\033[92m\033[1m" 
    mrk2_ed = "\033[0;0m"
    for idx in idx_subs:
      try:
        sym = sym_pred[idx]
        new_sym = mrk2_st+sym+mrk2_ed
      except:
        pass
      try:
        sym_pred[idx] = new_sym
        sym = sym_sms[idx]
      except:
        pass
      try:
        new_sym = mrk2_st+sym+mrk2_ed
        sym_sms[idx] = new_sym
      except:
        pass

    if 1: # write a qualitative representation of results
      f.write("SMS: {0}\n".format("".join(sym_sms)))
      f.write("PRD: {0}\n".format("".join(sym_pred)))
      f.write("REL: {0}\n".format("".join(sym_real)))
      f.write("\n")
  f.close()
  if 1: # print quantitative evaluation
    f = open(path2eval+"/quan_out_"+str(fold),"wb")
    f.write("\n\033[4mfold {0}\033[0;0m".format(fold))
    f.write("\n")
    f.write("{0:40} {1}".format("total identity symbols", all_same_a))
    f.write("{0:40} {1}".format("correctly predicted identity symbols", idx_same_a))
    f.write("{0:40} {1:.3f}".format("fold correct identity prediction", idx_same_a/all_same_a*100))
    f.write("\n")
    f.write("{0:40} {1}".format("total subs symbols", all_subs_a))
    f.write("{0:40} {1}".format("correctly predicted subs symbols", idx_subs_a))
    f.write("{0:40} {1:.3f}".format("fold correct substitution prediction", idx_subs_a/all_subs_a*100))
    f.write("\n")
    f.write("{0:40} {1:.3f}".format("fold accuracy", (idx_same_a+idx_subs_a)/(all_same_a+all_subs_a)*100))

    print "\n\033[4mfold {0}\033[0;0m".format(fold)
    print "\n"
    print "{0:40} {1}".format("total identity symbols", all_same_a)
    print "{0:40} {1}".format("correctly predicted identity symbols", idx_same_a)
    print "{0:40} {1:.3f}".format("fold correct identity prediction", idx_same_a/all_same_a*100)
    print "\n"
    print "{0:40} {1}".format("total subs symbols", all_subs_a)
    print "{0:40} {1}".format("correctly predicted subs symbols", idx_subs_a)
    print "{0:40} {1:.3f}".format("fold correct substitution prediction", idx_subs_a/all_subs_a*100)
    print "\n"
    print "{0:40} {1:.3f}".format("fold accuracy", (idx_same_a+idx_subs_a)/(all_same_a+all_subs_a)*100)
