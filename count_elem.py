#!/usr/bin/env python
import ids
freq = {}

with open('idsdata/elements.txt') as fe:
    freq.update((l.strip().decode('utf8'),0) for l in fe)
with open('output/variants.txt') as fv:
    freq.update((l.strip().split()[0].decode('utf8'),0) for l in fv)
idss=[]
for g,i in ids._compounds.iteritems():
    idss.append(ids.Ids.parse(i)[0])
    
for i in idss:
    i.elaborate()
    
for i in idss:
    for e in i.elements:
        freq[e]+=1

fo= open('output/elements_with_freq.txt','w')
for k,v in sorted(((k.encode('utf8'),v) for k,v in freq.iteritems()),key=lambda it:it[1],reverse=True):
    print >>fo, k +' '+ str(v)
fo.close()
