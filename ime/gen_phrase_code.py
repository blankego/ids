#! /usr/bin/env python


import sys 

def importPhraseCodeDict(dic={}):
   f= open('phrasecode.txt')
   for l in f:
      cols=l.strip('\n^').split()
      dic[cols[1].decode('utf8')] = cols[0]
   f.close()
   return dic

def genPhraseCode(fname, codeDic):
   f=open(fname )
   for l in f:
      l = l.strip()
      if l [0] == '#' or l == '': continue
      cols = l.split('|')
      phrase = cols[0].decode('utf8')
      cs=[]
      for ch in phrase[:4]:
         code = codeDic.get(ch,None)
         if not code:
            sys.stderr.write("Code for %s not found!\n" % ch.encode('utf8'))
            exit(1)
         cs.append(code)
      pLen = len(cs)
      if pLen == 2:
         codes = ''.join(cs)
      elif pLen == 3:
         codes = cs[0][0]+cs[1]+cs[2][0]
      elif pLen == 4:
         codes = ''.join([c[0] for c in cs])
      print codes  + " " + cols[0] + ' ' + cols[1]

if __name__ == '__main__':
   if len(sys.argv)!= 2:
      print "USAGE: %s phrase_table_file"
      exit(1)
   genPhraseCode(sys.argv[1],importPhraseCodeDict())

            
