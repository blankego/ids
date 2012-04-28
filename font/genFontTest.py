#!/usr/bin/env python
#-*- coding: utf-8 -*-
idsop = {   "H":"⿰","Z":"⿱","W":"⿲","E":"⿳","O":"⿴","P":"⿸","Q":"⿹",
            "L":"⿺","C":"⿷","N":"⿵","U":"⿶","D":"⿻","F":"調","V":"異","X":"切"}
import re
sub = re.compile(r'[A-Z]')
replace = lambda m:idsop[m.group(0)]
header = """
<html>
<head>
<title> IDSComps Font Presentation</title>
<style type="text/css">
body{font-size:1.5em}
@font-face {
font-family: "IDSComps";
src: url("IDSComps.ttf") format("truetype");

} 

@font-face{
font-family:"test";
src:url("test.ttf") format("truetype")
}
.ids{
    font: 2em "IDSComps";
    border:  solid 1px green;
}

</style>
</head>
<body>
<p>
"""
trailer = "</p></body></html>"
fo = open("fonttest.html",'w')
fo.write(header)
for l in open('../output/variants.txt'):
    com,demo = l.strip().split()
    form = sub.sub(replace,com)
    print >> fo,'<span class="ids">'+form + "</span>" , com,demo,"<br/>"
print >>fo,trailer 
fo.flush()
