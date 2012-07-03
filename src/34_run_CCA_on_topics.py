"""
get relation between cogat and disorder loadings
using topic loading directly rather than voxel data
- use only positive u and v vectors
"""

import numpy as N
from load_topicdata import *
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
import nibabel as nib
import scipy.stats
from run_shell_cmd import *
import pickle
from subprocess import *
import os

pma=importr('PMA')

basedir='/corral-repl/utexas/poldracklab/data/textmining/paper/'
outdir=os.path.join(basedir,'CCA_topic/')

thresh=0.95

if 1==1:

    cogat_topics=load_topickeys(basedir+'topic_modeling/cogatlas/cogatlas_lda_130/')
    cogat_loading=N.loadtxt(basedir+'topic_modeling/cogatlas/cogatlas_lda_130/loadingdata.txt')


    disorder_topics=load_topickeys(basedir+'topic_modeling/disorders/disorders_lda_29/')
    disorder_loading=N.loadtxt(basedir+'topic_modeling/disorders/disorders_lda_29/loadingdata.txt')
    
    
nccacomps=len(disorder_topics)
print 'found %d good disorder topics and %d good concepts'%(len(disorder_topics),len(cogat_topics))
pos_only=True
if pos_only==True:
    suffix='_nonneg'
else:
    suffix=''
if 1==1:
    cpm=pma.CCA_permute(rpy2.robjects.numpy2ri.numpy2ri(cogat_loading),rpy2.robjects.numpy2ri.numpy2ri(disorder_loading),upos=pos_only,vpos=pos_only,niter=100)

    bestxpenalty=cpm[3][0]
    bestypenalty=cpm[4][0]
    print 'best penalties: %f, %f'%(bestxpenalty,bestypenalty)
    # best penalty was 0.7 for both
    
if 1==1:
    c=pma.CCA(rpy2.robjects.numpy2ri.numpy2ri(cogat_loading),rpy2.robjects.numpy2ri.numpy2ri(disorder_loading),typex='standard',typez='standard',penaltyx=bestxpenalty,penaltyz=bestypenalty,K=nccacomps,niter=1000,upos=pos_only,vpos=pos_only)
    f=open(outdir+'CCA_solution_6mm%s.pkl'%suffix,'wb')
    pickle.dump(c,f)
    f.close()
else:
    f=open(outdir+'CCA_solution_6mm%s.pkl'%suffix,'rb')
    c=pickle.load(f)
    f.close()
    
u=N.array(c[0])
v=N.array(c[1])
cors=N.array(c[15])
N.savetxt(outdir+'uvecs.txt',u)
N.savetxt(outdir+'vvecs.txt',v)
N.savetxt(outdir+'cors.txt',cors)

if 1==1:
  topiclist=open(outdir+'topic_list_6mm%s.txt'%suffix,'w')
  for x in range(nccacomps):
    topiclist.write('component %d (%f)\n'%(x,cors[x]))
    topiclist.write('nonzero cognitive topics:\n')
    u_argsort=N.argsort(N.abs(u[:,x]))[::-1]
    v_argsort=N.argsort(N.abs(v[:,x]))[::-1]
    for i in u_argsort[0:nccacomps]:
        if u[i,x]>0:
            topiclist.write('%d (%f): %s\n'%(i,u[i,x],' '.join(cogat_topics[i][0:4])))

    topiclist.write('nonzero disease topics:\n')
    for i in v_argsort[0:nccacomps]:
        if v[i,x]>0:
            topiclist.write('%d (%f): %s\n'%(i,v[i,x],' '.join(disorder_topics[i][0:4])))
                      
    topiclist.write('\n')

  topiclist.close()



