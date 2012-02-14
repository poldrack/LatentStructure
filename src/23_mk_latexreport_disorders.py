#!/usr/bin/env python

# make latex report for topic model
import numpy as N

ntopics=29
imgscale=0.5

ldadir='/Users/poldrack/data2/neurosynth_data_analysis/topic_models/disorders/disorders_lda_%d/'%ntopics

outfile=open(ldadir+'latex_report_topicthresh0.05_fdr0.01/topicreport_disorders_lda_%d.tex'%ntopics,'w')

outfile.write('''\\documentclass[12pt]{article}
\\usepackage{geometry}
\\geometry{letterpaper} 
\\usepackage{graphicx}
\\usepackage{amssymb}
\\usepackage{epstopdf}
\\DeclareGraphicsRule{.tif}{png}{.png}{`convert #1 `dirname #1`/`basename #1 .tif`.png}
\\title{Topic modeling report - full_lda_%d}

\\begin{document}
'''%ntopics)

# load topic data
topicfile=open(ldadir+'topic_keys.txt','r')
topickeys=topicfile.readlines()
topicfile.close()

# load entropy rankings
#entropyfile=open(ldadir+'topic_entropy_rank.txt','r')
#entropylist=entropyfile.readlines()
#entropyfile.close()
loadingdata=N.loadtxt(ldadir+'loadingdata.txt')
ndocs=N.sum(loadingdata>0,0)
idx=N.argsort(ndocs)

# insert images and text
#for t in range(ntopics):
for t in idx:
    outfile.write('''\\begin{figure}[htbp]
\\begin{center}
\\scalebox{%0.2f}{\\includegraphics{%s/slice_images/topic%03d_slices.png}}
\\caption{Topic %03d (%d docs): %s}
\\end{center}
\\end{figure}
\\newpage


'''%(imgscale,ldadir,t,t,ndocs[t],topickeys[t].split('\t')[2].strip().replace('_','\_')))


# write end of file

outfile.write('\\end{document}\n')
outfile.close()

