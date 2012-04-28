#!/usr/bin/env python
#-*- coding: utf-8 -*-

def groupByCode(f,codes={}):    
    for l in f:
        l=l.strip().split()
        code,word = l[:2]
        freq = 0 if len(l)<3 else int(l[2])
        if code not in codes:codes[code]={}
        codes[code][word] = freq
    return codes
def _cmp(a,b):
    fa,fb=a[1],b[1]
    fcmp =fa.__cmp__(fb)
    if fcmp != 0 :return fcmp
    else:
        if a[0]>b[0]:return -1
        else:return 1
        
def codeDict2List(d):
    l=[]
    for k,v in d.iteritems():
        l.append((k,sorted(v.iteritems(),cmp=_cmp,reverse=True )))
    return sorted(l,key=lambda ent:ent[0])

def scim2mb(*fs):
    codes = {}
    for fn in fs:
        with open(fn) as f:
            codes = groupByCode(f,codes)
    for c,ws in codeDict2List(codes):
        print c,
        for w in ws:
            print w[0],
        print 

if __name__=='__main__':
    import sys
    scim2mb(*sys.argv[1:])
