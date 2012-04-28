#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ids
import sys

_ops0 = '⿰⿱⿲⿳⿴⿸⿺⿹⿵⿷⿶〾⿻'.decode('utf8')
_ops1 = u'HZWEOPLQNCUVDFX'

def main(fname):
    fel=open("el2add.txt","w")
    fcom = open("com2add.txt","w")
    fillegal = open('illegalids.txt','w')
    with open(fname) as f:
        for l in f:
            try:
                junk,glyph,formula = l.strip().decode('utf8').split('\t')
            except:
                print l
                raise
            
            if glyph == formula and glyph not in ids._elements:
                print >>fel,glyph.encode('utf8')
            elif glyph not in ids._compounds:                
                seq=[]
                for c in formula:
                    i = _ops0.find(c)
                    if i >= 0 :
                        c = _ops1[i]
                    elif c not in _ops1 and c not in ids._compounds and c not in ids._elements:
                        seq = []
                        break
                    seq.append(c)
                if not seq:
                    print >>fillegal, "%s has illegal char %s" %(l.strip(),c.encode('utf-8'))
                    
                else:
                    code = ''.join(seq)
                    ids.Ids.parse(code)
                    print >>fcom, ''.join([glyph,'|',code,'|']).encode('utf8')
                






if __name__=="__main__":
    main(sys.argv[1])