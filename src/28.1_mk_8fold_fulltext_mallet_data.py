#!/usr/bin/env python
"""
make data for 8-fold topic modeling test
"""
import numpy as N

mallet_bin='/scratch/01329/poldrack/textmining/mallet-2.0.6/bin/mallet'
basedir='/scratch/01329/poldrack/textmining/paper/fulltext_8fold/'

for fold in range(1,9):
    traindir=basedir+'fold%d_train'%fold
    testdir=basedir+'fold%d_test'%fold
    cmd="%s import-dir --input %s --output %s/fold%d_train_data.mallet --keep-sequence --remove-stopwords --stoplist-file /scratch/01329/poldrack/textmining/paper/stopwords/all_stopwords.txt"%(mallet_bin,traindir,basedir,fold)
    print cmd
    cmd="%s import-dir --input %s --output %s/fold%d_test_data.mallet --keep-sequence --remove-stopwords --stoplist-file /scratch/01329/poldrack/textmining/paper/stopwords/all_stopwords.txt"%(mallet_bin,testdir,basedir,fold)
    print cmd
