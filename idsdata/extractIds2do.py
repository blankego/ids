#!/usr/bin/env python
todo =  set(l.strip()for l in open('charset/cjkb.txt')) - \
        set(l.split('|')[0] for l in open('compounds.txt'))
with open('b2do.txt','w') as fo:
    for l in open('ids.txt'):   
       l=l.strip()
       parts=l.split('\t')
       if len(parts)<3:continue
       if parts[1] in todo:
         try:
             form = '\t'.join(parts[2:]).decode('utf8')
             print >>fo,'\t'.join( parts[:2]) + '\t' +\
                form.encode('utf8') + ('\t#' 
                if any(c>=u'\uE000' and c<=u'\uF8FF' or c == u'？' for c in form) else '')
         except:
             print >>fo,"!",l
