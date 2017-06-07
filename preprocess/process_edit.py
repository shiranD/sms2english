#! /usr/bin/env python

import sys
import os
import re

def make_corpus(ifile, dirr):

  sms = 1
  en = 2
  alg = 3

  new_sms = dirr+'/sms'
  new_en = dirr+'/en'
  f1 = open(new_sms, "w")
  f2 = open(new_en, "w")

  for i, line in enumerate(ifile):
    if i%3==0:
      line = re.sub(r'|', r'', line)
      line = line.replace("|","")
      line = line.replace(" ","")
    
      f1.write(line)
    if i%3==1:
      line = re.sub(r'|', r'', line)
      line = line.replace("|","")
      line = line.replace(" ","")
    
      f2.write(line)
    
if __name__ == '__main__':
  folder = sys.argv[1]
  make_corpus(sys.stdin, folder)
