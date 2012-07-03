# load topic data and make images

import numpy as N
import re

basedir='/corral-repl/utexas/poldracklab/data/textmining/paper/topic_modeling/cogatlas/8fold/'

for ntopics in range(10,251,10):
  datadir=basedir+'fold1_%d'%ntopics
  docloadingsfile=datadir+'/doc_topics.txt'
  
  
  f=open(docloadingsfile,'r')
  d=[]
  order=[]
  for l in f.readlines():
    if l[0] != '#':
      d.append(l)
      order.append(int(l.split(' ')[1].split('/')[8].split('_')[1].replace('.txt',''))-1)
  #ndocs=len(d)
  f.close()
  
  ndocs=5809
  ntopics=(len(d[0].split(' '))-4)/2
  
  docloadings=N.zeros((ndocs,ntopics))
  
  #docorderfile=datadir+'doc_order.txt'
  #f=open(docorderfile,'r')
  #order=f.readlines()
  #f.close()
  
  print 'detected %d topics over %d documents'%(ntopics,ndocs)
  
  ctr=0
  for dl in d:
      sd=dl.split(' ')
  #    articlenum=int(sd[0])
      articlenum=int(order[ctr])
      ctr=ctr+1
      for t in range(2,len(sd)-2,2):
              docloadings[articlenum,int(sd[t])]=float(sd[t+1])
  
  
  
  
  f=open(datadir+'loadingdata.txt','w')
  
  for i in range(ndocs):
      #f.write('%s\t'%nameindex[i])
  
      for t in range(ntopics):
          f.write('%0.8f\t'%docloadings[i,t])
  
      f.write('\n')
  
  f.close()




#    for t in range(ntopics):
#        docloadings[int(sd[0]),int(dl.split(' ')

