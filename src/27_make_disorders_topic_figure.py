"""
make disorders topic figure
"""

import numpy as N
import matplotlib.pyplot as plt
from load_topicdata import *
import matplotlib.image as mpimg

topics_to_show=[8,10,7, 24,25,14,11,12]
nwords_to_show=5
ntopics=len(topics_to_show)
image_padding=5
text_padding=200
line_padding=20

topicdir='/Users/poldrack/data2/neurosynth_data_analysis/topic_models/disorders/disorders_lda_29/'
keys=load_topickeys(topicdir)
loadingdata=N.genfromtxt(topicdir+'loadingdata.txt')
ndocs=N.sum(loadingdata>0,0)

plt.figure(num=None, figsize=(18,int(144.0/(text_padding+720)*18.0*len(topics_to_show))), dpi=72)

plt.axis('off')
pngfiles=[topicdir+'slice_images/topic%03d_slices.png'%i for i in topics_to_show]
imgshape = [144,720,3] # get image size
fullimg=N.ones((imgshape[0]*ntopics+image_padding*ntopics, imgshape[1]+text_padding,imgshape[2]))
plt.imshow(fullimg)

start=0
end=imgshape[0]
for t in range(len(topics_to_show)):
    topic=topics_to_show[t]
    im = mpimg.imread(pngfiles[t])[0:imgshape[0],:,:]
    fullimg[start:end,text_padding:,:]=im
    plt.text(10,start+30,'Topic %d (%d documents):'%(topic,ndocs[topic]))
    if len(keys[topic])<nwords_to_show:
        nwords=len(keys[topic])
    else:
        nwords=nwords_to_show
    for w in range(nwords):
        label='%s'%(keys[topic][w])
        plt.text(10,start+30+(w+1)*line_padding,label)
    
    start+=imgshape[0]+image_padding
    end+=imgshape[0]+image_padding

plt.savefig(topicdir+"disorders_fig.eps",format='eps')