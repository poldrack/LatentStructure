"""
get histograms of # of docs for each filtered paper
- for response to PLOS reviews
"""

import numpy as N
import matplotlib.pyplot as plt
import os

cog_fulltextdir='/corral-repl/utexas/poldracklab/data/textmining/paper/fulltext_cogatlas'
dis_fulltextdir='/corral-repl/utexas/poldracklab/data/textmining/paper/fulltext_disorders'

if 0:

    cogfiles=os.listdir(cog_fulltextdir)
    cog_nwords=N.zeros(len(cogfiles))
    ctr=0
    for f in cogfiles:
        i=open(os.path.join(cog_fulltextdir,f))
        l=i.readlines()
        i.close()
        cog_nwords[ctr]=len(l[0].strip().split(' '))
        ctr+=1

    disfiles=os.listdir(dis_fulltextdir)
    dis_nwords=N.zeros(len(disfiles))
    ctr=0
    for f in disfiles:
        i=open(os.path.join(dis_fulltextdir,f))
        l=i.readlines()
        i.close()
        dis_nwords[ctr]=len(l[0].strip().split(' '))
        ctr+=1

# make figures
print 'median # words:'
print 'cogatlas: %0.1f'%N.median(cog_nwords)
print 'disorders: %0.1f'%N.median(dis_nwords)
