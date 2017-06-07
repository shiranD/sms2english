# -*- coding: utf-8 -*-
"""
Created on JUNE 6 2017

@author: Shiran Dudy
"""

from __future__ import division
from random import randint
import numpy as np

def compare(y_hat, y_test):
  # provide a sample (sentence) level comparison
  sample = randint(0, 100)
  for th, tr in zip(y_hat[sample][:20], y_test[sample][:20]):
    print "argmax is ",np.argmax(th)
    print "argmax real is ",np.argmax(tr)
    print "max is ", np.max(th)
    print "max real is ", np.max(tr)

def accuracy(y_hat, y_test):
  # provide an accuracy report
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
