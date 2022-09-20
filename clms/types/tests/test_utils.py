""" test some utilities"""

import unittest

from clms.types.restapi.mapviewer_service.lrf_get import clean_component_title


class TestUtils(unittest.TestCase):
    """ test case"""

    def test_clean_component_title_with_hash(self):
        """ test the clean_component_title function """
        value = clean_component_title("01#This is my title")
        self.assertEqual(value, "This is my title")


    def test_clean_component_title_without_hash_number(self):
        """ if we use it without a #, it will return the original"""
        value = clean_component_title("This is my title")
        self.assertEqual(value, "This is my title")
