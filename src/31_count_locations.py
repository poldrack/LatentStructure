"""
count # of locations reported across all papers
- for response to PLOS reviews
"""

import numpy as N
from mniconvert import *
import nibabel as nib
import os

peakfiledir='/corral-repl/utexas/poldracklab/data/textmining/paper/data_preparation/peakfiles'

nfiles=5809

if 0:
    data=N.zeros((60,72,60))
    focictr=0
    for f in range(nfiles):
        d=N.loadtxt(os.path.join(peakfiledir,'peaks_%05d.txt'%int(f+1)),ndmin=2)

        #####################
        # read coordinates and add to dataset

        for cnum in range(len(d)):
            MNI_coords=d[cnum]
            voxel_coords=convert_MNI_to_voxel_coords(MNI_coords,3)
            if validate_voxel_coords(voxel_coords,3)==0:
                #print 'coord not valid:', voxel_coords
                continue
            else:
                data[voxel_coords[0]][voxel_coords[1]][voxel_coords[2]]=1
                focictr+=1


mni_template='/work/01329/poldrack/software_lonestar/atlases/MNI152lin_3mm_mask_dil2mm.nii.gz'
template=nib.load(mni_template)

newimg=nib.Nifti1Image(data,template.get_affine())
newimg.to_filename('foci_data.nii.gz')
