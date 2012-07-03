"""
annotate topics for a dataset
using whole-brain data

"""

from load_topicdata import *
import numpy as N
import nibabel as nib

# set up variables
topicdir='/scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/'
topicdatafile=topicdir+'all_topic_csq_cor.nii.gz'

testdatadir='/scratch/01329/poldrack/textmining/paper/task_annotation/'

#testdatafiles=['testdata_pain_3mm.nii.gz','testdata_wm_3mm.nii.gz','testdata_emotion_3mm.nii.gz']
testdatafiles=['pain_3mm_tstat1.nii.gz','wm_3mm_tstat1.nii.gz','emotion_3mm_tstat1.nii.gz']

maskfile=testdatadir+'testdata_mask_3mm.nii.gz'
mask=nib.load(maskfile)
maskdata=mask.get_data()
maskvox=N.where(maskdata>0)

# load topic data
keys=load_topickeys(topicdir)

# annotate each data file
if 1==1:
    topicimg=nib.load(topicdatafile)
    topic_alldata=topicimg.get_data()
    ntopics=130
    topicdata=N.zeros((ntopics,len(maskvox[0])))
    for t in range(ntopics):
        tmp=topic_alldata[:,:,:,t]
        topicdata[t,:]=tmp[maskvox]

    topicdata[N.where(N.isnan(topicdata))]=0
    
for f in testdatafiles:
    df=testdatadir+f

    testdataimg=nib.load(df)
    testdata_full=testdataimg.get_data()

    try:
        ndp=testdata_full.shape[3]
    except:
        ndp=1
        
    topiccorrs=N.zeros((ndp,ntopics))
    for dp in range(ndp):
        if ndp>1:
            testdata=testdata_full[:,:,:,dp]
        else:
            testdata=testdata_full
        testdata=testdata[maskvox]
        for t in range(ntopics):
            topiccorrs[dp,t]=N.corrcoef(testdata,topicdata[t,:])[0,1]

    
    N.save(df.replace(".nii.gz",'_wholebrain_corrs.npy'),topiccorrs)

        

