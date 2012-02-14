"""
get relation between cogat and disorder loadings
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

pma=importr('PMA')

basedir='/scratch/01329/poldrack/textmining/paper/'
thresh=0.95

if 1==1:
    cogatimg=nib.load(basedir+'topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor_6mm.nii.gz')
    cogatdata=cogatimg.get_data()
    cogatmask=nib.load(basedir+'topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor_6mm_mask.nii.gz')
    disordermask=nib.load(basedir+'topic_modeling/disorders/disorders_lda_29/all_topic_csq_cor_6mm_mask.nii.gz')
    maskdata=disordermask.get_data()*cogatmask.get_data()
    maskvox=N.where(maskdata)
    minvox=N.sum(maskdata)*0.1 # 50% of mask voxels
    cogat_loading_full=cogatdata[maskvox]
    good_concepts=N.sum(cogat_loading_full!=0,0)>minvox # half of the voxels must be present
    good_concept_nums=N.where(good_concepts==1)[0]
    cogat_topics_full=load_topickeys(basedir+'topic_modeling/cogatlas/cogatlas_lda_130/')
    cogat_loading=cogat_loading_full[:,good_concepts]
    cogat_topics=[cogat_topics_full[x] for x in good_concept_nums]

    disorderimg=nib.load(basedir+'topic_modeling/disorders/disorders_lda_29/all_topic_csq_cor_6mm.nii.gz')
    disorderdata=disorderimg.get_data()
    disorder_loading_full=disorderdata[maskvox]
    disorder_topics_full=load_topickeys(basedir+'topic_modeling/disorders/disorders_lda_29/')
    # deal with potential of topics with no loading voxels
    good_disorders=N.sum(disorder_loading_full!=0,0)>minvox # half of the voxels must be present
    good_disorder_nums=N.where(good_disorders==1)[0]
    disorder_loading=disorder_loading_full[:,good_disorders]
    disorder_topics=[disorder_topics_full[x] for x in good_disorder_nums]
    
nccacomps=len(disorder_topics)
print 'found %d good disorder topics and %d good concepts'%(len(disorder_topics),len(cogat_topics))
pos_only=True
if pos_only==True:
    suffix='_nonneg'
else:
    suffix=''
if 1==0:
    cpm=pma.CCA_permute(rpy2.robjects.numpy2ri.numpy2ri(cogat_loading),rpy2.robjects.numpy2ri.numpy2ri(disorder_loading),upos=pos_only,vpos=pos_only,niter=100)

    bestxpenalty=cpm[3][0]
    bestypenalty=cpm[4][0]
    print 'best penalties: %f, %f'%(bestxpenalty,bestypenalty)
    # best penalty was 0.7 for both
    
if 1==0:
    c=pma.CCA(rpy2.robjects.numpy2ri.numpy2ri(cogat_loading),rpy2.robjects.numpy2ri.numpy2ri(disorder_loading),typex='standard',typez='standard',penaltyx=bestxpenalty,penaltyz=bestypenalty,K=nccacomps,niter=1000,upos=pos_only,vpos=pos_only)
    f=open(basedir+'CCA/CCA_solution_6mm%s.pkl'%suffix,'wb')
    pickle.dump(c,f)
    f.close()
else:
    f=open(basedir+'CCA/CCA_solution_6mm%s.pkl'%suffix,'rb')
    c=pickle.load(f)
    f.close()
    
u=N.array(c[0])
v=N.array(c[1])
cors=N.array(c[15])
N.savetxt(basedir+'CCA/uvecs.txt',u)
N.savetxt(basedir+'CCA/vvecs.txt',v)
N.savetxt(basedir+'CCA/cors.txt',cors)

if 1==1:
  topiclist=open(basedir+'CCA/topic_list_6mm%s.txt'%suffix,'w')
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

# make component images

if 1==0:
  img=nib.load(basedir+'topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor_6mm.nii.gz')
  imgdata=img.get_data()
  imgdata=imgdata[:,:,:,good_concept_nums]
  maskimg=nib.load(basedir+'topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor_6mm_mask.nii.gz')
  posmax=N.zeros(nccacomps)
  negmax=N.zeros(nccacomps)
  posthresh=N.zeros(nccacomps)
  negthresh=N.zeros(nccacomps)
  for comp in range(nccacomps):
    pvaldata=N.zeros((30,36,30))
    corrdata=N.zeros((30,36,30))
    for x in range(30):
        for y in range(36):
            for z in range(30):
                if N.sum(imgdata[x,y,z])>0:
                    rval,pval=scipy.stats.stats.pearsonr(imgdata[x,y,z,:],u[:,comp])
                    #compdata[x,y,z]=N.corrcoef(imgdata[x,y,z,:],u[:,comp])[0,1]
                    pvaldata[x,y,z]=pval
                    corrdata[x,y,z]=rval
    i=nib.Nifti1Image(corrdata,maskimg.get_affine())
    i.to_filename(basedir+'CCA_corr/cca%s_comp%03d_6mm.nii.gz'%(suffix,comp))
    i=nib.Nifti1Image(pvaldata,maskimg.get_affine())
    i.to_filename(basedir+'CCA_corr/cca%s_comp%03d_6mm_pval.nii.gz'%(suffix,comp))
    p=Popen('fdr -i %sCCA_corr/cca%s_comp%03d_6mm_pval.nii.gz -q %f'%(basedir,suffix,comp,1-thresh),stdout=PIPE,shell=True)
    fdr_thresh=float(p.communicate()[0].split('\n')[1])
    above_thresh=pvaldata<fdr_thresh
    if N.sum(above_thresh)>0:
        corrdata_thresh=N.zeros((30,36,30))
        corrdata_thresh[above_thresh]=corrdata[above_thresh]
        i=nib.Nifti1Image(corrdata_thresh,maskimg.get_affine())
        i.to_filename(basedir+'CCA_corr/cca%s_comp%03d_6mm_thresh.nii.gz'%(suffix,comp))
        posthresh[comp]=N.min(corrdata_thresh[corrdata_thresh>0])
        negthresh[comp]=N.max(corrdata_thresh[corrdata_thresh<0])
        posmax[comp]=N.max(corrdata_thresh[corrdata_thresh>0])
        negmax[comp]=N.min(corrdata_thresh[corrdata_thresh<0])
   
# now make disorder component images
if 1==0:
  img=nib.load(basedir+'topic_modeling/disorders/disorders_lda_60/all_topic_csq_cor_6mm.nii.gz')
  imgdata=img.get_data()
  imgdata=imgdata[:,:,:,good_disorder_nums]
  maskimg=nib.load(basedir+'topic_modeling/disorders/disorders_lda_60/all_topic_csq_cor_6mm_mask.nii.gz')
  posmax_dis=N.zeros(nccacomps)
  negmax_dis=N.zeros(nccacomps)
  posthresh_dis=N.zeros(nccacomps)
  negthresh_dis=N.zeros(nccacomps)
  for comp in range(nccacomps):
    pvaldata=N.zeros((30,36,30))
    corrdata=N.zeros((30,36,30))
    for x in range(30):
        for y in range(36):
            for z in range(30):
                if N.sum(imgdata[x,y,z])>0:
                    rval,pval=scipy.stats.stats.pearsonr(imgdata[x,y,z,:],v[:,comp])
                    #compdata[x,y,z]=N.corrcoef(imgdata[x,y,z,:],u[:,comp])[0,1]
                    pvaldata[x,y,z]=pval
                    corrdata[x,y,z]=rval
    i=nib.Nifti1Image(corrdata,maskimg.get_affine())
    i.to_filename(basedir+'CCA_corr/cca%s_disorders_comp%03d_6mm.nii.gz'%(suffix,comp))
    i=nib.Nifti1Image(pvaldata,maskimg.get_affine())
    i.to_filename(basedir+'CCA_corr/cca%s_disorders_comp%03d_6mm_pval.nii.gz'%(suffix,comp))
    p=Popen('fdr -i %sCCA_corr/cca%s_disorders_comp%03d_6mm_pval.nii.gz -q %f'%(basedir,suffix,comp,1-thresh),stdout=PIPE,shell=True)
    fdr_thresh=float(p.communicate()[0].split('\n')[1])
    above_thresh=pvaldata<fdr_thresh
    if N.sum(above_thresh)>0:
        corrdata_thresh=N.zeros((30,36,30))
        corrdata_thresh[above_thresh]=corrdata[above_thresh]
        i=nib.Nifti1Image(corrdata_thresh,maskimg.get_affine())
        i.to_filename(basedir+'CCA_corr/cca%s_disorders_comp%03d_6mm_thresh.nii.gz'%(suffix,comp))
        posthresh_dis[comp]=N.min(corrdata_thresh[corrdata_thresh>0])
        negthresh_dis[comp]=N.max(corrdata_thresh[corrdata_thresh<0])
        posmax_dis[comp]=N.max(corrdata_thresh[corrdata_thresh>0])
        negmax_dis[comp]=N.min(corrdata_thresh[corrdata_thresh<0])
   

# make slice images
if 1==0:
  for comp in range(nccacomps):
    if posthresh[comp]>0:
      # first take back to 3mm space
      
      cmd='/work/01329/poldrack/software_lonestar/fsl/bin/flirt -in /scratch/01329/poldrack/textmining/paper/CCA_corr/cca%s_comp%03d_6mm_thresh.nii.gz -applyxfm -init /work/01329/poldrack/software_lonestar/fsl/etc/flirtsch/ident.mat -out %sCCA_corr/cca%s_comp%03d_thresh.nii.gz -paddingsize 0.0 -interp trilinear -ref /scratch/01329/poldrack/textmining/paper/data_preparation/all_peakimages.nii.gz'%(suffix,comp,basedir,suffix,comp)
      print cmd
      run_shell_cmd(cmd)
      cmd='overlay 1 0 /work/01329/poldrack/software_lonestar/atlases/MNI152lin_3mm.nii.gz -a %sCCA_corr/cca%s_comp%03d_thresh.nii.gz %f %f %sCCA_corr/cca%s_comp%03d_thresh.nii.gz %f %f cbar.png ysb %sCCA_corr/cca%s_comp%03d_rend'%(basedir,suffix,comp,posthresh[comp],posmax[comp],basedir,suffix,comp,negthresh[comp],negmax[comp],basedir,suffix,comp)
      print cmd
      run_shell_cmd(cmd)
      cmd='slicer %sCCA_corr/cca%s_comp%03d_rend.nii.gz -u -S 2 750 %sCCA_corr/cca%s_comp%03d_slices.png'%(basedir,suffix,comp,basedir,suffix,comp)
      print cmd
      run_shell_cmd(cmd)

# make slice images for disorders
if 1==0:
  for comp in range(nccacomps):
    if posthresh_dis[comp]>0:
      # first take back to 3mm space
      
      cmd='/work/01329/poldrack/software_lonestar/fsl/bin/flirt -in /scratch/01329/poldrack/textmining/paper/CCA_corr/cca%s_disorders_comp%03d_6mm_thresh.nii.gz -applyxfm -init /work/01329/poldrack/software_lonestar/fsl/etc/flirtsch/ident.mat -out %sCCA_corr/cca%s_disorders_comp%03d_thresh.nii.gz -paddingsize 0.0 -interp trilinear -ref /scratch/01329/poldrack/textmining/paper/data_preparation/all_peakimages.nii.gz'%(suffix,comp,basedir,suffix,comp)
      print cmd
      run_shell_cmd(cmd)
      cmd='overlay 1 0 /work/01329/poldrack/software_lonestar/atlases/MNI152lin_3mm.nii.gz -a %sCCA_corr/cca%s_disorders_comp%03d_thresh.nii.gz %f %f %sCCA_corr/cca%s_disorders_comp%03d_thresh.nii.gz %f %f cbar.png ysb %sCCA_corr/cca%s_disorders_comp%03d_rend'%(basedir,suffix,comp,posthresh_dis[comp],posmax_dis[comp],basedir,suffix,comp,negthresh_dis[comp],negmax_dis[comp],basedir,suffix,comp)
      print cmd
      run_shell_cmd(cmd)
      cmd='slicer %sCCA_corr/cca%s_disorders_comp%03d_rend.nii.gz -u -S 2 750 %sCCA_corr/cca%s_disorders_comp%03d_slices.png'%(basedir,suffix,comp,basedir,suffix,comp)
      print cmd
      run_shell_cmd(cmd)

