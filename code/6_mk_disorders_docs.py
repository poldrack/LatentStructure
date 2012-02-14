#!/usr/bin/env python
"""
create text files with cog atlas terms from each paper in neurosynth

# rerun on 2/2/2012 to use NIF dataset

"""

import numpy as N
import pickle

basedir='/scratch/01329/poldrack/textmining/paper/'
if 1==1:
    loadingdata=N.load(basedir+'NIF-Disorders/disorders_neurosynth_loadings.npy').T
    f=open(basedir+'NIF-Disorders/disorders_concepts.pkl','rb')
    concepts=pickle.load(f)
    f.close()
    concepts=[x.replace(')','').replace('(','') for x in concepts]
    
outputdir=basedir+'fulltext_disorders/'

good_docs=N.zeros(loadingdata.shape[0])

for x in range(loadingdata.shape[0]):
    if N.sum(loadingdata[x,:]>0):
        good_docs[x]=1
        print '%d'%x
        f=open(outputdir+'disorders_%05d.txt'%int(x+1),'w')
        for c in range(loadingdata.shape[1]):
            if loadingdata[x,c]>0:
                for i in range(loadingdata[x,c].astype('int')):
                    f.write(concepts[c].replace(' ','_').replace("\\'",'').replace('-','_')+' ')
        f.close()

        
#N.save('disorders_good_docs.npy',good_docs)
