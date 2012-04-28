#!/usr/bin/env python
patch = {}
for l in open('compoundsPatch.txt'):
    hw,form,comm = l.strip().split('|')
    patch[hw] = (form,comm)

tmp = open('tmp','w')
for l in open('compounds.txt'):
    hw,form,comm = l.strip().split('|')
    if hw in patch:
        print >> tmp, hw + '|' + '|'.join(patch[hw])
    else:
        print >> tmp, l,
