# extract text from nidag database to perform topic modeling

import MySQLdb

# connect to nidag database
conn = MySQLdb.connect (host = "localhost",
                        user = "articles_foci",
                           passwd = "",
                           db = "articles_foci")
cursor = conn.cursor()

query='select * from articles where active=1;'
active_articles_query=cursor.execute(query)
active_articles_result=cursor.fetchall()
print 'found %d articles'%len(active_articles_result)
for article in active_articles_result:
    query='select text from article_texts where article_id=%d'%article[0]
    fulltext_query=cursor.execute(query)
    fulltext_result=cursor.fetchall()
    f=open('/data1/poldracklab/textmining/fulltext/nidag_%05d.txt'%article[0],'w')
    f.write(fulltext_result[0][0])
    f.close()





cursor.close ()
conn.close ()
