(function(){
    CharTree = function(ids,parent)
    {
		var me = this;
		this.ids = ids;
        this.jq = $('<dl class="charTree"></dl>');
        this.jq.charTree = this;        
        var cap = $('<dt class="charTreeCap"></dt>');
        this.name = ids.toString();
        this.name = $('<span class="comp">' + this.name +'</span>')
            .dblclick(function(e){me.sendChar();})
            .appendTo(cap);
        cap.appendTo(this.jq);
        
        if(!this.ids.isElement())
        {
            this.toggleBtn = $('<span class="charTreeToggle">[拆分]</span>')
				.click(function(){me.toggle();})
                .appendTo(cap);
            this.open = false;
        }
        else
            this.isElement = true;
        if(parent)this.parent = parent;
    }
    
    CharTree.prototype.toggle=function(open)
    {
		if(this.isElement)return;
        if(open )
        {
			if(!this.open)
			this.toggleBtn.text('[合攏]');
			this.divide();
			this.open = true;
		}
        else
        {
			
			if(!this.open)
			{
				this.toggleBtn.text('[合攏]');
				this.divide();
				this.open = true;
			}
			else
			{
				this.toggleBtn.text('[拆分]');
				this.children.slideUp();
				this.open = false;
			}
		}
    };
    
    CharTree.prototype.sendChar = function(cb)
    {
        if(cb)this.cb = cb;
        else if(this.cb)this.cb(this.name);
    };
    CharTree.prototype.divide = function()
    {
        if(this.isElement)return;
        if(!this.children)
        {
            this.ids = this.ids.divided();
            this.children = $('<dd class="charTreeChildren"><table><tr><td class="op">' +
                              this.ids.op +
                              '</td><td class="compsContainer"></td></tr></table></dd>')
                              .appendTo(this.jq);
            var con = this.children.find('.compsContainer');
            for(var i = 0;i<this.ids.length;i++)
            {
				con.append(new CharTree(this.ids.get(i),this).jq);
			}
        }
        this.children.slideDown();
    }
    IdsUi = function()
    {
		var me = this;
        var tabs = new $ui.Tabs($("#tabs"));
        this.divide = new $ui.Panel($("#divide"));
        this.combine = new $ui.Panel($("#combine"));
        var chTable = $('#charTable');
        var formType = $('#formType');
        var ch,ciStr;
		var cInput = $('#charInput').val('')
			.change(function(){
				//alert(this.value);
                if(this.value && this.value != ciStr)
                {
                    ciStr = this.value;
                    var ids = Ids.parse(this.value);
                    if(ids && ids.toString()!=ch)
                    {
                        ch = ids.toString();
                        $('#charTree').empty().append(new CharTree(ids).jq);
                    }
                }
			});
        var piStr;
        var pInput = $('#partsInput').val('')
            .change(function(){
                if(this.value && this.value != piStr)
                {
                    piStr = this.value;
                    var cl;
                    if(formType.val() == 'ids')
                    {
                        
                        cl = Ids.getCharsByIds(piStr);
                    }
                    else
                    {
                        cl = Ids.getCharsByParts(piStr);
                    }
                    chTable.empty();
                    _.each(cl,function(c){chTable.append($('<span class="ch">'+c +'</span>'));});
                }
            });
        
    };
    
    $(function(){
        initIds(function(){			
            ui = new IdsUi;
			//$("#splitter").splitter({dock:true,outline:true});
            
            
        });        
    });
    
})();
