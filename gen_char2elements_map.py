#!/usr/bin/env python

import ids

with open('output/char2elements_map.txt','w') as fo:
    for g,i in ids._compounds.iteritems():
        i = ids.Ids.parse(i)[0]
        i.elaborate()
        print >>fo,g.encode('utf8')+"|"+' '.join(i.elements).encode('utf8')
    