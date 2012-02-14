""" get concepts from pubatlas terms

note: had to fix nidag database for full text editing using:

ALTER TABLE article_texts ADD FULLTEXT(text);

as recommended at http://devzone.zend.com/26/using-mysql-full-text-searching/

originally run on Macbook Pro

"""
import MySQLdb
import numpy as N
import re
import pickle

f=open('NIF_disorders.pkl','rb')
disorders=pickle.load(f)
f.close()

nconcepts=len(disorders.keys())
ndocs=5809
data=N.zeros((nconcepts,ndocs))

# connect to nidag database
conn = MySQLdb.connect (host = "localhost",
                        user = "root",
                           passwd = "",
                           db = "nidag")
cursor = conn.cursor()

disorderlist=[None]*nconcepts

logfile=open('NIF_query_log.txt','w')
for disorder_key in disorders.iterkeys():
    c=disorders[disorder_key]['classnumber']
    disorderlist[c]=disorders[disorder_key]['prefLabel'][0]
    print 'querying for #%d: %s'%(c,disorders[disorder_key]['prefLabel'][0])
    logfile.write('querying for #%d: %s\n'%(c,disorders[disorder_key]['prefLabel'][0]))
    resultctr=0
    for label in disorders[disorder_key]['prefLabel']+disorders[disorder_key]['synonyms']:
        label=label.lower().replace("\'"," ")
        query='select id,text from article_texts where match(text) against (\'"%s"\' in boolean mode);'%label
        #   print query
        fulltext_query=cursor.execute(query)
        fulltext_result=cursor.fetchall()
        for r in fulltext_result:
            text=r[1].lower().replace(')','').replace('(','').replace('-',' ')
            p=re.compile(label.replace('-',' ').replace("'","\s"))
            data[c,r[0]-1]+=len(p.findall(text))
                
        print '%s: %d'%(label,len(fulltext_result))
        logfile.write('%s: %d\n'%(label,len(fulltext_result)))
        
cursor.close ()
conn.close ()
logfile.close()

good_disorders=N.where(N.sum(data,1)>0)[0]

data_good=data[good_disorders,:]
disorderlist_good=[disorderlist[x] for x in good_disorders]

N.save('disorders_neurosynth_loadings.npy',data_good)
f=open('disorders_concepts.pkl','wb')
pickle.dump(disorderlist_good,f)
f.close()

