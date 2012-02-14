# merge all images
fslmerge -t /scratch/01329/poldrack/textmining/paper/data_preparation/all_peakimages.nii.gz /scratch/01329/poldrack/textmining/paper/data_preparation/peakimages/*.nii.gz
# compute mask, excluding voxels that are not active on at 
# least 1% of papers
fslmaths /scratch/01329/poldrack/textmining/paper/data_preparation/all_peakimages.nii.gz -Tmean -thr 0.01 -bin /scratch/01329/poldrack/textmining/paper/data_preparation/all_peakimages_mask

