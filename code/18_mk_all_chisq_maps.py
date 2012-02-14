f=open('18.1_mk_all_chisq_maps.sh','w')
for i in range(130):
    f.write('python /work/01329/poldrack/code/poldrack/textmining/paper/utils/mk_chisq_maps_filter.py cogatlas_lda_130 %d\n'%i)
    
for i in range(70):
    f.write('python /work/01329/poldrack/code/poldrack/textmining/paper/utils/mk_chisq_maps_filter.py disorders_lda_70 %d\n'%i)

f.close()
