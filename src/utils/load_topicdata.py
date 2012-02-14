#!/usr/bin/env python
""" load_topicdata.py - loads topic loading file from mallet output

"""

import numpy as N

def load_topicdata(topicdir):
   try:
       f=open(topicdir+'/doc_topics.txt')
   except:
       print 'could not open %s/doc_topics.txt - exiting'%topicdir
       return []

   d=f.readlines()
   f.close()
   ndocs=len(d)-1
   ntopics=(len(d[1].strip().split(' '))-2)/2
   loadingdata=N.zeros((ndocs,ntopics))
   docnames=[]
   for doc in range(ndocs):
       docdata=d[doc+1].strip().split(' ')
       docnames.append(docdata[1])
       for t in range(ntopics):
           loadingdata[doc,int(docdata[t*2+2])]=float(docdata[t*2+3])

   return loadingdata, docnames

def load_topickeys(topicdir):
   try:
       f=open(topicdir+'/topic_keys.txt')
   except:
       print 'could not open %s/doc_topics.txt - exiting'%topicdir
       return []

   d=f.readlines()
   f.close()
   ndocs=len(d)
   keys={}
   for x in d:
      keys[int(x.split()[0])]=x.strip().split()[2:]
   return keys

