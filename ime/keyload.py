#! /usr/bin/env python
#-*- coding: utf8 -*-
import sys
import re
def main(f):
	dic = {}
	with open("charFreq.txt") as charfreq:
		for l in charfreq:
			char,freq = re.split(' |\||\t',l.strip())
			dic[char] = int(freq)
	kb = ["qwert","asdfg","zxcvb","yuiop[]","hjkl;","nm,./"]
	keyload = dict((c,0) for c in ''.join(kb))
	
	codes = {}
	for l in f:
		l=l.strip().split()
		code,w = l[:2]
		if dic.has_key(w):
			codes[w]=(code if len(codes.get(w,'     '))>len(code) else codes[w])
			
	for k,code in codes.iteritems():
		freq = dic[k]
		for c in code:
			keyload[c] += freq
	acc = 0
	
	for i  in range(1,7):
		part = kb[i-1]
		line = 0
		for c in part:
			load = keyload[c]
			acc += load 
			line += load
			print "%s[%-6i]" % (c,load),
		print line
		if i%3 == 0 :
			print acc
			acc = 0
	print acc
		
	#print codes['的']

if __name__=="__main__":
	with open(sys.argv[1]) as f:
		main(f)
