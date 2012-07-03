"""
get a set of topics relevant to a particular term,
and then find the matching hierarchy of topics at
the higher dimensionalities
- create a .dot file for later creation of figure
"""

import numpy as N
import pydot

term='language'
graph = pydot.Dot(term, graph_type='graph',rankdir='RL')



    
dims=[10,50,100,250]
data={}
loading={}
matching_topics={}
for dnum in range(len(dims)):
    #subg = pydot.Subgraph('%d'%dims[dnum], rank='same')
    #graph.add_subgraph(subg) 
    d=dims[dnum]
    loading[dnum]=N.loadtxt('fold1_%dloadingdata.txt'%d)
    f=open('fold1_%d/topic_keys.txt'%d)
    data[dnum]=[]
    for l in f.readlines():
            data[dnum].append(l.split('\t')[2].split(' ')[0:5])
    
    print '\n\n%d topics'%d
    matching_topics[dnum]=[]
    for n in range(len(data[dnum])):
        dline=data[dnum][n]
        if ' '.join(dline).find(term)>-1:
            print dline
            graph.add_node(pydot.Node('%d_%d'%(dims[dnum],n),
                                     label='%d_%d: '%(dims[dnum],n)+' '.join(dline),
                                     shape='box')) 
            matching_topics[dnum].append(n)
    

# find the matching topics at higher dimensions

for dnum in range(1,len(dims)):
    for lowertopic in matching_topics[dnum]:
        ltcorrs=N.zeros(dims[dnum-1])
        for uppertopic in matching_topics[dnum-1]:
            ltcorrs[uppertopic]=N.corrcoef(loading[dnum][:,lowertopic],loading[dnum-1][:,uppertopic])[0,1]
            if 0:
                print 'comparing'
                print '%d\t%d\t%s'%(dims[dnum],uppertopic,data[dnum][uppertopic])
                print '%d\t%d\t%s'%(dims[dnum+1],lowertopic,data[dnum+1][lowertopic])
                print 'r = %f'%ltcorrs[lowertopic]
        matchcorr=N.where(ltcorrs==N.max(ltcorrs))[0]
        print ''
        print 'MATCH: %d'%matchcorr
        print '%d\t%d\t%s'%(dims[dnum],lowertopic,data[dnum][lowertopic])
        print '%d\t%d\t%s'%(dims[dnum-1],matchcorr,data[dnum-1][matchcorr])
        print 'r = %f'%ltcorrs[matchcorr]
        graph.add_edge(pydot.Edge('%d_%d'%(dims[dnum],lowertopic),'%d_%d'%(dims[dnum-1],matchcorr),
                       label='%0.2f'%ltcorrs[matchcorr],labelfloat="true"))
        
graph.write('%s.dot'%term)