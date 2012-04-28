#!/usr/bin/env python
import ids
def tryGetVar(i):
    if i.isChar:
        if len(i.parts)>1:yield i.parts
    else:
        for c in i.children:
            for v in tryGetVar(c):
                yield v

def main():
    with open('output/variants.txt','w') as fo:
        vars={}
        for g,form in ids._compounds.iteritems():
            for i in ids.Ids.parse(form):
                for v in tryGetVar(i):
                    vars[v]=g    
                
                    
        for i,g in sorted(vars.iteritems(),key=lambda ent:ent[0]):
            print >>fo, (i+' '+g).encode('utf8')

if __name__ == '__main__':
    main()
