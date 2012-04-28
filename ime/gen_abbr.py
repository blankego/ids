#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2011 fermtect <fermtect@126.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import re

def main():
	short1 = set(l.strip().split()[1] for l in open('shorthands1.txt'))
	freq ={None:0}
	used=set(l.strip().split()[0] for l in open('tra_plus.txt'))
	ents =[]
	abbr3={}
	abbr2={}
	rsplit = re.compile('\|| |\t')
	#populate frequency dictionary
	freq.update((w,int(f)) for w,f in
		(rsplit.split(l.strip())[:2] for l in  open('totalFreq.txt'))
		if len(w) == 3
	)
	#freq.update((w,int(f)) for w,f in
		#(rsplit.split(l.strip())[:2] for l in open('charFreq.txt')))
	print "%d freqs done!" % len(freq)
	
	#read the table to the list ents and 
	
	#pick out all used short-form code
	for l in open('fullcodes.txt'):
		c,w = l.strip().split()	
		wl = len(w)
		cl = len(c)
		if wl == 3:
			if (cl==2 or cl==3) and freq.get(w,-1)>=0:
				used.add(c)
			if cl >3 and w not in short1 and w in freq:				
				ents.append([c,w])
	print "%d glyphs! %d used code!" %(len(ents),len(used))	
	
	for c,w in [l.strip('\n^').split() for l in open('phrasecode.txt')]:
		if len(w)==3 and  w not in short1 and w in freq:
			cf = freq.get(w,-1)
			if cf >=0 and c not in used:
				if cf > freq[abbr2.get(c,None)]:
					abbr2[c] = w
	print "%d 2-letter abbreviations" % len(abbr2)
	
	#put the most frequent chars to the abbr dict
	 
	for c,w in ents:
		cf = freq[w]
		init = c[:3]				
		if init not in used:
			if cf > freq[abbr3.get(init,None)]:
				abbr3[init]= w
	
	#write the result to file
	print "%d 3-letter abbreviations!" % len(abbr3)
	with open('tra_abbr.txt','w') as fo:
		for c,w in sorted(abbr2.iteritems(),key=lambda it:it[0]):
			print >> fo , c + ' ' + w
		for c,w in sorted(abbr3.iteritems(),key=lambda it:it[0]):
			print >> fo , c + ' ' + w

	
	return 0

if __name__ == '__main__':
	main()

