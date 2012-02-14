#!/usr/bin/env python
"""
split data into folds for topic model evaluation
"""

import sklearn.cross_validation
import os
import numpy as N

doclist=os.listdir('/scratch/01329/poldrack/textmining/paper/fulltext_cogatlas')

ndocs=len(doclist)

basedir='/scratch/01329/poldrack/textmining/paper/'
outdir=basedir+'cogatlas_8fold/'
origdir=basedir+'fulltext_cogatlas/'
cv=sklearn.cross_validation.KFold(ndocs,8)  # use 8-fold CV
randidx=range(ndocs)
N.random.shuffle(randidx)

foldcounter=1
cmdfile=open('8.1_mk_cogatlas_8fold_data.sh','w')
for train,test in cv:
    randtrain=N.where(train[randidx])[0]
    randtest=N.where(test[randidx])[0]
    try:
        os.mkdir('%sfold%d_train'%(outdir,foldcounter))
    except:
        pass
    
    try:
        os.mkdir('%sfold%d_test'%(outdir,foldcounter))
    except:
        pass
   
    for traindoc in randtrain:
        cmd='cp %s%s %sfold%d_train/'%(origdir,doclist[traindoc],outdir,foldcounter)
        cmdfile.write(cmd+'\n')
   
    for testdoc in randtest:
        cmd='cp %s%s %sfold%d_test/'%(origdir,doclist[testdoc],outdir,foldcounter)

        cmdfile.write(cmd+'\n')
      
    foldcounter+=1
    
cmdfile.close()
