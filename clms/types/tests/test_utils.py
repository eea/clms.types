""" test some utilities"""

import unittest

from clms.types.restapi.mapviewer_service.lrf_get import clean_component_title, has_items


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

    def test_has_items_empty(self):
        """ with an empty value is False"""
        self.assertEqual(has_items({}), False)

    def test_has_items_empty_items_key(self):
        """with an empty value is False"""
        self.assertEqual(has_items({'items': []}), False)

    def test_has_items_single_item_without_path(self):
        """with an empty value is False"""
        self.assertEqual(has_items({"items": [{"title": "some title"}]}), False)

    def test_has_items_single_item_with_path(self):
        """ This should be True """
        self.assertEqual(
            has_items({"items": [{"title": "some title", "path": "/some_path"}]}), True
        )

    def test_has_items_multiple_values_without_path(self):
        """ This should be False """
        self.assertEqual(
            has_items(
                {"items": [{"title": "some title"}, {"title": "some other title"}]}
            ),
            False,
        )

    def test_has_items_multiple_values_with_path(self):
        """ This should be True """
        self.assertEqual(
            has_items(
                {
                    "items": [
                        {"title": "some title", "path": "/some_path/here"},
                        {"title": "some other title", "path": "/some_path/other/here"},
                    ]
                }
            ),
            True,
        )

    def test_has_items_multiple_values_with_and_without_path(self):
        """ This should be True """
        self.assertEqual(
            has_items(
                {
                    "items": [
                        {"title": "some title"},
                        {
                            "title": "some other title",
                            "path": "/some_path/other/here",
                        },
                    ]
                }
            ),
            True,
        )
