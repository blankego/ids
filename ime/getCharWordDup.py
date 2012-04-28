#!/usr/bin/env python
import sys
def main():
	cset = set(l.strip().split()[0] for l in open('charFreq.txt'))
	cfreq = {}
	wfreq = {}
	
	for l in open('impalpable_build/table_with_freq.txt'):
		c,w,f = l.strip().split()
		if len(w)==3 and w in cset:
			cfreq[c]=(int(f),w)
	
	for l in open('impalpable_build/table_with_freq.txt'):
		c,w,f = l.strip().split()
		f = int(f)
		if len(w)>4 and c in cfreq and f > cfreq[c][0]:
			wfreq[c]=wfreq.get(c,[])+[(f,w)]
	
	for w in wfreq.itervalues():
		w.sort(key=lambda e:e[0],reverse=True)
	for k,v in wfreq.iteritems():
		cf,ch = cfreq[k]
		print k, ch + ',' +str(cf),
		for (wf,wrd) in v:
			print wrd +','+str(wf),
		print 
if __name__=='__main__':
	main()
#TODO: consider char dups as well
