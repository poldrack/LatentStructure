#fslmerge -t /scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor /scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/chisquare_maps/topic_csq_cor_*.nii.gz

fslmerge -t /scratch/01329/poldrack/textmining/paper/topic_modeling/disorders/disorders_lda_29/all_topic_csq_cor /scratch/01329/poldrack/textmining/paper/topic_modeling/disorders/disorders_lda_29/chisquare_maps/topic_csq_cor_*.nii.gz

#fslmaths /scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor.nii.gz -Tstd -thr 0 -bin /scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor_mask

fslmaths /scratch/01329/poldrack/textmining/paper/topic_modeling/disorders/disorders_lda_29/all_topic_csq_cor.nii.gz -Tstd -thr 0 -bin /scratch/01329/poldrack/textmining/paper/topic_modeling/disorders/disorders_lda_29/all_topic_csq_cor_mask
#/work/01329/poldrack/software_lonestar/fsl/bin/flirt -in /scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor.nii.gz -applyxfm -init /work/01329/poldrack/software_lonestar/fsl/etc/flirtsch/ident.mat -out /scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor_6mm.nii.gz -paddingsize 0.0 -interp trilinear -ref /work/01329/poldrack/software_lonestar/atlases/MNI152_T1_6mm.nii.gz

/work/01329/poldrack/software_lonestar/fsl/bin/flirt -in /scratch/01329/poldrack/textmining/paper/topic_modeling/disorders/disorders_lda_29/all_topic_csq_cor.nii.gz -applyxfm -init /work/01329/poldrack/software_lonestar/fsl/etc/flirtsch/ident.mat -out /scratch/01329/poldrack/textmining/paper/topic_modeling/disorders/disorders_lda_29/all_topic_csq_cor_6mm.nii.gz -paddingsize 0.0 -interp trilinear -ref /work/01329/poldrack/software_lonestar/atlases/MNI152_T1_6mm.nii.gz

#fslmaths /scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor_6mm.nii.gz -Tstd -thr 0 -bin /scratch/01329/poldrack/textmining/paper/topic_modeling/cogatlas/cogatlas_lda_130/all_topic_csq_cor_6mm_mask

fslmaths /scratch/01329/poldrack/textmining/paper/topic_modeling/disorders/disorders_lda_29/all_topic_csq_cor_6mm.nii.gz -Tstd -thr 0 -bin /scratch/01329/poldrack/textmining/paper/topic_modeling/disorders/disorders_lda_29/all_topic_csq_cor_6mm_mask
