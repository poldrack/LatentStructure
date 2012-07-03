
import numpy as N
from load_topicdata import *
import scipy.stats.stats
#from ballotbox.ballot import BallotBox
#from ballotbox.singlewinner.preferential import KemenyYoungVoting
#from ballotbox.singlewinner.preferential import BordaVoting

#bb = BallotBox(method=KemenyYoungVoting)

topicdir='/scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/'

testdatadir='/scratch/01329/poldrack/textmining/paper/task_annotation/'

#testdatafiles=['testdata_pain_3mm_wholebrain_corrs.npy','testdata_wm_3mm_wholebrain_corrs.npy','testdata_emotion_3mm_wholebrain_corrs.npy']
testdatafiles=['pain_3mm_tstat1_wholebrain_corrs.npy','wm_3mm_tstat1_wholebrain_corrs.npy','emotion_3mm_tstat1_wholebrain_corrs.npy']

keys=load_topickeys(topicdir)

for ip in testdatafiles:

    inputfile=testdatadir+ip
    loading=N.load(inputfile)

    idxcount=N.zeros(loading.shape[1])
    wincount=N.zeros(loading.shape[1])
    idxcorr=N.zeros(loading.shape)

    for subject in range(loading.shape[0]):
        sorted_idx=N.argsort(loading[subject,:])
        wincount[sorted_idx[-1]]+=1
        votedict={}
        for i in range(loading.shape[1]):
            votedict[str(sorted_idx[i])]=loading.shape[1]-i
            idxcount[sorted_idx[i]]+=i
            idxcorr[subject,sorted_idx[i]]+=loading[subject,sorted_idx[i]]
        
    tstats_p=N.zeros(loading.shape[1])
    tstats=N.zeros(loading.shape[1])
    for i in range(loading.shape[1]):
        tstats[i],tstats_p[i]=scipy.stats.ttest_1samp(idxcorr[:,i],0)
    mean_idxcorr=N.mean(idxcorr,0)
    sorted_idxcount=N.argsort(mean_idxcorr)[::-1]
    print ""
    print inputfile
    for i in range(5):

            print '%d (%0.3f, %0.3f, %d wins, p=%0.6f): %s'%(sorted_idxcount[i],mean_idxcorr[sorted_idxcount[i]],idxcount[sorted_idxcount[i]],wincount[sorted_idxcount[i]],tstats_p[sorted_idxcount[i]],' '.join(keys[sorted_idxcount[i]][0:10]))

