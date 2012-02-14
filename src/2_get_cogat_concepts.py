""" get concepts from rdf

note: had to fix nidag database for full text editing using:

ALTER TABLE article_texts ADD FULLTEXT(text);

as recommended at http://devzone.zend.com/26/using-mysql-full-text-searching/
"""
import MySQLdb
import numpy as N
import re
    
f=open('cogat_concepts.rdf','r')
concepts=[]
for l in f.readlines():
    if l.find('prefLabel')>0:
        c=l.strip().split('>')[-1]
        concepts.append(c.strip(' ').strip('.').replace('"','').strip())
        print concepts[-1]
        
f.close()

nconcepts=len(concepts)
ndocs=5809
data=N.zeros((nconcepts,ndocs))

# connect to nidag database
conn = MySQLdb.connect (host = "localhost",
                        user = "root",
                           passwd = "",
                           db = "nidag")
cursor = conn.cursor()

for c in range(nconcepts):
    query='select id,text from article_texts where match(text) against (\'"%s"\' in boolean mode);'%concepts[c]
    print query
    fulltext_query=cursor.execute(query)
    fulltext_result=cursor.fetchall()
    
    print '%s: %d'%(concepts[c],len(fulltext_result))
    for r in fulltext_result:
        text=r[1].lower().replace(')','').replace('(','')
        p=re.compile(concepts[c])
        data[c,r[0]-1]=len(p.findall(text))
                    
    
cursor.close ()
conn.close ()

N.save('cogat_neurosynth_loadings.npy',data)
import pickle
f=open('cogat_concepts.pkl','wb')
pickle.dump(concepts,f)
f.close()

