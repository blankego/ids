#!/usr/bin/env python
orig = {}
for l in open('zmOrig.txt'):
    c,g = l.strip().split()
    orig[g.decode('utf8')]=c
cset = set(l.strip().split('\t')[0].decode('utf8') for l in open('charFreq.txt'))
import genImeTable
genImeTable.readRootDic()
gen = genImeTable.genOrigZm()
for g,c in gen.iteritems():
  if g in cset:
    co = orig.get(g,None)
    if co and co != c:
        print g.encode('utf8'),c,co
