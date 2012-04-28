#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ids
def getCommonComponents():
	ccoms = {}
	for g,i in ids._compounds.iteritems():
		els = ids.Ids.parse(i)[0].elements
		for el in els:
			ccoms[el] = ccoms.get(el,0) + 1
	with open('output/commonComponents.txt','w') as fo:
		for g,f in sorted(ccoms.iteritems()
		,key=lambda e:e[1],reverse=True):
			print >>fo, g.encode('utf8'), f
if __name__=='__main__':
	getCommonComponents()
