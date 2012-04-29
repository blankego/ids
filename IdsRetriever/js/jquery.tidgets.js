(function($){
//IE8 is brainfucked, It doesn't even allow the prop test!!

//support DnD;
jQuery.event.props.push("dataTransfer");

//tSplitter
var MIN_HEIGHT = 80;
$.fn.tSplitter = function(options){
	
	var opt = $.extend({
		belongsTo:'left'
		,leftWidth:'30%'
		,withToggle:true
		//,height:'auto'
	},options);
	
	return this.each(function(){			
		var box = $(this).filter('div')
		var panes = box.children();
		if(panes.length !== 2)return;
		box.addClass('tSplitBox');
		
		
		var l =$('<div/>').append(panes.eq(0)).addClass('tSplitLeft').appendTo(box).css('width',opt.leftWidth);
		var	r =$('<div/>').append(panes.eq(1)).addClass('tSplitRight').appendTo(box).css('left',opt.leftWidth);
		//$('<div style="position:static;height:100%;"/>').append(l).append(r).appendTo(box);
		var	sp = $('<div class="tSplitter" unselectable="on"/>')				
				.addClass(opt.belongsTo)
				.css('left',opt.leftWidth)
				.insertAfter(l);
		var collapsable = opt.belongsTo === 'left'?l:r;
		function setHeight(h)
		{
			box.height(h);
			sp.height(h);
			l.height(h);
			r.height(h);	
		}
		if(opt.height)
		{
			if(opt.height==='auto')
			{
				var oldH;
				setInterval(function(){
					var lH = panes.eq(0).outerHeight(),
						rH = panes.eq(1).outerHeight();				
					var h = (lH > rH? lH: rH)+20;
					if(h < MIN_HEIGHT)h = MIN_HEIGHT;
					if(h !== oldH)
					{
						oldH = h;
						setHeight(h);
					}
					
				},300);
				
			}else
			{
				setHeight(opt.height);
			}
		}
		else
		{
			
		}
		
		//Add toggle button
		var collapsed = false;
		if(opt.withToggle)
		{
			function toggle(e)
			{
				var x;
				if(!( x=sp.data('x')))
				{
					
					sp.data('x',sp.position().left)
						.css('left',collapsable===l ? 0: box.innerWidth()-sp.outerWidth());
					collapsable.hide();
					collapsed = true;
				}
				else
				{
					sp.data('x','')
						.css('left',x);					
					collapsable.show();
					collapsed = false;
				}
				resize();
				e.stopPropagation();
			}
			$('<button class="tSplitToggle"></button>')
				.addClass(opt.belongsTo)
				.appendTo(sp)			
				.click(toggle);
			sp.dblclick(toggle);
		}
		
		//resize both panes after drag is done or the mouse cursor moved out of the box area
		function resize()
		{
			var x = sp.position().left;
			sp.removeClass('dragging');			
			r.css('left',x);
			l.width(x);
			
			box.off('mousemove',drag);
			sp.add(window).off('mouseup',resize);			
		}
		var oldX, spX;
		function drag(e)
		{
			
			var currX = e.pageX;
			var diff = currX-oldX;
			if(Math.abs(diff)>2)
			{
				var boxWidth = box.innerWidth();
				var _spX = spX + diff;
				if(_spX >= 0  && _spX <= boxWidth)
				{
					sp.css('left',_spX)					
					oldX = currX;
					spX = _spX;
				}
				else
					resize();						
			}					
		}
		function startDrag(e)
		{
			if(collapsed)return;
			oldX = e.pageX;
			//currX = oldX;
			spX = sp.position().left;				
			sp.addClass('dragging')
				.add(window).mouseup(resize);
			box.mousemove(drag);
		}
		sp.on('mousedown',startDrag);		
	});		
};

//tTree

$.fn.tTree = function(options)
{
	options = $.extend({
		target:null
		,open:null
		,scroll:false 
	},options);
	var openAll = options.open === 'all';
	function addToggle(li)
	{
		var fst = li.firstChild;
		if(!fst)return;
		
		var a,url,href;
		
		switch(fst.nodeType)
		{
		case 1:
			if(fst.className.indexOf('tTreeToggle') >= 0)return;
			a    = fst;
			url  = fst.getAttribute('url');
			href = fst.getAttribute('href');
			break;
		case 3:
			a = li.insertBefore(document.createElement('a'),fst);
			a.appendChild(fst);
			break;
		default:return;
		}
		
		
		if(options.target && href)
		{
			var targ = options.target;
			$(a).click(function(e){
				e.preventDefault();
				var isStr = targ.substr;				
				$.get(href,isStr? function(data){
					$(targ).html(data);
				}:targ);
				return false;				
			});				
		}
		var ul = a.nextSibling;		
		while(ul && (ul.nodeType!==1 || ul.tagName !=='UL'))ul = ul.nextSibling;
		
		//create toggle button
		if(ul || url)
		{
			var btn = li.insertBefore(document.createElement('span'),a);
			btn.className = 'tTreeToggle';				
			btn.onclick = function(){toggle.call(btn)};
			var toOpen = openAll? true: ( li.className.indexOf('open') >= 0);
			toggle.call(btn,toOpen);
		}
	
		
		
	}
	
	function addChildren (ul)
	{
		if(!ul.className || ul.className.indexOf('tTreeChildren') < 0)
		{
			var nodes = ul.childNodes;
			for(var i=0;i<nodes.length;i++)
			{
				var n = nodes[i];
				if(n.nodeType === 1 && n.tagName === 'LI')
					addToggle(n);
			}	
			ul.className += ' tTreeChildren';
		}
	}
	function toggle(toOpen,cb)
	{
		var li = $(this.parentNode);
		var ch = li.children('ul').first();
		var noUl=false;
		if(!ch.length)
		{
			noUl=true;
			ch = li.children('span.tTreeToggle+a~*');
		}
		toOpen = (toOpen === true || toOpen === false)? toOpen : !li.hasClass('open') ;
		
		if(toOpen)
		{					
			if(noUl && !ch.length)
			{				
				var me = this;
				var url = li.children('a').attr('url');
				//console.log(this,li,url);
				$.get(url,function(data){
					li.append(data);
					toggle.call(me,true,cb);
				});
				return this;				
			}
			this.innerHTML = '⊟';	
			li.addClass('open');
			if(!noUl && !ch.hasClass('tTreeChildren'))addChildren(ch[0]);
			ch.show();
			
		}
		else
		{
			this.innerHTML = '⊞';
			li.removeClass('open');
			ch.hide();
		}
		if(cb)cb();
		return this;
	}
	
	
	return this.each(function(){
		
		var tree = $(this).filter('ul');
		if(!tree.length)return;
		if(!tree.hasClass('tTree'))
		{
			tree.addClass('tTree');		
			var ch = tree.children('li').each(function(){addToggle(this);});
		}
		if(options.open && $.isArray(options.open))//TODO: openAll
		{
			
			var path = options.open.slice();
			var subTree, i, node, btn;
			//It should be an array of path like [1,2,3];
			function openNode()
			{
				if(!(subTree = node?node.children('ul').first():tree).length)return;
				if((i = path.shift()) !== undefined &&
					(node = subTree.children().eq(i)).length &&				
					(btn = node.children('span.tTreeToggle').first()[0]))				
						toggle.call(btn,true,openNode);
				else if(node.length && options.scroll)
				{
					(i==0?(node.parent().parent()):node.prev())[0].scrollIntoView();
				}
			};
			openNode();
			
		}		
	});
};
//---------------tTabs--------------------------
$.fn.tTabs = function(options)
{
	var opt = $.extend({
		showHeader:false,
		select:0
	},options);
	
	function selectTab(t)
	{
		if(t.hasClass('selected'))return;
		t.eq(0).removeClass('unselected').addClass('selected');
		var panel = t.parent('ul').nextAll('div').hide().eq(t.index());
		var url = t.attr('url');		
		if(url && !t.hasClass('loaded'))
		{
			$.get(url,function(data){ panel.html(data);});
			t.addClass('loaded');
		}
		panel.show();
		t.siblings().removeClass('selected').addClass('unselected');		
	}
	
	return this.each(function(){
		var con = $(this);
		var nav = con.children('ul:first-child');		
		
		if(nav.length)
		{
			var tabs = nav.children('li').addClass('tTabs-tab');
			con.addClass('tTabs');
			nav.addClass('tTabs-nav');
			var panels = con.children('div').addClass('tTabs-panel');
			if(!opt.showHeader)nav.addClass('hidden');
			tabs.each(function(i,el){				
					$(this).click(function(){
						selectTab($(this));						
					});
				});
		 	selectTab( tabs.eq(opt.select));
			
		}
		
	});
}

//-----------------tPopup--------------------
$.fn.tPopup = function(opts)
{
	return this.each(function(){
		//construct
		var box = $(this);
		var cap = box.children('a:first-child');
		if(!cap.length)return;
		var url = cap.attr('url');
		var help = cap.next('div').addClass('tPopup-description');
		var poppy = help.next('div')
						.addClass('tPopup-content')
						.mouseleave(function(){	$(this).removeClass('show');});
		var helpBtn = $('<a class="tPopup-help">？</a>')
						.click(function(){help.toggleClass('show');poppy.removeClass('show');});
		var inp = $('<input type="text" class="tPopup-input"/>');
		cap = $('<div class="tPopup-header"></div>').append(cap).append(inp).append(helpBtn);
		box.addClass('tPopup').prepend(cap);
		
		//pop
		function showPoppy(){poppy.addClass('show');help.removeClass('show');}
		var lastVal = null;
		function popup(e)
		{
			e.preventDefault();
			if(e.dataTransfer)this.value = e.dataTransfer.getData('Text');
			var v = inp.val();
			if(url && v && v!==lastVal)
			{//retrieve data
				poppy.html('<br/>Loading...<br/><br/><br/>')
				$.get(url+'/'+$.trim(v), function(data){poppy.html(data);});
				lastVal = v;
			}
			poppy.addClass('show');            
			return false;
		}
		
		//inp events
		inp.keydown(function(e){
			if(e.which===13)
			{
				e.preventDefault();
				popup.call(inp[0],e);
			}
		}).on('dragover dragenter',function(e){
			inp.val('...');            
			return false;
		}).on("change drop",popup)
		.dblclick(function(){
			poppy.toggleClass('show');
		});
			
		
	});
	
};

})(jQuery);