#!/usr/bin/env python
import sys
def main(fname):
    toDo =set()
    with open('ids2do.csv') as f:    
        for l in f:
            toDo.add(l.split(',')[0].strip('"'))
    with open(fname) as f:
        for l in f:
            if l.split('\t')[1] in toDo:
                print l.strip()


if __name__== '__main__':
    try:
        main(sys.argv[1])
    except:
        print >>sys.stderr, "USAGE: %s  [file to filter]" % sys.argv[0]
        exit(1)