#!/usr/bin/env python
"""
create chi-squared maps for each topic
filter out voxels that are not active in at least 2.5% of papers
"""

from __future__ import division
import numpy as N
#from mvpa.suite import *
import subprocess
import sys
import chisq
import pickle
import nibabel as nib


if len(sys.argv)<3:
    print 'USAGE: python mk_chisq_maps_filter.py <datatype> <topicnum>'
 #   sys.exit(0)
    topic=1
    datatype='cogatlas_lda_100'
else:
    topic=sys.argv[2]
    datatype=sys.argv[1]


datadir='/scratch/01329/poldrack/textmining/paper/topic_modeling/%s/%s/'%(datatype.split('_')[0],datatype)

loadingdata=N.loadtxt(datadir+'loadingdata.txt')
ndocs,ntopics=loadingdata.shape


voxthresh=N.round(ndocs*0.025)

# load image data
basedir='/scratch/01329/poldrack/textmining/paper/'
maskimg=basedir+'data_preparation/all_peakimages_mask.nii.gz'

m=nib.load(maskimg)
maskdata=m.get_data()
maskvox=N.where(maskdata)
maskzeros=N.where(maskdata==0)

pklfile=open(basedir+'data_preparation/pickled_data/voxdata.pkl','rb')
voxdata=pickle.load(pklfile)
pklfile.close()


thr=0
nvox=voxdata.shape[1]


pvalmap=N.zeros(nvox)
maskmat=N.zeros(nvox)
cormap=N.zeros(nvox)


for x in range(nvox):
        xdat=(loadingdata[:,topic]>thr).astype(int)
        ydat=voxdata[:,x].astype(int)
         # filter by minimum number of papers activating voxel
        (pval,foo,e)=chisq.chisqtest(xdat,ydat)
        if N.min(e)>=5:
                pvalmap[x]=pval
                cormap[x]=N.corrcoef(xdat,ydat)[0,1]
        else:
                pvalmap[x]=1
                cormap[x]=0
             
# save data files
# save data files
pv=N.zeros(maskdata.shape)
pv[maskvox]=pvalmap
pv[maskzeros]=0

i=nib.Nifti1Image(pv,m.get_affine())
i.to_filename(datadir+"chisquare_maps/topic_csq_%003d.nii.gz"%int(topic))

pv=1-pv
pv[maskzeros]=0
i=nib.Nifti1Image(pv,m.get_affine())
i.to_filename(datadir+"chisquare_maps/topic_csq_1-p_%003d.nii.gz"%int(topic))

cm=N.zeros(maskdata.shape)
cm[maskvox]=cormap
cm[maskzeros]=0

i=nib.Nifti1Image(cm,m.get_affine())
i.to_filename(datadir+"chisquare_maps/topic_csq_cor_%003d.nii.gz"%int(topic))


