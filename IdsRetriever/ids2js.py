#!/usr/bin/env python
import sys
sys.path += [".."]
import ids

def ids2js():
    with open('js/idsdataHeader.js','w') as fo:
        print >> fo, open('idsdataHeader.tmpl').read() % ids.tableVersion
    with open('js/idsdata.js','w') as fo:
        print >>fo,"Idsdata = {};"
        print >>fo,"(function(){\nif(!Idsdata.compounds)Idsdata.compounds={" 
        for g,i in ids._compounds.iteritems():
            print >>fo,'"%s":"%s",' %(g.encode('utf8'), i.encode('utf8'))
        print >>fo,"};"
        print >>fo,'Idsdata.elements ="'+\
            ''.join(el.encode('utf8') for el in ids._elements) +'";\n' +\
            'Idsdata.parts = {'            
        for i,gs in ids._partsDict.iteritems():
			print >>fo,'"%s":"%s",' %(i.encode('utf8'),u''.join(gs).encode('utf8'))
        print >>fo,"};\n})();"
if __name__=='__main__':
    ids2js()
