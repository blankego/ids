#!/usr/bin/env python
# -*- coding: utf-8 -*-
#TODO: a lot of redundant methods need to be cleaned up
from  copy import copy
import os
import re
_datapath = os.path.join(
    (os.path.dirname(__file__) if __file__ else ''),'idsdata')

_compounds = {}
_partsDict = None
_ids2char = {}
_elements = set()
_operators = {u'H':2,u'W':3,u'Z':2,u'E':3,u'O':2,u'P':2,u'Q':2,
    u'L':2,u'N':2,u'U':2,u'C':2,u'D':2,u'V':1,u'F':1}
tableVersion = '0'

def _getFileVer(f):
    verRe = re.compile(r'# *VERSION *: *([\d.]+)',re.I)
    l = f.readline()        
    while l and (not l.strip() or l.startswith('#')):            
        m = verRe.match(l)
        if m:
            v = m.group(1)
            break
        l = f.readline()
    return v,l

def _mod_init():    
    global _compounds, _elements, tableVersion
    with open(os.path.join(_datapath,'elements.txt')) as f:
        for l in f:
            _elements.add(l.strip().decode('utf8'))
    with open(os.path.join(_datapath,'compounds.txt')) as f:
        #get version number
        tableVersion,l = _getFileVer(f)
        while l:   
            l=l.strip()
            if l and not l.startswith('#'):
                l=l.decode('utf8').split(u'|')
                glyph, formula = l[0], l[1].split()[0]
                _compounds[glyph] = formula
                _ids2char[formula] = _ids2char.get(formula,'') + glyph
            l=f.readline()

_mod_init()

##For debug
coms = _compounds
els = _elements
##
import codecs

class _UniQueuer(object):
    def __init__(self,s):
        self.s = codecs.iterdecode( s, 'utf8') if isinstance(s,str) else iter(s)
        self.seq = self.s        
    def __iter__(self):
        return self
    def next(self):
        try:
            return self.seq.next()
        except StopIteration:
            if self.seq != self.s:
                self.seq = self.s
                return self.seq.next()
    def unshift(self,head):
        self.seq = head

class Ids(object):
    
    """"""
    @staticmethod
    def parse(code,isUniQueue = False,):
        """assume the input is piece of code represents a single unit"""
        try:
            if not isUniQueue:
                code = _UniQueuer(code)
            initial = code.next()
            if initial == u'V' or initial == u'F':
                #variant or flipped char
                return Ids(None,initial + code.next())
            else:
                nEl = _operators.get(initial,None)
                if nEl:
                    #compound
                    if nEl == 2:
                        #check if it's a gouged char such as 'Q鳥X'
                        c1,c2 = code.next(),code.next()
                        if c1 == u'X' and ord(c2) >= 0x3400 or \
                            ord(c1) >= 0x3400 and c2 == u'X':
                            #slacky check if it's a zh char
                            return Ids(None, initial+c1+c2)
                        else:
                            #if it's no gouged char, spit it out
                            code.unshift(iter((c1,c2)))
                    #normal compound
                    op = initial                    
                    parts = [Ids.parse(code, True) for i in range(nEl)]
                    return Ids(op,parts)
                else:                    
                    #unknown level char
                    return Ids(None,initial)
        except:
            #print code.encode('utf8')
            raise
        
        
            
        
    def __init__(self,op,parts):
        """do not call this directly!"""
        self.op = op
        self.parts = parts
        
    def elaborate(self):
        try:
            if self.op:
                for ch in self.parts:
                    ch.elaborate()
            elif self.isElement:
                return
            else:
                #non-element char
                ids = Ids.parse(_compounds[self.parts])
                self.op, self.parts = ids.op, ids.parts
                self.elaborate()
            return self
        except:
            print self
            raise
    
    def synthesize(self):
        if not self.isChar:            
                self.parts = self.chrForm
                self.op = None
        return self
    def __unicode__(self):
        if self.isChar:
            return self.parts
        else:
            return self.op + u''.join(ch.__unicode__() for ch in self.parts)
    
    def __str__(self):
        if self.isChar:
            return self.parts.encode('utf8')
        else:
            return self.op.encode('utf8') + ''.join(str(ch) for ch in self.parts)
    def __repr__(self):
        return '[%s]' % str(self)
    @property
    def isChar(self):
        return  not self.op
    
    @property
    def isElaborated(self):
        """If all descendant components have been totally analysed to elements"""
        if self.isChar:
            return self.isElement
        else:
            return all(ch.isElaborated for ch in self.parts)
    
    
    @property
    def isElement(self):
        """If it's a fundamental glyph, with which all kanjis are constituted"""
        if not self.isChar:
            return False
        else:
            if len(self.parts)>1:
                #gouged component
                return True
            else:
                return self.parts in _elements
            
    def __contains__(self,part):
        if self.isChar and part.decode('utf8') == self.parts:                        
                return True            
        else:
            return any(ch.__contains__(part) 
                for ch in self.children)            
    
    
    @property
    def chrForm(self):
        if self.isChar:
            return self.parts
        else:
            try:
                return _ids2char[self.op  + u''.join( part.chrForm for part in self.parts)]
            except KeyError:
                return ''
    #mimic list
    def __iter__(self):
        self.idx = -1
        return self
    def next(self):
        if self.isChar:
            if self.idx == -2:raise StopIteration
            else:
                self.idx = -2
                return self
        else:
            self.idx += 1
            if self.idx >= len(self.parts):
                raise StopIteration
            else:
                return self.parts[self.idx]
    def __len__(self):
        return 1 if self.isChar else len(self.parts)
    def __getitem__(self,idx):
        if not self.isChar:
            return self.parts[idx]
        elif idx == 0 or idx == -1:
            return self
        else:
            raise IndexError
    
    @property
    def divided(self):
        if not self.isChar or self.isElement:
            return self
        else:
            return Ids.parse(_compounds[self.parts])
    @property
    def children(self):
        """immediate children"""
        if self.isElement:
            return []
        else:
            if self.isChar:
                return Ids.parse( _compounds[self.parts]).children
            else:
                return self.parts
                
            
parse = Ids.parse

def _getParts(i):
    for ch in i.parts:            
        if ch.isChar:
            yield ch.parts
        else:
            for  p in  _getParts(ch):
                yield p

def _populatePartsDict():
    import cPickle
    global _partsDict
    if not _partsDict:        
        picklePath = os.path.join(_datapath,"compsDict.pickle")
        if os.access(picklePath,os.R_OK):
            v,d = cPickle.load(open(picklePath))
            if v == tableVersion:#if versions match then done
                _partsDict = d
                return
                
        _partsDict = {}
        
        for g,i in _compounds.iteritems():            
            i = parse(i)
            for p in _getParts(i):
                ents = _partsDict.get(p,None)            
                if ents:
                    ents.add(g)
                else:
                    _partsDict[p] = set(g)            
        cPickle.dump((tableVersion,_partsDict),open(picklePath,'w'))
        

_populatePartsDict()
def getCharsByParts(*parts):
    
    chars = None
    for p in parts:
        if isinstance(p,str):p = p.decode('utf8')
        if not chars:chars = _partsDict[p] 
        else:
            chars = chars & _partsDict[p]
    return CharList(chars)

def getCharsByIds(i):
    i = parse(i)
    return i.chrForm

class CharList(list):
    def __init__(self,l):
        super(CharList,self).__init__(sorted(l))
    def __str__(self):
        return '〖' + ', '.join(c.encode('utf8') for c in self) + '〗'
    def __repr__(self):return self.__str__()
