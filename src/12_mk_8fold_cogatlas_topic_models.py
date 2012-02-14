#!/usr/bin/env python
"""
make scripts to run all topic models
"""
import numpy as N
import os

mallet_bin='/scratch/01329/poldrack/textmining/mallet-2.0.6/bin/mallet'
datadir='/scratch/01329/poldrack/textmining/paper/cogatlas_8fold/'
outputdir='/scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/8fold/'

ntopics=N.arange(10,260,10)

for t in ntopics:
  for fold in range(1,11):
    outfile=open('nfold_scripts/run_mallet_cogatlas_fold%d_%d.sh'%(fold,t),'w')
    a=50.0/t
    topicdir='%sfold%d_%d'%(outputdir,fold,t)
    try:
        os.mkdir(topicdir)
    except:
        pass
    cmd=mallet_bin+' train-topics --input %s/fold%d_train_data.mallet --num-topics %d --num-top-words 31 --output-topic-keys %s/topic_keys.txt --output-doc-topics %s/doc_topics.txt --topic-word-weights-file %s/word_weights.txt --word-topic-counts-file %s/word_topic_counts.txt --num-iterations 5000 --output-model %s/saved_model.mallet --evaluator-filename %s/evaluator.mallet --alpha %f --beta 0.1'%(datadir,fold,t,topicdir,topicdir,topicdir,topicdir,topicdir,topicdir,a)
    outfile.write(cmd+'\n')
    cmd=mallet_bin+' evaluate-topics --evaluator %s/evaluator.mallet --input %s/fold%d_test_data.mallet --output-prob %s/prob.txt --output-doc-probs %s/docprob.txt'%(topicdir,datadir,fold,topicdir,topicdir)   
    outfile.write(cmd+'\n')
    outfile.close()
