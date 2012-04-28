function test(){
    Idsdata={};
                script = document.createElement("script");
            script.setAttribute('type','text/javascript');
            script.setAttribute('src','js/idsdata.js');
            document.body.appendChild(script);
            console.log('a');
            console.log('b');
    Idsdata.init = function()
    {
       console.log("data loaded!");
    }
};