# -*- coding: utf-8 -*-
"""
Created on MAY 18 2017

@author: Shiran Dudy
"""
import random
import pickle
import numpy as np
import sys

def dict_it(symbols):
    # make encoding decoding dicts for symbols
    uniq = list(set(sorted(symbols)))
    # dict symbols
    lang2num = {}
    num2lang = {}
    uniq.append("</s>")
    for i, key in enumerate(uniq):
        lang2num[key] = i+1
        num2lang[i+1] = key
        
    return lang2num, num2lang

def ltr2digit(sample, dic):
    # convert symbol to digit
    size = len(dic)+1
    new_vec = []
    for i in range(6):# pre pad for convolution 
      new_vec.append(0)
    for token in sample:
        value = dic[token]
        new_vec.append(value)
    return new_vec

def encodeHot(sample, dic):
    # convert symbol to hot rep
    size = len(dic)+1
    new_vec = []
    for token in sample:
        value = dic[token]
        tok = np.zeros(size)
        tok[value] = 1
        new_vec.append(tok)
    return new_vec

def chunks(l, n):
    # Yield successive n-sized chunks from l.
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

location = sys.argv[1]        
db = ["/sms", "/en"]
orig_file1 = location + db[0]
orig_file2 = location + db[1]

num_lines = sum(1 for line in open(orig_file1))
array = range(num_lines)
random.shuffle(array)
fold = 5
shard = int(round((num_lines) / fold))

# open both files to two lists
f = open(orig_file1)
all_sym = []
lines_o1 = []
for line in f.readlines():
    line = line.lower()
    line = line.replace("\n", "")
    all_sym.extend(list(line)) 
    lines_o1.append(line)
uniq = list(set(all_sym))
uniq.append('</s>')

sms2num, num2sms = dict_it(all_sym)

f = open(orig_file2)
all_sym = []
lines_o2 = []
for line in f.readlines():
    line = line.lower()
    line = line.replace("\n", "")
    all_sym.extend(list(line))
    lines_o2.append(line)

en2num, num2en = dict_it(all_sym)
uniq2 = list(set(all_sym))
uniq2.append('</s>')

print "There are", len(uniq), "SMS symbols"
print "There are", len(uniq2), "English symbols"

the_dict = {"en2num": en2num, "sms2num": sms2num, "num2en": num2en, "num2sms": num2sms}
with open(location+"/decoding", 'wb') as handle:
    pickle.dump(the_dict, handle)

# insert indecies to form arrays
file1 = []
file2 = []

for arr in chunks(array, shard):
    l1 = [lines_o1[x] for x in arr]
    l2 = [lines_o2[x] for x in arr]
    file1.append(l1)
    file2.append(l2)

# generate 5 mutually exclusive pickled test sets
for i, (ls1, ls2) in enumerate(zip(file1,file2)):
    lst1 = []
    lst2 = []
    # write test file
    for line1, line2 in zip(ls1, ls2):
        # encode input
        line1 = list(line1.lower())
        line1.append("</s>")
        l1 = ltr2digit(line1, sms2num)# list of lists
        line2 = list(line2.lower())
        line2.append("</s>")
        l2 = encodeHot(line2, en2num)
        lst1.append(l1)
        lst2.append(l2)
    the_dict = {"X": lst1, "y": lst2}
    with open(location+"/fold_"+str(i), 'wb') as handle:
	    pickle.dump(the_dict, handle)

