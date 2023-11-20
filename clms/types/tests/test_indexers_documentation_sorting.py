"""
Tests indexers on this package
"""
# -*- coding: utf-8 -*-
import datetime
import json
import unittest

from plone import api
from plone.app.testing import SITE_OWNER_NAME, login
from plone.indexer.interfaces import IIndexer
from plone.uuid.interfaces import IUUID
from zope.component import getMultiAdapter

from clms.types.behaviors.dataset_relation import IDataSetRelationMarker
from clms.types.behaviors.product_relation import IProductRelationMarker
from clms.types.content.data_set import IDataSet
from clms.types.content.product import IProduct
from clms.types.content.technical_library import ITechnicalLibrary
from clms.types.indexers.associated_datasets import (
    associated_datasets_behavior,
)
from clms.types.indexers.associated_products import (
    associated_products_behavior,
)
from clms.types.indexers.component_title import component_title_behavior
from clms.types.indexers.custodian_information import custodian_information
from clms.types.indexers.documentation_sorting import documentation_sorting
from clms.types.indexers.geographic_coverage import geographic_coverage
from clms.types.indexers.spatial_resolution import spatial_resolution
from clms.types.indexers.temporal_extent import temporal_extent
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


class TestIndexers(unittest.TestCase):
    """test associated_datasets indexer"""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

        login(self.portal, SITE_OWNER_NAME)
        self.portal_catalog = api.portal.get_tool("portal_catalog")
        self.newsitem1 = api.content.create(
            container=self.portal, type="News Item", id="newsitem1"
        )
        product_components = {
            "items": [
                {
                    "@id": "id-1",
                    "name": "This component",
                    "description": "Component 1 description",
                },
                {
                    "@id": "id-2",
                    "name": "That component",
                    "description": "Component 2 description",
                },
            ]
        }

        api.portal.set_registry_record(
            "clms.types.product_component.product_components",
            json.dumps(product_components),
        )

        self.product = api.content.create(
            container=self.portal,
            type="Product",
            id="product1",
            mapviewer_component="id-1",
        )
        self.product2 = api.content.create(
            container=self.portal,
            type="Product",
            id="product2",
            mapviewer_component="id-2",
        )

        self.dataset = api.content.create(
            container=self.product, type="DataSet", id="dataset1"
        )
        self.document = api.content.create(
            container=self.portal, type="Document", id="document1"
        )
        self.technical_library1 = api.content.create(
            container=self.portal,
            type="TechnicalLibrary",
            id="technical-1",
            technical_library_categorization=["18fdjdprkq"],
        )

        self.technical_library2 = api.content.create(
            container=self.portal,
            type="TechnicalLibrary",
            id="technical-2",
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
        self.assertTrue(ITechnicalLibrary.providedBy(self.technical_library2))
        indexed_value = documentation_sorting(self.technical_library2)
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
