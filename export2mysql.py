#!/usr/bin/env python
#-*- coding:utf-8 -*-
import MySQLdb as My
import ids
passwd = None

try:
	passwd = open('secrets/dbpassword').read().strip()
except:
	passwd = "YOUR PASSWORD HERE!"

try:
	#print passwd 
	con = My.connect(host="localhost",db="dict",user="dict",passwd=passwd)
	cur = con.cursor()
	try:
		#populate the compounds table
		cur.execute('''create table if not exists ids_compounds
			(glyph varbinary(8) primary key, 
			formula varbinary(200) not null)''')
		cur.execute('''truncate table ids_compounds''')
		
		compounds = sorted(((k.encode('utf8'),v.encode('utf8')) for k,v in ids._compounds.iteritems()),
			key=lambda ent:ent[0])
		for k,v in compounds:
			cur.execute("insert into ids_compounds values(%s,%s)",(k,v))
		con.commit()
		print "table ids_compounds done!\n"
		#~ 
		#elements
		cur.execute('''create table if not exists ids_elements
			(glyph varbinary(60) primary key)''')
		cur.execute('''truncate table ids_elements''')
		elements = sorted(el.encode('utf8') for el in ids._elements)
		for el in elements:
			cur.execute("insert into ids_elements values(%s)",(el,))
		con.commit()
		print "table ids_elements done!\n"
		
		#form2chars
		cur.execute('''create table if not exists ids_form2chars 
			(formula varbinary(200) primary key, glyphs varbinary(200) not null)''')
		cur.execute('''truncate table ids_form2chars''')
		form2char = sorted(((k.encode('utf8'),v.encode('utf8')) for k,v in ids._ids2char.iteritems()),
			key=lambda ent:ent[0])
		for k,v in form2char:
			cur.execute("insert into ids_form2chars values(%s,%s)",(k,v))
		con.commit()
		print "table form2chars done!\n"
		
		#part2chars
		cur.execute('''create table if not exists ids_part2chars
			(part varbinary(200) primary key, glyphs varbinary(200) not null)''')
		cur.execute('''truncate table ids_part2chars''')
		part2chars = sorted(((k.encode('utf8'),''.join(v).encode('utf8')) for k,v in ids._partsDict.iteritems()),
			key=lambda	ent:ent[0])
		for k,v in part2chars:
			cur.execute("insert into ids_part2chars values(%s,%s)",(k,v))
		con.commit()
		print "table part2chars done!"
		
		print "all done!"
		cur.close()
		con.close()
	except My.Error,e:
		con.rollback()
		print "Error %d: %s" % (e.args[0],e.args[1])
		exit(1)
except My.Error,e:
	
	print "Error %d: %s" % (e.args[0],e.args[1])
	
