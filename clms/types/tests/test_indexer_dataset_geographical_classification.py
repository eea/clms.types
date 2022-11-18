"""
tests for the dataset_geographical_classification indexers
"""
# -*- coding: utf-8 -*-

import json
import unittest


from plone import api
from plone.app.testing import SITE_OWNER_NAME, login
from plone.indexer.interfaces import IIndexer
from zope.component import getMultiAdapter

from clms.types.content.data_set import IDataSet
from clms.types.indexers.dataset_geographical_classification import (
    is_eea,
    is_northern_hemisphere,
    is_southern_hemisphere,
    classify_bounding_boxes,
    dataset_geographical_classification,
    expand_bounding_box,
)
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


class TestAssociatedDatasetsIndexer(unittest.TestCase):
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
            container=self.product,
            type="DataSet",
            id="dataset1",
            geographicBoundingBox={
                "@items": [
                    {
                        "north": "",
                        "south": "",
                        "east": "",
                        "west": "",
                    },
                ]
            },
        )

        self.document = api.content.create(
            container=self.portal, type="Document", id="document1"
        )

    def test_dataset_geographical_classification(self):
        """test the indexer in a dataset"""
        self.assertTrue(IDataSet.providedBy(self.dataset))
        indexed_value = dataset_geographical_classification(self.dataset)
        # pylint: disable=not-callable
        self.assertTrue(isinstance(indexed_value(), list))

    def test_dataset_geographical_classification_adapter(self):
        """test the adapter"""
        self.assertTrue(IDataSet.providedBy(self.dataset))

        adapter = getMultiAdapter(
            (self.dataset, self.portal_catalog),
            interface=IIndexer,
            name="dataset_geographical_classification",
        )
        indexed_value = adapter()
        self.assertTrue(isinstance(indexed_value, list))

    def test_dataset_geographical_classification_elsewere(self):
        """test in some other object type"""
        self.assertFalse(IDataSet.providedBy(self.document))

        adapter = getMultiAdapter(
            (self.document, self.portal_catalog),
            interface=IIndexer,
            name="dataset_geographical_classification",
        )
        self.assertRaises(AttributeError, adapter)


class TestIndexerUtils(unittest.TestCase):
    """test utils"""

    def test_expand_bounding_box(self):
        """test the expand_bounding_box function"""
        bounding_box = {
            "north": "10",
            "east": "20",
            "west": "30",
            "south": "40",
        }

        values = expand_bounding_box(bounding_box)
        self.assertEqual(values, (10.0, 20.0, 40.0, 30.0))

    def test_is_eea(self):
        """test the is_eea function"""
        bounding_box_true = {
            "north": "90",
            "east": "20",
            "west": "50",
            "south": "20",
        }

        bounding_box_false = {
            "north": "90",
            "east": "20",
            "west": "50",
            "south": "10",
        }

        self.assertTrue(is_eea(bounding_box_true))
        self.assertFalse(is_eea(bounding_box_false))

    def test_is_northern_hemisphere(self):
        """test the is_northern_hemisphere function"""
        bounding_box_true = {
            "north": "90",
            "east": "20",
            "west": "50",
            "south": "20",
        }

        bounding_box_false = {
            "north": "90",
            "east": "20",
            "west": "50",
            "south": "-10",
        }

        self.assertTrue(is_northern_hemisphere(bounding_box_true))
        self.assertFalse(is_northern_hemisphere(bounding_box_false))

    def test_is_southern_hemisphere(self):
        """test the is_southern_hemisphere function"""
        bounding_box_true = {
            "north": "-90",
            "east": "20",
            "west": "50",
            "south": "-20",
        }

        bounding_box_false = {
            "north": "90",
            "east": "20",
            "west": "50",
            "south": "10",
        }

        self.assertTrue(is_southern_hemisphere(bounding_box_true))
        self.assertFalse(is_southern_hemisphere(bounding_box_false))

    def test_classify_bounding_boxes(self):
        """test the classify_bounding_boxes function"""

        bbox_eea = {
            "north": "90",
            "east": "20",
            "west": "50",
            "south": "20",
        }

        bbox_northern = {
            "north": "90",
            "east": "20",
            "west": "50",
            "south": "10",
        }

        bbox_southern = {
            "north": "-90",
            "east": "20",
            "west": "50",
            "south": "-20",
        }

        bbox_global = {
            "north": "78.25",
            "east": "180",
            "west": "-180",
            "south": "-60",
        }

        self.assertIn(
            "European Economic Area", classify_bounding_boxes([bbox_eea])
        )
        self.assertIn(
            "Northern hemisphere", classify_bounding_boxes([bbox_northern])
        )
        self.assertIn(
            "Southern hemisphere", classify_bounding_boxes([bbox_southern])
        )
        self.assertIn(
            "Northern hemisphere",
            classify_bounding_boxes([bbox_northern, bbox_southern]),
        )
        self.assertIn(
            "Southern hemisphere",
            classify_bounding_boxes([bbox_northern, bbox_southern]),
        )

        self.assertIn(
            "Global",
            classify_bounding_boxes([bbox_global]),
        )
