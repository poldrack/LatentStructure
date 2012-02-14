#!/usr/bin/env python

# read in foci and create a nifti image
# 
# for now we read from text file
# TBD: read directly from mysql db
#
#

import numpy as N
import nibabel as nb
import subprocess as sub
import os

from mniconvert import *

def foci_to_image(all_MNI_coords,outfileprefix,kernel='sphere',radius=10):
    try:
        FSLDIR=os.environ['FSLDIR']
    except:
        print 'it appears that FSL has not been configured'
        print 'you should set FSLDIR and then source $FSLDIR/etc/fslconf/fsl.{sh,csh}'
        return

# TBD: check foci format
# should be N x 3 array
    tmpdir='/tmp/'
    # use 3mm template to reduce data size
    mni_template='/data1/fmri/atlases/MNI152lin_3mm_mask_dil2mm.nii.gz'

    data=N.zeros((60,72,60))

    #####################
    # read coordinates and add to dataset

    for cnum in range(len(all_MNI_coords)):
        MNI_coords=all_MNI_coords[cnum]
        voxel_coords=convert_MNI_to_voxel_coords(MNI_coords,3)
        if validate_voxel_coords(voxel_coords,3)==0:
            #print 'coord not valid:', voxel_coords
            continue
        else:
            data[voxel_coords[0]][voxel_coords[1]][voxel_coords[2]]=1


    # KLUDGE: I've not been able to find any python code to do 3d convolution
    # so I am using an external call to fslmaths

    ###########################
    # save the unconvolved image
    mni_image=nb.load(mni_template)
    new_image=nb.Nifti1Image(data,mni_image.get_affine(),header=mni_image.get_header())
    tmpfname=tmpdir+'tmp_%.8f.nii.gz'%N.random.rand()
    new_image.to_filename(tmpfname)

    #####################
    # convolve points with sphere
    filt_tmpfname=tmpfname.replace('.nii.gz','_filt.nii.gz')
    if kernel=='gauss':
        cmd='fslmaths %s -kernel gauss %f -fmean %s'%(tmpfname,radius,filt_tmpfname)
    else:
        cmd='fslmaths %s -kernel sphere %f -fmean -bin %s'%(tmpfname,radius,outfileprefix)
    #print cmd
    p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
    output, errors = p.communicate()

    # clean up temp file
    if os.path.isfile(tmpfname):
        os.remove(tmpfname)
    # load the filtered image and ensure max = 1
    if kernel=='gauss':
        filt_image=nb.load(filt_tmpfname)
        filtdata=filt_image.get_data()
        filtdata=filtdata/N.max(filtdata)
        final_image=nb.Nifti1Image(filtdata,mni_image.get_affine(),header=mni_image.get_header())
        final_image.to_filename(outfileprefix+'.nii.gz')
        # clean up temp file
        if os.path.isfile(filt_tmpfname):
            os.remove(filt_tmpfname)
        




 
