#!/usr/bin/env python
import ids
d={}
with open('output/ids_duplicates.txt','w') as fo:
  for k,v in ids._compounds.iteritems():
    if v not in d:
      d[v] = k
    else:
      print >>fo, ' '.join([d[v], k, v]).encode('utf8')
