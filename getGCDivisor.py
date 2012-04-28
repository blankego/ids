#!/usr/bin/env python
import ids
def _getParts(i):
    for ch in i.parts:            
            if ch.isChar:
                yield ch.parts
            else:
                for  p in  _getParts(ch):
                    yield p
                   

    
def getGCDivisor():
    gcd = {}
  
    for g,form in ids._compounds.iteritems():
        i = ids.Ids.parse(form)
        for p in _getParts(i):
            if len(p) > 1:
                gcd[p] = gcd.get(p,[]) + [g]
            elif p not in ids._compounds:
                gcd[p] = gcd.get(p,[]) + [g]
    return gcd            
    
    
            

if __name__== '__main__':
    
    for comp,glyphs in sorted(getGCDivisor().iteritems(),key = lambda ent:len(ent[1]),
        reverse = True):
        print comp.encode('utf8'),len(glyphs),glyphs[0].encode('utf8')
