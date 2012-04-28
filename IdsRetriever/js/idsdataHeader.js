(function(){
    function loaddata()
    {
        script = document.createElement("script");
        script.setAttribute('type','text/javascript');
        script.setAttribute('src','js/idsdata.js');
        document.body.appendChild(script);
    }
    if(!idsdata)idsdata = {};
    idsdata.version = '0.9.0';    
    if(window.JSON && window.localStorage )
    {
        if( 'idsdata.version' in localStorage)
        {
            var v = localStorage.getItem('idsdata.version');
            if(v == idsdata.version)
            {
                idsdata.compounds = JSON.parse(localStorage.getItem('idsdata.compounds'));                  
                return;
            }
        }
        loaddata();
        localStorage.setItem('idsdata.version',idsdata.version);
        localStorage.setItem('idsdata.compounds',JSON.stringify(idsdata.compounds));
    }
    else
    {
        loaddata();
    }
})();

