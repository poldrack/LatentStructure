"""
run topic models using estimated dimensionalities
"""


import numpy as N

stubfile='/work/01329/poldrack/code/poldrack/textmining/paper/run_mallet_stub.sh'
f=open(stubfile)
stub=f.readlines()
f.close()

#datatypes=['disorders','cogatlas']
datatypes=['disorders']
for datatype in datatypes:
    likelihood_data=N.load('/scratch/01329/poldrack/textmining/paper/%s_8fold/%s_8fold_likelihood.npy'%(datatype,datatype))
    
                           
    ll=likelihood_data[1,:]
    ntopics=likelihood_data[0,:]

    maxll=N.where(ll==N.max(ll))
    print datatype,maxll,ntopics[maxll]
    
    f=open('run_mallet_%s_%d.sh'%(datatype,ntopics[maxll]),'w')
    f.write("#Automatically generated script\n")
    f.write('NTOPICS=%d\n'%ntopics[maxll])
    f.write('ALPHA=%f\n'%float(50.0/ntopics[maxll]))
    f.write('LABEL=%s\n'%datatype)
    for s in stub:
        f.write(s)
    f.close()
