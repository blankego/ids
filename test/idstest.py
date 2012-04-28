#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
sys.path.append('..')
from ids import Ids

class TestIds(unittest.TestCase):
    def setUp(self):
        self.s = "H石Z艹H氵Z甫寸"
        self.c = u'礴'
        self.s1 = 'QQ鳥X几'
        self.c1 = u'鳬'
    def test_ids_parse(self):
       
        i = Ids.parse(self.s)
        self.assertEqual(self.c,i.chrForm)
        self.assertFalse(i.isChar)
        self.assertFalse(i.isElement)
        
        i1 = Ids.parse(self.s1)
        self.assertEqual(self.c1,i1.chrForm)
        
    
    def test_char(self):
        i = Ids.parse(self.c)
        self.assertEqual(self.s, str(i.elaborate()))
        self.assert_(i.isElaborated)
        self.assertEqual(self.c,i.synthesize().chrForm)
        self.assertFalse(i.isElaborated)
        self.assert_('氵' in i)
    
    def test_gouged_char_parse(t):
        pass

if __name__=='__main__':
    unittest.main()
