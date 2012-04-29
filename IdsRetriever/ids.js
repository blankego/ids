function initIds(cb){
    
    if(window.Idsdata === undefined)Idsdata = {};
    if(window.cjk == undefined)cjk = {};
    
    Idsdata.version = '0.9.1'; 
    var _operators = {'H':2,'W':3,'Z':2,'E':3,'O':2,'P':2,'Q':2,
    'L':2,'N':2,'U':2,'C':2,'D':2,'V':1,'F':1,'X':null};
    
    (function IdsClass(){
        Ids = function(op,parts)
        {
            this.op = op;
            this.parts = parts;
            this.length = op? parts.length: 1;
        };
        Ids.lop2op = {'H':'⿰','W':'⿲','Z':'⿱','E':'⿳','O':'⿴','P':'⿸','Q':'⿹',
            'L':'⿺','N':'⿵','U':'⿶','C':'⿷','D':'⿻','V':'異','F':'調','X':'切'};
        Ids.op2lop =  {'⿰':'H','⿲':'W','⿱':'Z','⿳':'E','⿴':'O','⿸':'P','⿹':'Q',
            '⿺':'L','⿵':'N','⿶':'U','⿷':'C','⿻':'D','異':'V','調':'F','切':'X'};
        Ids.prototype.get = function(idx)
        {
            if(!this.isChar())
                return this.parts[idx];
            else if(idx == 0 || idx == -1)
                return this;
            else
                return undefined;
        };
        
        Ids.prototype.isChar = function(){ return this.op === null;};
        
        Ids.prototype.isElement = function()
        {
            if(!this.isChar())return false;
            else
            {
                var init = this.parts[0];
                if(init >'B' && init <= 'Z')return true; //letter
                else
                    return this.parts in Idsdata.elements;
            }
        };
        
        Ids.prototype.chrForm = function()
        {
            if(this.isChar())return this.parts;
            else
            {
                var parts = this.op;
                for(var i = 0;i< this.parts.length;i++)parts += this.parts[i].chrForm();
                return Idsdata.ids2char[parts];
            }
        };
        
        Ids.prototype.divided = function()
        {
            if(!this.isChar() || this.isElement())
                return this;
            else
                return Ids.parse(Idsdata.compounds[this.parts]);
        };
        
        Ids.prototype.children = function()
        {
            if(this.isElement())
                return [];
            else
            {
                if(this.isChar())
                    return Ids.parse(Idsdata.compounds[this.parts]).children();
                else
                    return this.parts;
            }
        };
        Ids.prototype.toString = function()
        {
            if(!this.op)return this.parts;
            var res = this.op;
            for(var i=0;i<this.length;i++)
                res += this.parts[i].toString();
            return res;
        }
    })();
    
    
    cjk.str2CharList = function(s)
    {
        res = [];
        if(!s.substr)return s;
        
        //const  L = 0x4dff, R = 0x9fa6;
        //const  LA = 0x33ff, RA = 0x4db6;
        //const  LB = 0x1ffff, RB = 0x2a6d7;
        const  SURROGATEHL = 0xd7ff, SURROGATEHR = 0xdc00;
        const  SURROGATELL = 0xdbff, SURROGATELR = 0xe000;
        
        for(i= 0;i < s.length;++i)
        {
            var c = s.charCodeAt(i);
            var dic = null;				
            if (c > SURROGATEHL && c < SURROGATEHR && ++i)
            {
                var c2 = s.charCodeAt(i);
                if (c2 > SURROGATELL && c2 < SURROGATELR)
                {
                    res.push(String.fromCharCode(c,c2));
                }
                else
                    res.push(String.fromCharCode(c));//invalid char
            }
            else
                res.push(String.fromCharCode(c));
                
        }
        return res;
    };
    (function CharQueueClass(){
        cjk.CharQueue = function(cl)
        {
            this.s = cl.substr? cjk.str2CharList(cl) : cl;
            this.s.idx = -1;
            this.seq = this.s;        
        };
        
        cjk.CharQueue.prototype.reset = function()
        {
            this.seq.idx = -1;
        };
        
        cjk.CharQueue.prototype.next = function()
        {        
            this.seq.idx++;
            if(this.seq.idx >= this.seq.length)
            {
                if(this.seq !== this.s)
                {
                    this.seq = this.s;
                    return this.next();
                }
                throw RangeError();           
            }
            return this.seq[this.seq.idx];
        };
        
        cjk.CharQueue.prototype.unshift = function(head)
        {
            head.idx = -1;
            this.seq = head;        
        };
        cjk.CharQueue.prototype.toString = function()
        {
            var res = this.seq.join('');
            return this.seq != this.s ? res + this.s.join('') : res;
        }
        
    })();
 
    
    Ids.parse = function(code, isCharQueue)
    {
        try
        {
            var form = isCharQueue ? code : new cjk.CharQueue(code);
            init = form.next();
            initCode = init.charCodeAt(0);
            if(initCode == 86 || initCode == 70)//V or F
                return new Ids(null,init + form.next());
            else
            {
                var nEl = _operators[init];
                if(nEl != undefined)
                {
                    if(nEl == 2)
                    {
                        var c1 = form.next();
                        var c2 = form.next();
                        //check if it's a gouged char such as 'Q鳥X'
                        if(c1 == 'X' && c2 >= "\u3400" ||
                           c2 == 'X' && c1 >= "\u3400")
                        {
                            return new Ids(null,init + c1 + c2);
                        }
                        else
                        {
                            form.unshift([c1,c2]);
                        }
                    }
                    
                    
                    //normal compound
                    var op = init;
                    var parts = [];
                    for(var j=0;j < nEl;j++)
                    {
                        
                        parts.push(Ids.parse(form,true));
                       
                    }
                    return new Ids(op,parts);
                }
                else //unknown lever char
                {
                    //console.log('parsing:', init)
                    return new Ids(null,init);
                }
            }
     
        }
        catch(e)// if e instanceof RangeError)
        {
            //alert("Ill formed ids: " + form);
            return undefined;
        }
    };
    
    Ids.getCharsByIds = function(i)
    {
        i = Ids.parse(i);
        if(!i)return [];
        var chs = i.chrForm();
        return chs? cjk.str2CharList(chs).sort() : [];   
    };
    
    Ids.getCharsByParts = function()
    {
        var res = [];
        var argc = arguments.length;
        if(argc == 0)return res;
            
        var ps = argc == 1 ?
                _.isArray(arguments[0])?
                arguments[0]:
                ps = arguments[0].split(/ +|, */):
            arguments;
        
        
        _.each(ps,function(p){
            var chs = Idsdata.parts[p];
            if(chs)
            {
                chs = cjk.str2CharList(chs);
                if(res.length == 0)res = chs;
                else res = _.intersection(res,chs);
            }
        });
        return res.sort();
    };
    //init
    Idsdata.init = function()
    {
        var els = cjk.str2CharList(Idsdata.elements);
        Idsdata.elements={};
        for(var i=0;i<els.length;i++)
            Idsdata.elements[els[i]] = true;
        
       /* if(window.localStorage && window.JSON)
        {
            localStorage.setItem('Idsdata.version',Idsdata.version);
            localStorage.setItem('Idsdata.compounds',JSON.stringify(Idsdata.compounds));
            localStorage.setItem('Idsdata.elements',JSON.stringify(Idsdata.elements));
            localStorage.setItem('Idsdata.parts',JSON.stringify(Idsdata.parts));
        }*/
        Idsdata.init2();
    };
    Idsdata.init2 = function()
    {
        Idsdata.ids2char={};
        for(var k in Idsdata.compounds)
        {
            var form = Idsdata.compounds[k];
            var g = Idsdata.ids2char[form];
            Idsdata.ids2char[form] = g ? g + k : k;
        }
        if(cb)cb();
    };
    
    (function DoInitStuff(){
        Idsdata.init();
       /* function loadData()
        {
            var script = document.createElement("script");
            script.setAttribute('type','text/javascript');
            script.setAttribute('charset','UTF-8');
            script.setAttribute('src','js/idsdata.js');
            document.body.appendChild(script);
            
        }
        
           
        if(window.JSON && window.localStorage )
        {
            if( 'Idsdata.version' in localStorage)
            {
                var v = localStorage.getItem('Idsdata.version');
                if(v == Idsdata.version)
                {
                    Idsdata.compounds = JSON.parse(localStorage.getItem('Idsdata.compounds'));
                    Idsdata.elements = JSON.parse(localStorage.getItem('Idsdata.elements'));
                    Idsdata.parts = JSON.parse(localStorage.getItem('Idsdata.parts'));
                    Idsdata.init2();
                    return;
                }
            }
            loadData();
            
            
        }
        else
        {
            loadData();
        }*/
    })();

};