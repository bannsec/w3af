'''
test_vuln.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
import unittest

from nose.plugins.attrib import attr

from core.data.kb.vuln import Vuln
from core.data.parsers.url import URL
from core.data.request.fuzzable_request import FuzzableRequest
from core.data.dc.data_container import DataContainer
from core.data.fuzzer.mutants.mutant import Mutant


class MockVuln(Vuln):
    def __init__(self):
        desc = 'desc ' * 10
        super(MockVuln, self).__init__('TestCase', desc, 'High', 1, 'plugin_name')

@attr('smoke')
class TestVuln(unittest.TestCase):
    
    def test_from_vuln(self):
        url = URL('http://moth/')
        
        inst1 = MockVuln()
        inst1.set_uri(url)
        inst1['eggs'] = 'spam'
        
        inst2 = Vuln.from_vuln(inst1)
        
        self.assertNotEqual(id(inst1), id(inst2))
        self.assertIsInstance(inst2, Vuln)
        
        self.assertEqual(inst1.get_uri(), inst2.get_uri())
        self.assertEqual(inst1.get_uri(), url)
        self.assertEqual(inst2.get_uri(), url)
        self.assertEqual(inst2['eggs'], 'spam')
        self.assertEqual(inst1.get_url(), inst2.get_url())
        self.assertEqual(inst1.get_method(), inst2.get_method())
        self.assertEqual(inst1.get_dc(), inst2.get_dc())
        self.assertEqual(inst1.get_var(), inst2.get_var())
        self.assertEqual(inst1.get_to_highlight(), inst2.get_to_highlight())

    def test_from_mutant(self):
        dc = DataContainer()
        url = URL('http://moth/')
        payloads = ['abc', 'def']

        dc['a'] = ['1', ]
        dc['b'] = ['2', ]
        freq = FuzzableRequest(url, dc=dc)
        fuzzer_config = {}
        
        created_mutants = Mutant.create_mutants(freq, payloads, [], False,
                                                fuzzer_config)
                
        mutant = created_mutants[0]
        
        inst = Vuln.from_mutant('TestCase', 'desc' * 30, 'High', 1,
                                'plugin_name', mutant)
        
        self.assertIsInstance(inst, Vuln)
        
        self.assertEqual(inst.get_uri(), mutant.get_uri())
        self.assertEqual(inst.get_url(), mutant.get_url())
        self.assertEqual(inst.get_method(), mutant.get_method())
        self.assertEqual(inst.get_dc(), mutant.get_dc())
        self.assertEqual(inst.get_var(), mutant.get_var())
    