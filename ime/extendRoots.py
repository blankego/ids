#!/usr/bin/env python
rParts = set(l.split(',')[0] for l in open('roots.csv'))
with open("../output/gcdivisors.txt") as f:
    for l in f:
        c = l.split()[0]
        if c not in rParts:
            print c +',,,,,'
