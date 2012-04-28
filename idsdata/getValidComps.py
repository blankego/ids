#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
dc =set("⿰|⿱|⿲|⿳|⿴|⿵|⿶|⿷|⿸|⿹|⿺|⿻".split('|'))
tail = re.compile('\[.+?\]$')
def getValidComps(f):
    n=1
    for l in f:
        try:
            l=l.strip()            
            g,form =l.split('\t')[1:3]
            if g != form:
                form = tail.sub('',form)
                uform = form.decode('utf8')
                if form[:3] in dc and not any(c>=u'\uE000' and c<=u'\uF8FF'
                 or c == u'？' for c in uform):
                    print l[0] +'\t' + g +'\t' + form
            n+=1
        except:
            print ' '.join(l) + 'WTF at line %d' % n
            raise
if __name__=='__main__':
    import sys
    fi = open(sys.argv[1]) if len(sys.argv)>1 else sys.stdin
    getValidComps(fi)
