#!/usr/bin/env python
import re
dic = {}
def populateFreqDict(fname):
	with open(fname) as f:
		for l in f:
			w = re.split('\|| |\t', l.strip())[0]
			dic[w] = 0
	#print "character set:%d" % len(dic)
	

def main(f,stat=False):
	dup = {}
	for l in f:
		l = l.strip().split()
		c,w = l[:2]
		if w in dic:
			dup[c] = dup.get(c,[]) + [w]
	dup = [(c,hws) for c,hws in dup.iteritems() if len(hws)>1]
	if not stat:
		dup = sorted(dup,	key=lambda tup:tup[0])
		for ent in dup:
			print ent[0],''.join(ent[1])
	else:
		st = {}
		sum = 0
		for c,hws in dup:
			cnt = len(hws)
			st[cnt] = st.get(cnt,0) + 1
		for codelength,glyphcount in sorted([(k,v)for k,v in st.iteritems()],
			key=lambda ent:ent[0],reverse = True):
			sum += glyphcount
			print codelength,glyphcount
		print "\n-----------\nTOTAL: %d" % sum
if __name__=='__main__':
	import sys 
	if(len(sys.argv)<2):
		print "USAGE: %s [-stat] codelist [freqtable] " % sys.argv[0]
		exit(1)
	stat = sys.argv[1].strip() == '-stat'
	if stat:
		del sys.argv[0]
	populateFreqDict("charFreq.txt" if len(sys.argv) == 2 else sys.argv[2])
		
	with open(sys.argv[1]) as f:
		main(f,stat)
