#!/usr/bin/env python
from subprocess import *
ntopics=130
thresh=0.99
topicthresh="0.05"  # this is the threshold for topic loading in mk_chisq_maps.py
anatimg='/work/01329/poldrack/software_lonestar/atlases/MNI152lin_3mm.nii.gz'
datadir='/corral-repl/utexas/poldracklab/data/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_%d/'%ntopics

for x in range(ntopics):
    p=Popen('fdr -i %s/chisquare_maps/topic_csq_%03d.nii.gz -q %f'%(datadir,x,1-thresh),stdout=PIPE,shell=True)
    fdr_thresh=1-float(p.communicate()[0].split('\n')[1])

    cmd='fslmaths %s/chisquare_maps/topic_csq_1-p_%03d.nii.gz -thr %f -bin -mul %s/chisquare_maps/topic_csq_cor_%03d.nii.gz %s/chisquare_maps/topic_csq_cor_fdrthresh_%03d.nii.gz'%(datadir,x,fdr_thresh,datadir,x,datadir,x)
    print cmd

    cmd='fslmaths %s/chisquare_maps/topic_csq_cor_fdrthresh_%03d.nii.gz -mul -1 %s/chisquare_maps/topic_csq_cor_fdrthresh__negmul_%03d.nii.gz'%(datadir,x,datadir,x)
    print cmd
    
    cmd='overlay 1 0 %s -a %s/chisquare_maps/topic_csq_cor_fdrthresh_%03d.nii.gz 0.001 0.1 %s/chisquare_maps/topic_csq_cor_fdrthresh__negmul_%03d.nii.gz 0.001 0.1 cbar.png ysb %s/slice_images/topic%03d_rendered_threshcor'%(anatimg,datadir,x,datadir,x,datadir,x)
    print cmd
    
    cmd='slicer %s/slice_images/topic%03d_rendered_threshcor -u -S 2 750 %s/slice_images/topic%03d_slices_threshcor.png'%(datadir,x,datadir,x)
    print cmd
    #pngappend cope3_slices.png + cbar.png cope3_slices.png
