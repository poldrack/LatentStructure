#!/usr/bin/env python

# read foci from database
# and create image for each paper

import MySQLdb
from foci_to_image import *

conn = MySQLdb.connect (host = "localhost",
                        user = "articles_foci",
                           passwd = "",
                           db = "articles_foci")
cursor = conn.cursor ()

basedir='/data1/poldracklab/textmining/1_database/'
peakimgdir=basedir+'peakimages/'
peaktextdir=basedir+'peakfiles/'

query='select * from articles where active=1;'
active_articles_query=cursor.execute(query)
active_articles_result=cursor.fetchall()
print 'found %d articles'%len(active_articles_result)
for article in active_articles_result:
    outfile=open(peaktextdir+'peaks_%05d.txt'%article[0],'w')
    peaklist=[]
    print 'article %d'%article[0]
    tables_query=cursor.execute('select id from tables where article_id=%d'%article[0])
    tables_result=cursor.fetchall()
    for t in tables_result:
        #print 'table %d'%t[0]
        peaks_query=cursor.execute('select * from peaks where table_id=%d'%t[0])
        peaksresult=cursor.fetchall()
        for p in peaksresult:
            if article[14]=='TAL':  # do Tal-MNI conversion
                mnifoci=tal_to_mni([p[6],p[7],p[8]])
                print '%d,%d,%d became %0.1f,%0.1f,%01.f'%(p[6],p[7],p[8],mnifoci[0],mnifoci[1],mnifoci[2])
            outfile.write('%d %d %d\n'%(p[6],p[7],p[8]))
            #print 'peak %d: %d %d %d'%(p[0],p[6],p[7],p[8])
            peaklist.append([p[6],p[7],p[8]])
        foci_to_image(peaklist,peakimgdir+'paper%05d'%article[0])

cursor.close ()
conn.close ()
