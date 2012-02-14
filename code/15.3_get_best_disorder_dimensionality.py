"""
check for repeated topics
"""

import numpy as N

def matrixrank(A,tol=1e-8):
        s = N.linalg.svd(A,compute_uv=0)
        return N.sum(N.where( s>tol, 1, 0 ) )

for ntopics in range(20,60):
    topicdir='/scratch/01329/poldrack/textmining/paper/topic_modeling/disorders/disorders_lda_%d/'%ntopics
    try:
        f=open(topicdir+'/word_weights.txt')
    except:
        print 'could not open %s/word_weights.txt - exiting'%f
    #    return []
    
    
    
    d=f.readlines()
    f.close()
    wordlist=[]
#    ntopics=0
    weightdict={}
    # first get all words
    for x in d:
        topicnum,word,weight=x.split('\t')
        topicnum=int(topicnum)
        weight=float(weight)
#        if (topicnum+1)>ntopics:
#            ntopics=topicnum+1
        wordlist.append(word)
        
    wordlist=list(set(wordlist))
    
    for w in wordlist:
        weightdict[w]=N.zeros(ntopics)
    
    for x in d:
        topicnum,word,weight=x.split('\t')
        topicnum=int(topicnum)
        weight=float(weight)
    
        weightdict[word][topicnum]=weight
        
    # make array
    weightarray=N.zeros((len(wordlist),ntopics))
    for w in range(len(wordlist)):
        for t in range(ntopics):
            weightarray[w,t]=weightdict[wordlist[w]][t]
            
    weightarray_bin=(weightarray>0.01).astype('int')
    
    print ntopics, matrixrank(weightarray_bin), ntopics==matrixrank(weightarray_bin)
