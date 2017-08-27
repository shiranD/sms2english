#! /usr/bin/env python

import sys
import os
import re

def op_align(operations, inp, out):
  "align according to input length given the edits"
  op_list = []
  ins = ""
  for i, op in enumerate(operations):

    if op == 'n' or op=='d':
      if ins:
        act = '{0}({1})'.format('i', ins)
        ins = ""
      else:
        act = op
      op_list.append(act)

    if op == 's':
      if ins:
        act = '{0}({1}){2}({3})'.format('i', ins, 's', out[i])
        ins = ""
      else:
        act = '{0}({1})'.format('s', out[i])
      op_list.append(act)
    if op == 'i':
      ins+=out[i]
    
  # is finished with ins
  if ins:
    act = '{0}{1}({2})'.format(act,'i',ins)   
    op_list[-1] = act
  return op_list
  
def make_corpus(ifile, dirr):

  new_sms = dirr+'/sms'
  new_en = dirr+'/en'
  fop = dirr+'/op'
  f1 = open(new_sms, "w")
  f2 = open(new_en, "w")
  f3 = open(fop, "w")

  for i, line in enumerate(ifile):

    if i%3==0:
      sms_or = line
      line = re.sub(r'|', r'', line)
      line = line.replace("|","")
      sms = line.replace(" ","")
      # filter and write line
      line_sms = sms.replace("#", "")    

    if i%3==1:
      en_or = line
      line = re.sub(r'|', r'', line)
      line = line.replace("|","")
      en = line.replace(" ","")

    if i%3==2:
      line = re.sub(r'|', r'', line)
      line = line.replace("|", "")
      op = line.replace(" ", "")
      #f3.write(op)
      # process line to fit sms length and operations
      nop = op_align(op, sms, en)
      if len(nop)+1!=len(line_sms):
        #print len(nop), len(line_sms)
        #print line_sms
        #print nop
        continue
      else:
        f1.write(line_sms)
        f2.write(" ".join(nop)+"\n")
        f3.write(sms_or)
        f3.write(en_or) 
        new_op = "| "+" | ".join(nop)+" |"
        f3.write(new_op)      
        f3.write("\n")
      # print operations
    
if __name__ == '__main__':
  folder = sys.argv[1]
  make_corpus(sys.stdin, folder)
