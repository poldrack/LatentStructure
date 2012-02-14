#!/usr/bin/env python
"""
create text files with cog atlas terms from each paper in neurosynth
"""

import numpy as N
import pickle

basedir='/scratch/01329/poldrack/textmining/paper/'

if 1==1:
    loadingdata=N.load(basedir+'cogatlas/cogat_neurosynth_loadings.npy').T
    f=open(basedir+'cogatlas/cogat_concepts.pkl','rb')
    concepts=pickle.load(f)
    f.close()
    concepts=[x.replace(')','').replace('(','') for x in concepts]
    
outputdir=basedir+'/fulltext_cogatlas/'

for x in range(loadingdata.shape[0]):
    if N.sum(loadingdata[x,:]>0):
        print '%d'%x
        f=open(outputdir+'cogatlas_%05d.txt'%int(x+1),'w')
        for c in range(loadingdata.shape[1]):
            if loadingdata[x,c]>0:
                for i in range(loadingdata[x,c].astype('int')):
                    f.write(concepts[c].replace(' ','_')+' ')
        f.close()

        
