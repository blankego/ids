#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path += ['..']
import ids
rootDic = {}
origRootDic = {}
rootCode = {}
specPhraseCode = {}
commonChrs= None
def wrapCode(c):
    if isinstance(c,str):
        return [[el] for el in c.split()]
    else:
        return map(wrapCode, c)

def readSpecPhraseCode():
    specPhraseCode.update((k.decode('utf8'),v) for (v,k) in (l.strip().split() for l in open('specPhraseCode.txt')))
def readCommonChrs():
    global commonChrs
    commonChrs = dict((g.decode('utf8'),int(f)) for g,f in (
        l.split('\t')[:2] for l in open('charFreq.txt')))
    #print >>sys.stderr,"common chars: %d" % len(commonChrs)
def readRootDic():
    for l in open('roots.csv'):
        l = l.strip().split(',')
        g, c1,c2,c3,orig = l[:5] 
        g=g.decode('utf8')
        code = wrapCode(c2.split('|')) if c2 else wrapCode(c1)
        rootDic[g] = code        
        origRootDic[g] = (c1 if not orig else orig).split()
        if c3:
            rootCode[g] = c3

def fstCode(p):    
    while isinstance(p,list):
        p = p[0]
    return p
    
def lstCode(p):
    while isinstance(p,list):
        p = p[-1]
    return p

def getRoots(i,top=False):
    try:
        if i.isChar and i.parts in rootDic:
            return rootDic[i.parts]
        else:
            div = i.divided
            #if not children:
                #print >>sys.stderr, 'cathca! %s' % str(i)
                #raise
            if div.op == u'L' and div[0].isChar and div[0].parts in u'辶廴⻍':
                #print >>sys.stderr , str(i)
                div = (div[1],div[0])
            elif div.op == u'W' and div[0].isChar and div[0].parts == u'彳' and \
                div[2].isChar and div[2].parts == u'亍':
                return  [['o'],getRoots(div[1]),['i']]
            elif div.op == u'U' and div[0].isChar and div[0].parts ==u'V舁':
                return [['nb'],getRoots(div[1]),['o']]
            res = []
            for p in div:        
                res.append(getRoots(p))
            
            return res 
    except RuntimeError:
            print >>sys.stderr,i.parts
            exit(0)

limit = 4        

def finishCode(picked,last):
    code = ''.join(picked)
    rLen = limit - len(code)
    code += last[1:1+rLen]
    if len(code) == 2:
        code +='vv'
    return code

    
def encode2(part):
    nP = len(part)
    if nP >= 2:
        return  [fstCode(part)[0] , lstCode(part)[0]]
    elif nP == 1:
        singleton = part[0]
        if isinstance(singleton,list):
            return encode2(singleton)
        return [fstCode(part)[0]] #leave the complement to the finishCode func
    else:
        return []

def encode3(part):
    #part must be a list
    nP = len(part)
    res = []
    if nP >= 3:
        res = [fstCode( part[0])[0], fstCode(part[1])[0], lstCode(part[-1])[0]]
    else:
        if nP == 2:
            fst,snd = part
            if isinstance(fst,list) :
                # the sibling comps always be of the same type (all lists or all strings)
                if len(fst)>=2:
                    #[[a,b],[c]]
                    res = [fstCode(fst)[  0], lstCode(fst)[0], lstCode(snd)[0]]            
                elif len(snd)>=2:
                    #[[a],[b,c]]
                    res = [fstCode(fst)[0], fstCode(snd)[0],lstCode(snd)[0]]
                else:
                    #[['a..'],['b..']]
                    res = [fstCode(fst)[:2],lstCode(snd)[0]]
            else:
                #['a..','b..']
                res = [fst[:2], snd[0]]
        elif nP == 1:
            # ["a.."]
            singleton = part[0]
            if isinstance(singleton,list):
                return encode3(singleton)
            res = [fstCode(part)[0]]
    return res

def tryGet3StrParts(roots,deep=False):
    res = []
    for p in roots:
        if len(p) == 1 and isinstance(p[0],str):
                res.append( p[0])
            
        else:
            got = tryGet3StrParts(p,True)
            if not got:return None
            res += got            
    return res if deep or len(res) == 3 else None
        
def genCode3(roots):
    parts = tryGet3StrParts(roots)
    if not parts:return None
    a,b,c = parts
    #la,lb,lc = len(a),len(b),len(c)
    #if la >1 and lb == 1 :
        #return a[0] + b + c[0]
    #elif la == 1 and lb > 1 :
        #return a + b[0] + c[0]
    return a[0] + b[0] + c[0]
    return None
    
def genIme():
    fullCodes = {}
    threeCodes = {}
    shortCodes = {}
    g=None
    try:
        for g,i in sorted(ids._compounds.iteritems(),key=lambda ent:ent[0]):            
            if g in rootDic or g in fullCodes:
                continue
            else:
                i = ids.Ids.parse(i)
                roots = getRoots(i,True)     
            code,seq = encode(roots)     
               
            #if len(seq) < 1 :
                #print g.encode('utf8')
                #exit(1)            
            
            
            fullCodes[g] = code
            if g in commonChrs:
                code3 = genCode3(roots)
                if code3 and code3!=code:
                    threeCodes[g] = code3
            short = seq[0][0] + seq[1][0] if len(seq)>1 else seq[0][:2]
            shortCodes[g] = short
        for g,i in rootDic.iteritems():
            if len(g) == 1 and g not in fullCodes:
                if g in rootCode:
                    code = rootCode[g]                                      
                    short = code[:2] 
                else:
                    roots = i
                    code,seq = encode(roots)
                    short = seq[0][0] + seq[1][0] if len(seq)>1 else seq[0][:2]
                    if g in commonChrs:
                        code3 = genCode3(roots)
                        if code3 and code3 != code:
                            threeCodes[g] = code3
                
                fullCodes[g] = code
                shortCodes[g] = short
        shortCodes.update(specPhraseCode)
        codeset = set(fullCodes.itervalues())
        print >>sys.stderr, len(threeCodes)
        with open('fullcodes.txt','w') as fo:
            for g,c in sorted(fullCodes.iteritems(),key=lambda e:e[1]):
                print >> fo, c, g.encode('utf8')
            c3s = {}
            
            for g,c in threeCodes.iteritems():                
                
                freq = commonChrs[g]
                if c not in c3s or c3s[c][0] < freq:
                    c3s[c]=(freq,g)
            with open('tra_3_abbr.txt','w') as f3:
                for c,(f,g) in sorted( c3s.iteritems(),key=lambda e:e[0]):
                    g=g.encode('utf8')
                    if  c not in codeset:
                        print >>fo,c,g
                        print >>f3,c,g
                    else:
                        print >>f3,"#"+c,g
        with open('phrasecode.txt','w') as fo:
            for g,c in sorted(shortCodes.iteritems(),key=lambda e:e[1]):
                print >> fo, c, g.encode('utf8')
    except:
        print >>sys.stderr, g.encode('utf8')
        #raise
        exit(1)
def encode(roots,limit = 4):
        try:
            fstPart = roots[0]
            nFst = len(fstPart)
            fstRoot = fstCode(fstPart)
            nParts = len(roots)            
            if nParts > 1:
                lstPart  = roots[-1]
                lstRoot =  lstCode(lstPart)
                lLst = len(lstRoot)
                lstInit = lstRoot[0]
                nLst = len(lstPart)
                if nParts >=3:
                    midPart = roots[1]
                    nMid = len(midPart)
               
               
            code = ''
            picked = []
            
            if nFst == 1:
                #(1,x...)   
                picked.append(fstRoot)
                lFst = len(fstRoot)     
                if nParts > 1:              
                    if lFst == 3:
                        picked.append(lstInit)                    
                    elif lFst == 2:
                        picked += encode2(roots[1:])
                    else:
                        #length of first root = 1
                        picked += encode3(roots[1:])
                        #if len(picked) == 3 and len(picked[1]) + len(picked[2])==2:
                            #picked[2]+='v'   
                    code = finishCode(picked,lstRoot)
                    
            else:
                #(2+,x...)
                if nParts == 1:
                    return encode(fstPart)
                else:
                    if nParts >=3 or nLst > 1:
                        picked = encode2(fstPart) + encode2(roots[1:])
                    else:
                        #nLst = 0
                        picked = encode3(fstPart) + [lstInit]
                    
                    code = finishCode(picked,lstRoot)
            if not code: code = ''.join(picked)
            return code, picked
        except:
            print >>sys.stderr,roots
            raise

#def flattenRoots(roots):
    #res = []
    #for el in roots:
        #if isinstance(el,list):
            #res += flattenRoots(el)
        #else:
            #res.append(el)
    #return res

def getOrigRoots(i):
    if i.isChar and i.parts in origRootDic:
        return origRootDic[i.parts]
    else:
        div = i.divided        
        if div.op == u'Q' and div[0].isChar and div[0].parts in u'𣪊Q𣪊X':
            #print >>sys.stderr , str(i)
            return ['b','ww'] +getOrigRoots(div[1]) +['qx']
        
        elif div.op == u'W' and div[0].isChar and div[0].parts == u'彳' and \
            div[2].isChar and div[2].parts == u'亍':
            return  ['oi'] + getOrigRoots(div[1])   
        elif div.op == u'N' and div[0].isChar and div[0].parts ==u'𣎆':
            return ['sh','j','q']+getOrigRoots(div[1])+['qda']
        elif div.op == u'U' and div[0].isChar and div[0].parts ==u'V舁':
            return ['nb']+getOrigRoots(div[1]) + ['o']
        res = []
        for p in div:        
            res += getOrigRoots(p)        
        return res 

_origOrder = [1,-2,-1]

def origEncode(roots):
    code = roots[0]    
    lCode = len(code)     
    nR = min(len(roots)-1,4-lCode)    
    if nR:        
        rest = _origOrder[3-nR:3]     
        r= ''
        for r in map(lambda i:roots[i],rest):           
            code += r[0]
        tail = r[1:5 - (nR+lCode)]
        code += tail
        
        if nR == 1 and  len(code)==2:
            code +='vv'
    return code

def genOrigZm():
    g=None
    try:
        codes = {}
        for g,i in ids._compounds.iteritems():
            if g not in origRootDic and g not in codes:
                codes[g] = origEncode( getOrigRoots(ids.Ids.parse(i)))
        for g,r in origRootDic.iteritems():
            if len(g)==1 and  g not in codes:
                codes[g] = origEncode(r)
        return codes
    except:
        print >>sys.stderr,g
        raise
if __name__=='__main__':
    readCommonChrs()
    readSpecPhraseCode()
    readRootDic()
    genIme()
        
