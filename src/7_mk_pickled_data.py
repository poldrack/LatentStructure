import nibabel as nib
import pickle
import numpy as N

basedir='/scratch/01329/poldrack/textmining/paper/data_preparation/'
maskimg=basedir+'all_peakimages_mask.nii.gz'
ndocs=5809


mask=nib.load(maskimg)
maskdata=mask.get_data()
maskvox=maskdata>0
nvox=N.sum(maskvox)

voxdata=N.zeros((ndocs,nvox),dtype='bool')

# loop through all images
for x in range(1,ndocs+1):
    
    d=nib.load(basedir+'peakimages/paper%05d.nii.gz'%x)
    data=d.get_data()
    print "loaded %d"%x
    voxdata[x-1,:]=data[maskvox]
    
output=open(basedir+'pickled_data/voxdata.pkl','wb')
pickle.dump(voxdata,output)
output.close()
