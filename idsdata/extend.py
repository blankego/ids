#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
dc = "⿰|⿱|⿲|⿳|⿴|⿵|⿶|⿷|⿸|⿹|⿺|⿻"
dcRe = re.compile(dc)
adc = "HZWEONUCPQLD"
dic = dict(zip(dc.split('|'),adc))
replace = lambda m:dic[m.group(0)]

def trFormulae(lst):
    res =[]
    for f in lst[2:]:
        f=f.strip()
        res.append(dcRe.sub(replace,f))
    return '|' + '|'.join(res) + ('|' if len(res)==1 else '')
import ids
def extend(f):
    comps = ids._compounds
    els = ids._elements
    with open('compSup.tmp','w') as fc:
        with open('elSup.tmp','w' ) as fe:
            for l in f:
                if l.startswith(";;"):continue
                l=l.strip().split('\t')
                g = l[1]
                if g not in comps:
                    if g != l[2]:
                        print >>fc, g + trFormulae(l)
                    elif g not in els:
                        print >>fe,g
            
                        
                        
        
if __name__=='__main__':
    import sys
    if len(sys.argv)== 1:
        extend(sys.stdin)
    else:
        with open(sys.argv[1]) as fi:
            extend(fi)
