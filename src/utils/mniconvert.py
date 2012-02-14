import numpy as N
import nibabel as nb
import os
import scipy.linalg

####################
# apply lancaster tal-mni conversion
# from Tal Yarkoni, 4/8/2011

def tal_to_mni(foci,trans_type='SPM'):
	foci=N.hstack((N.array(foci),1))

	if trans_type=='SPM':
           trans = N.array([[0.9254, 0.0024, -0.0118, -1.0207], [-0.0048, 0.9316, -0.0871, -1.7667], [0.0152, 0.0883,  0.8924, 4.0926], [0.0, 0.0, 0.0, 1.0]])
	   #print 'using SPM transform'
	elif trans_type=='FSL':
           trans=N.array([[0.9464,0.0034,-0.0026,-1.0680],[-0.0083,0.9479,-0.0580,-1.0239],[0.0053,0.0617,0.9010,3.1883],[0.0,0.0,0.0,1.0]])
	   #print 'using FSL transform'
	else:  # use pooled as default
           trans=N.array([[0.9357, 0.0029, -0.0072, -1.0423], [-0.0065, 0.9396, -0.0726, -1.3940], [0.0103, 0.0752,  0.8967, 3.6475], [0.0, 0.0, 0.0, 1.0]])
	   #print 'using pooled transform'

        invtrans = scipy.linalg.pinv(trans)

        return N.dot(invtrans,foci)[0:3]

#####################
# convert coordinates from MNI to voxel space

def convert_MNI_to_voxel_coords(MNIcoord, resolution):
    # first check c
    if len(MNIcoord)!=3:
        raise IndexError

    # inv qform obtained from MNI152lin_T1_2mm_brain.nii.gz
    if resolution==2:
      invQForm=N.array([[ -0.5,  -0. ,  -0. ,  45. ],
       [  0. ,   0.5,   0. ,  63. ],
       [  0. ,   0. ,   0.5,  36. ],
       [  0. ,   0. ,   0. ,   1. ]])
    elif resolution==3:
      invQForm=N.array([[ -0.3333,0,0,30.0000],
         [0,0.3333,0,42.0000],
         [0,0,0.3333,24.0000],
         [0,0,0,1.0000]])
    else:
	    print '%dmm resolution not supported - exiting'%resolution
	    return


    # needs to be a homogenous coordinate array so add an extra 1 
    # in the 4th position
    coord_array=N.ones((1,4))
    coord_array[0][0:3]=MNIcoord

    trans_coord=N.dot(invQForm,coord_array.T)[:][0:3].T[0]

    return trans_coord

def validate_voxel_coords(voxcoord,resolution):

    try:
        FSLDIR=os.environ['FSLDIR']
    except:
        print 'it appears that FSL has not been configured'
        print 'you should set FSLDIR and then source $FSLDIR/etc/fslconf/fsl.{sh,csh}'
        return

            
    # check for negative coords
    if voxcoord[0]<0 or voxcoord[1]<0 or voxcoord[2]<0:
        print 'bad vox coords: %d %d %d'%(voxcoord[0],voxcoord[1],voxcoord[2])
        return 0

    # load MNI image
    if resolution==3:
        mni_template='/data1/fmri/atlases/MNI152lin_3mm_mask_dil2mm.nii.gz'
    else:
        mni_template=FSLDIR+'/data/standard/MNI152_T1_2mm_brain_mask_dil.nii.gz'

    mni_image=nb.load(mni_template)
    d=mni_image.get_data()

    # check coords for sanity
    try:
        dval=d[voxcoord[0]][voxcoord[1]][voxcoord[2]]
    except:
        print 'bad vox coords: %d %d %d'%(voxcoord[0],voxcoord[1],voxcoord[2])
        return 0

    # check for positive mask value
    if dval>0:
        return 1
    else:
        return 0
   
