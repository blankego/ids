$(function(){
module("Ids ");
test("hello",function(){equals(1,1);});
initIds(function(){
    test("test str2CharList",function(){
        var s="𣒏|H木𠦑|𣒒|W木文阝|";
        var cl = cjk.str2CharList(s);
        equals(cl.length,13);
        equals(cl[1],'|');
        equals(cl[4],'𠦑');
    });
    
    test("test charQueue",function(){
       var s = "H木𠦑|";
       var cq = new cjk.CharQueue(s);
       equals(cq.next(),'H');
       equals(cq.next(),'木');
       equals(cq.next(),'𠦑');
       cq.reset();
       equals(cq.next(),'H');
       cq.unshift(['X']);
       equals(cq.next(),"X");
       equals(cq.next(),'木');
       cq = new cjk.CharQueue('H日月');
       equals(cq.next(),'H');
       equals(cq.next(),'日');
       equals(cq.next(),'月');
       raises(function(){ cq.next();},RangeError);
    });
    //test("dummy",function(){
    //    var dc ={a:'a',b:'b',c:'c'};
    //    var dn={97:'a',98:'b',99:'c'};
    //    var z;
    //   var start = new Date().getTime();
    //   
    //   for(var i=0;i<1000000;i++)
    //     z = dc['c'];
    //    console.log(new Date().getTime()-start,z);
    //     start = new Date().getTime();
    //    for(var i=0;i<1000000;i++)
    //     z = dn[99];
    //    console.log(new Date().getTime()-start,z);
    //});
    
    test("test parser", function() {
        
      equals(Ids.parse('H日月').length,2);
      
    });
    test("test Ids",function(){
       var i = Ids.parse('H日月');
       console.log(i);
       equals(i.toString(),'H日月');
       equals(i.op,'H');
       
       
       ok(!i.isChar());
       ok(!i.isElement());
       var s= 'H木HX佩';
       i= Ids.parse(s);
       equals(i.length,2);
       ok(i.get(1).isElement());
       ok(i.get(1).isChar());
       ok(i.divided(),i);
       ok(Ids.parse('一').isElement());
       i = Ids.parse('礡');
       equals(i.divided().get(1).divided().get(1).divided().get(1).toString(),'寸');
    });
    test("test get chars by parts",function(){
        
        var res = Ids.getCharsByParts('甬','广');
        console.log(res);
       deepEqual(res,['𣘋','𨪞']);
       deepEqual(Ids.getCharsByParts(['甬','广']),['𣘋','𨪞']);
       deepEqual(Ids.getCharsByParts("扌 一,几"),['𢪁']);
    });
    test("test get chars by IDS",function(){
        var i = 'E彑冖果';
        deepEqual(Ids.getCharsByIds(i),['彙','𢑥']);
    });
});


});