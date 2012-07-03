"""
make plots of empirical likelhood as function of ntopics
"""

import numpy as N
import matplotlib.pyplot as plt
import os

modeltype='disorders' # or 'disorders'
nfolds=8
tvals=N.arange(10,251,10)
ntvals=len(tvals)

basedir='/corral-repl/utexas/poldracklab/data/textmining/paper/topic_modeling/%s/8fold'%modeltype
figdir='/corral-repl/utexas/poldracklab/data/textmining/paper/emplik_figs'

emplik=N.zeros((ntvals,nfolds))

for t in range(ntvals):
    for f in range(nfolds):
        d=N.loadtxt(os.path.join(basedir,'fold%d_%d/prob.txt'%(f+1,tvals[t])))
        emplik[t,f]=d
            
meanlik=N.mean(emplik,1)
datarange=N.max(meanlik)-N.min(meanlik)
axislims=[N.min(tvals)-5,N.max(tvals)+5,N.min(meanlik)-datarange*0.05,N.max(meanlik)+datarange*0.05]
plt.clf()
plt.plot(tvals,meanlik)
plt.axis(axislims)

plt.savefig(os.path.join(figdir,'%s_emplik.pdf'%modeltype))
