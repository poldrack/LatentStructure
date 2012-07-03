"""
make histograms of docs/topic and topics/doc
"""

import numpy as N
import matplotlib.pyplot as plt
import os

loadingdatafile='/corral-repl/utexas/poldracklab/data/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/loadingdata.txt'

figdir='/corral-repl/utexas/poldracklab/data/textmining/paper/doc_topic_hist'


ld=N.loadtxt(loadingdatafile)

ld_bin=(ld>0)*1

fontsize=20

plt.clf()
plt.hist(N.sum(ld_bin,0),bins=30)
plt.ylabel('Count of topics',fontsize=fontsize)
plt.xlabel('Number of documents',fontsize=fontsize)
plt.savefig(os.path.join(figdir,'cog_ndocs_hist.pdf'))

plt.clf()
plt.hist(N.sum(ld_bin,1),bins=22)
plt.ylabel('Count of documents',fontsize=fontsize)
plt.xlabel('Number of topics',fontsize=fontsize)
plt.savefig(os.path.join(figdir,'cog_ntopics_hist.pdf'))

loadingdatafile='/corral-repl/utexas/poldracklab/data/textmining/paper/topic_modeling/disorders/disorders_lda_29/loadingdata.txt'

figdir='/corral-repl/utexas/poldracklab/data/textmining/paper/doc_topic_hist'


ld=N.loadtxt(loadingdatafile)

ld_bin=(ld>0)*1

plt.clf()
plt.hist(N.sum(ld_bin,0),bins=30)
plt.ylabel('Count of topics',fontsize=fontsize)
plt.xlabel('Number of documents',fontsize=fontsize)
plt.savefig(os.path.join(figdir,'dis_ndocs_hist.pdf'))

plt.clf()
plt.hist(N.sum(ld_bin,1),bins=22)
plt.ylabel('Count of documents',fontsize=fontsize)
plt.xlabel('Number of topics',fontsize=fontsize)
plt.savefig(os.path.join(figdir,'dis_ntopics_hist.pdf'))
