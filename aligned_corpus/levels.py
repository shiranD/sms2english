from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pdb
import pandas
import seaborn as sns

def level(idx_same, idx_sub, samlen):
  #print samlen  
  lsamp = int(samlen/10)+1
  noapp = 16-lsamp
  #print noapp
  bins = np.linspace(10, lsamp*10, lsamp)
  samlevels = np.histogram(idx_same, bins)[0]/10 
  sublevels = np.histogram(idx_sub, bins)[0]/10
  for i in range(noapp):
    samlevels = np.append(samlevels, np.nan)
    sublevels = np.append(sublevels, np.nan)
  #print len(samlevels)
  return samlevels, sublevels


def plot(sames, subs, fold): 
  # plot
  labels = [str(i*10) for i in range(1, 16)]
  subsd = {}
  samsd = {}
  for i in range(0,15):
    subsd[str((1+i)*10)] = subs[:,i]
    samsd[str((1+i)*10)] = sames[:,i]
  fig, axes = plt.subplots(nrows=2, ncols=1)
  df = pandas.DataFrame(subsd)
  df.boxplot(column=labels, ax=axes[0])
  axes[0].set_title('substitutions')
  axes[0].axes.get_xaxis().set_visible(False)
  df2 = pandas.DataFrame(samsd)
  df2.boxplot(column=labels, ax=axes[1])
  axes[1].set_title('identity')

  fig.savefig('imgs/sub_same_rate'+str(fold)+'.pdf')
