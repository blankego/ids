#!/usr/bin/env python
import ids
def enc(tup):
	return tuple(map(lambda s:s.encode('utf8'),tup))
print "BEGIN TRANSACTION;"
print  "DELETE FROM ids_comp;"
for ent in sorted(((c,f) for c,f in ids._compounds.iteritems()),key=lambda tup:tup[0]):
	print "INSERT INTO ids_comp VALUES('%s','%s');" % enc(ent)
	
print "DELETE FROM ids_element;"
for el in sorted(iter(ids._elements)):
	print "INSERT INTO ids_element VALUES('%s');" % el.encode('utf8')

print "DELETE FROM ids_part;"
for k,v in sorted(((p,cs) for p,cs in ids._partsDict.iteritems()),key=lambda tup:tup[0]):
	print "INSERT INTO ids_part VALUES('%s','%s');"%(k.encode('utf8'),''.join(v).encode('utf8'))

print "COMMIT TRANSACTION;"