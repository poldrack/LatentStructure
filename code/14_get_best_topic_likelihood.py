#!/usr/bin/env python
"""
make scripts to run all topic models
"""
import numpy as N
import os
import matplotlib.pyplot as plt


datatypes=['disorders','cogatlas']
ntopics=N.arange(10,260,10)

mallet_bin='/scratch/01329/poldrack/textmining/mallet-2.0.6/bin/mallet'

for datatype in datatypes:
  datadir='/scratch/01329/poldrack/textmining/paper//%s_8fold/'%datatype
  outputdir='/scratch/01329/poldrack/textmining/paper/topic_modeling/%s/8fold/'%datatype


  ll=N.zeros((8,len(ntopics)))

  for t in range(len(ntopics)):
    for fold in range(8):
      topicdir='%sfold%d_%d'%(outputdir,fold+1,ntopics[t])
      docprobs=N.loadtxt(topicdir+'/docprob.txt')
      ll[fold,t]=N.mean(docprobs)

  meanll=N.mean(ll,0)
  maxll=N.where(meanll==N.max(meanll))
  print maxll, meanll[maxll],ntopics[maxll]
  data=N.vstack((ntopics,meanll))
  N.save(datadir+'%s_8fold_likelihood.npy'%datatype,data)


#plt.plot(ntopics,meanll)
#plt.show()


