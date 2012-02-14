#!/usr/bin/env python
"""
load NIF dysfnction ontology and grab synonyms

NOTE: made following changes to NIF file, need to pass back to NIF:
- added Korsakoff's syndrome
- removed "Alzheimer's" since it will match to more specific terms
- added "dementia of the alzheimer type"
- removed Parkinson's and Parkinsons
- removed Huntington's and HD
- removed TS
- changed default label from Tourette's to Tourettes to prevent problems with apostropphe

added additional terms missing from NIF:
- dyslexia
- alexia
- specific language impairment
- acquired aphasia

"""
import pickle

#'rp1':{'prefLabel':'amnesia','synonyms':[]}
    
added_disorders={'rp1':{'prefLabel':'amnesia','synonyms':['amnestic syndrome']},\
    'rp2':{'prefLabel':'dyslexia','synonyms':['reading disability','reading disorder']},\
    'rp3':{'prefLabel':'alexia','synonyms':['acquired dyslexia']},\
    'rp4':{'prefLabel':'specific language impairment','synonyms':['SLI', 'language delay']},\
    'rp5':{'prefLabel':'dissociative disorder','synonyms':['multiple personality disorder']},\
    'rp6':{'prefLabel':'impulse control disorder','synonyms':[]},
    'rp7':{'prefLabel':'gambling','synonyms':[]},
    'rp8':{'prefLabel':'trichotillomania','synonyms':[]},
    'rp9':{'prefLabel':'attention deficit disorder','synonyms':['attention deficit hyperactivity disorder','ADHD']},
    'rp10':{'prefLabel':'conduct disorder','synonyms':['Oppositional Defiance Disorder','Oppositional Defiant Disorder']},
    'rp11':{'prefLabel':'antisocial personality disorder','synonyms':[]},
    'rp12':{'prefLabel':'borderline personality disorder','synonyms':[]}, 
    'rp13':{'prefLabel':'compulsive personality disorder','synonyms':[]}, 
    'rp14':{'prefLabel':'histrionic personality disorder','synonyms':[]}, 
    'rp15':{'prefLabel':'paranoid personality disorder','synonyms':[]}, 
    'rp16':{'prefLabel':'passive-aggressive personality disorder','synonyms':[]}, 
    'rp17':{'prefLabel':'schizoid personality disorder','synonyms':[]}, 
    'rp18':{'prefLabel':'schizotypal personality disorder','synonyms':['schizotypal disorder','schizotypy']}}

def strip_owl_format(owl):
    return owl.split('>')[1].split('<')[0]

nif_file='NIF-Dysfunction.owl'
f=open(nif_file,'r')
disorders={}
found_class=0
classctr=0
onto_id=[]

for line in f.readlines():
    # first check to see if we are at the top of a good class
    if line.find('NIF-Dysfunction')>0 and line.find('<owl:Class')>0 and found_class==0:
        try:
            onto_id=line.strip().split('#')[1].replace('">','').replace('"/>','')
            disorders[onto_id]={}
            disorders[onto_id]['prefLabel']=[]
            disorders[onto_id]['synonyms']=[]
            disorders[onto_id]['classnumber']=classctr
            classctr+=1
            print 'found class: %s'%onto_id
            print line
            found_class=1
        except:
            print 'bad line: %s'%line
            pass
        #then make sure that we are not at the end of a class
    elif found_class==1 and line.find('</owl:Class')>0:
        #print 'found end of class %s'%onto_id
        found_class=0
        onto_id=[]
    #we are in a good class, so parse it to get label and synonyms
    elif onto_id:
        print line
        if line.find('obo_annot:synonym')>0:
            disorders[onto_id]['synonyms'].append(strip_owl_format(line).replace('&#39;',"\'"))
        if line.find('rdfs:label')>0:
            disorders[onto_id]['prefLabel'].append(strip_owl_format(line).replace('&#39;',"\'"))

for ak in added_disorders.iterkeys():
    added_disorders[ak]['prefLabel']=[added_disorders[ak]['prefLabel']]
    disorders[ak]=added_disorders[ak]
    disorders[ak]['classnumber']=classctr
    classctr+=1
    
f=open('NIF_disorders.pkl','wb')
pickle.dump(disorders,f)
f.close()


