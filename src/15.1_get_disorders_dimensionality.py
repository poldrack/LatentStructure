"""
run topic models at decreasing dimensionality from 60
to find one without any duplicated topics
"""


import numpy as N

stubfile='/work/01329/poldrack/code/poldrack/textmining/paper/run_mallet_stub.sh'
f=open(stubfile)
stub=f.readlines()
f.close()

#datatypes=['disorders','cogatlas']
datatypes=['disorders']
for datatype in datatypes:

  for ntopics in range(20,60):
    
    f=open('run_mallet_%s_%d.sh'%(datatype,ntopics),'w')
    f.write("#Automatically generated script\n")
    f.write('NTOPICS=%d\n'%ntopics)
    f.write('ALPHA=%f\n'%float(50.0/ntopics))
    f.write('LABEL=%s\n'%datatype)
    for s in stub:
        f.write(s)
    f.close()
