"""
Tests indexers on this package
"""
# -*- coding: utf-8 -*-
import json
import unittest

from plone import api
from plone.app.testing import SITE_OWNER_NAME, login
from plone.indexer.interfaces import IIndexer
from zope.component import getMultiAdapter

from clms.types.content.technical_library import ITechnicalLibrary
from clms.types.indexers.documentation_sorting import documentation_sorting
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


# Some constants to easily assign categories
# These are default values coming from the default
# categories, loaded to Plone when the package is installed.
# Check profiles/default/taxonomies/technical_library_categorization
# Keep in mind that when the sub-category is selected, the value of the
# main category is also assigned to the item
CATEGORY_01 = "18fdjdprkq"
CATEGORY_01_01 = "pvwxi0tmyr"
CATEGORY_01_02 = "cvlh7ur10y"
CATEGORY_01_03 = "p35b7fh1ng"
CATEGORY_01_04 = "qbbdaeny9r"

CATEGORY_02 = "x0ho7are9n"
CATEGORY_02_01 = "i2223921k5"
CATEGORY_02_02 = "3awub96pqx"
CATEGORY_02_03 = "obvwrtdeqx"
CATEGORY_02_04 = "0xs7rsp6cw"

CATEGORY_03 = "63qwxkfcrx"
CATEGORY_03_01 = "c5ifc5oxei"
CATEGORY_03_02 = "6o561w24t7"
CATEGORY_03_03 = "xfh4funakh"
CATEGORY_03_04 = "33tmub0shd"
CATEGORY_03_05 = "ee0iurm8uh"
CATEGORY_03_06 = "gtcg0dlku6"

CATEGORY_05 = "bbbnmxu54oq9q"


class TestIndexers(unittest.TestCase):
    """test associated_datasets indexer"""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

        login(self.portal, SITE_OWNER_NAME)
        self.portal_catalog = api.portal.get_tool("portal_catalog")

        self.document = api.content.create(
            container=self.portal, type="Document", id="document1"
        )

        self.technical_library1 = api.content.create(
            container=self.portal,
            type="TechnicalLibrary",
            id="technical-1",
            taxonomy_technical_library_categorization=[
                CATEGORY_01,
                CATEGORY_01_01,
            ],
        )

        self.technical_library2 = api.content.create(
            container=self.portal,
            type="TechnicalLibrary",
            id="technical-2",
            taxonomy_technical_library_categorization=[
                CATEGORY_01,
                CATEGORY_01_02,
            ],
        )

        self.technical_library3 = api.content.create(
            container=self.portal,
            type="TechnicalLibrary",
            id="technical-3",
            taxonomy_technical_library_categorization=[
                CATEGORY_02,
                CATEGORY_02_01,
                CATEGORY_02_04,
            ],
        )

        self.technical_library4 = api.content.create(
            container=self.portal,
            type="TechnicalLibrary",
            id="technical-4",
            taxonomy_technical_library_categorization=[
                CATEGORY_01,
                CATEGORY_01_03,
                CATEGORY_02,
                CATEGORY_02_01,
            ],
        )

        self.technical_library5 = api.content.create(
            container=self.portal,
            type="TechnicalLibrary",
            id="technical-5",
            taxonomy_technical_library_categorization=[],
        )

        self.technical_library6 = api.content.create(
            container=self.portal,
            type="TechnicalLibrary",
            id="technical-6",
            taxonomy_technical_library_categorization=[CATEGORY_02],
        )

        self.technical_library7 = api.content.create(
            container=self.portal,
            type="TechnicalLibrary",
            id="technical-7",
            taxonomy_technical_library_categorization=[CATEGORY_05],
        )

    def test_documentation_sorting_indexer(self):
        """test the documentation sorting indexer in a Technical Library"""
        self.assertTrue(ITechnicalLibrary.providedBy(self.technical_library1))
        indexed_value = documentation_sorting(self.technical_library1)

        self.assertTrue(isinstance(indexed_value(), int))

    def test_documentation_sorting_indexer_adapter(self):
        """test the adapter"""
        self.assertTrue(ITechnicalLibrary.providedBy(self.technical_library1))

        adapter = getMultiAdapter(
            (self.technical_library1, self.portal_catalog),
            interface=IIndexer,
            name="documentation_sorting",
        )
        indexed_value = adapter()
        self.assertTrue(isinstance(indexed_value, int))

    def test_documentation_sorting_indexer_empty_field_value(self):
        """test the indexer when the field is empty"""
        self.assertTrue(ITechnicalLibrary.providedBy(self.technical_library5))
        indexed_value = documentation_sorting(self.technical_library5)
        self.assertTrue(isinstance(indexed_value(), int))

    def test_documentation_sorting_indexer_elsewere(self):
        """test in some other object type"""
        self.assertFalse(ITechnicalLibrary.providedBy(self.document))

        adapter = getMultiAdapter(
            (self.document, self.portal_catalog),
            interface=IIndexer,
            name="documentation_sorting",
        )
        self.assertRaises(AttributeError, adapter)

    def test_documentation_sorting_ordering_all(self):
        """test some orderings according to the values set in the
        technical library documents
        """
        value_1 = documentation_sorting(self.technical_library1)()
        value_2 = documentation_sorting(self.technical_library2)()
        value_3 = documentation_sorting(self.technical_library3)()
        value_4 = documentation_sorting(self.technical_library4)()

        items = [value_1, value_2, value_4, value_3]
        self.assertEqual(items, sorted(items))

    def test_documentation_sorting_ordering_same_category(self):
        """test some orderings according to the values set in the
        technical library documents
        """
        value_1 = documentation_sorting(self.technical_library1)()
        value_2 = documentation_sorting(self.technical_library2)()

        items = [value_1, value_2]
        self.assertEqual(items, sorted(items))

    def test_documentation_sorting_only_category(self):
        """test that when having just one category, the item goes
        as the last item in the same category
        """
        value_4 = documentation_sorting(self.technical_library4)()
        value_6 = documentation_sorting(self.technical_library6)()

        items = [value_4, value_6]
        self.assertEqual(items, sorted(items))

    def test_documentation_sorting_unnumbered_category(self):
        """test that when a category that doesn't have a number
        in its name, the item is indexed as a last value
        """
        value_4 = documentation_sorting(self.technical_library4)()
        value_7 = documentation_sorting(self.technical_library7)()
        self.assertTrue(isinstance(value_7, int))
        items = [value_4, value_7]
        self.assertEqual(items, sorted(items))
