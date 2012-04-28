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

import sys

##prepare char list for rearrange frequency of words which have
##duplicated codes of common characters
#cCharFreq = {}
#def prepare():
	#d = dict((k,int(v)) for k,v in 
	#(l.strip().split() for l in open('charFreq.txt')))
	#for l in open('fullcodes.txt'):
		#c,w = l.strip().split()
		#if w in d:
			#cCharFreq[c] = d[w]

def main(fname):
	#prepare()
	fDic = dict(l.strip().split('|') for l in 
		open('totalFreq.txt') )
	fDic.update(l.strip().split() for l in open('component_freq.txt'))
	abbrs = set(l.split()[1] for l in open('tra_abbr.txt'))
	dupFullcode={}
	for l in open('dupCodes.txt'):
		c,ws=l.strip().split()
		for w in ws.decode('utf8'):
			w = w.encode('utf8')
			if w in abbrs:
				dupFullcode[w] = c
	cwDup = {}
	for l in open('charWordDup.txt'):
		if l[0]!="#":
			c,ch,w = l.strip().split()[:3]
			cwDup[c]=(ch.split(',')[0],str(int(w.split(',')[1])+1))
	
	f=open(fname)	
	for l in f:
		code,word=l.strip().split()[:2]
		wLen = len(word)
		cLen = len(code)
		if wLen == 3 and cLen == 4 and code.endswith('vv') and word in abbrs:
			continue
		if wLen==3 and dupFullcode.get(word,'')== code:
			freq = '11'
		else:
			freq = fDic.get(word,'0')
			##adjust freq for words that have duplicated codes of
			##common chars
			if wLen==3 and cLen == 4 and code in cwDup:
				newFreq = cwDup[code]
				if word == newFreq[0]:
					freq = newFreq[1]
			
		print code +' '+word+' '+ freq 
	return 0

if __name__ == '__main__':	
	main(sys.argv[1])

