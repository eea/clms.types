"""
Tests indexers on this package
"""
import unittest

from plone import api

# -*- coding: utf-8 -*-
from plone.app.testing import SITE_OWNER_NAME, login
from plone.uuid.interfaces import IUUID

from clms.types.behaviors.dataset_relation import IDataSetRelationMarker
from clms.types.behaviors.product_relation import IProductRelationMarker
from clms.types.indexers.associated_datasets import (
    associated_datasets_behavior,
)
from clms.types.indexers.associated_products import (
    associated_products_behavior,
)
from clms.types.indexers.custodian_information import custodian_information
from clms.types.indexers.geographic_coverage import geographic_coverage
from clms.types.indexers.spatial_resolution import spatial_resolution
from clms.types.indexers.temporal_extent import temporal_extent
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING

import datetime


class TestAssociatedDatasetsIndexer(unittest.TestCase):
    """ test associated_datasets indexer """

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

        login(self.portal, SITE_OWNER_NAME)
        self.portal_catalog = api.portal.get_tool("portal_catalog")
        self.newsitem1 = api.content.create(
            container=self.portal, type="News Item", id="newsitem1"
        )
        self.product = api.content.create(
            container=self.portal, type="Product", id="product1"
        )
        self.dataset = api.content.create(
            container=self.product, type="DataSet", id="dataset1"
        )

    def test_newsitem_provides_dataset_relation_behavior(self):
        """ test dataset relation behavior index saves related datasets UID"""
        self.assertTrue(IDataSetRelationMarker.providedBy(self.newsitem1))
        self.newsitem1.datasets = [IUUID(self.dataset)]
        self.assertEqual(
            associated_datasets_behavior(self.newsitem1)(),
            [IUUID(self.dataset)],
        )

    def test_newsitem_provides_product_relation_behavior(self):
        """ test product relation behavior index saves related datasets UID"""
        self.assertTrue(IProductRelationMarker.providedBy(self.newsitem1))
        self.newsitem1.products = [IUUID(self.product)]
        self.assertEqual(
            associated_products_behavior(self.newsitem1)(),
            [IUUID(self.product)],
        )

    def test_custodian_information_indexer(self):
        """ test the value of the custodian information field """
        responsibleParty1 = {
            "organisationName": "The Organization",
            "roleCode": "custodian",
        }
        responsibleParty2 = {
            "organisationName": "The Organization 1",
            "roleCode": "owner",
        }
        responsibleParty3 = {
            "organisationName": "The Organization 2",
            "roleCode": "reviewer",
        }

        self.dataset.responsiblePartyWithRole = {
            "items": [
                responsibleParty1,
                responsibleParty2,
                responsibleParty3,
            ]
        }

        indexed_value = custodian_information(self.dataset)()

        self.assertEqual(len(indexed_value), 1)
        self.assertEqual(indexed_value[0], "The Organization")

    def test_geographic_coverage_indexer(self):
        """ test the geographic coveraget indexer """
        self.dataset.geographicCoverage = {"geolocation": [{"label": "EEA39"}]}

        indexed_value = geographic_coverage(self.dataset)()
        self.assertEqual(len(indexed_value), 1)
        self.assertEqual(indexed_value[0], "EEA39")

    def test_spatial_resolution_indexer(self):
        """ test the spatial resolution indexer """
        self.dataset.qualitySpatialResolution_line = "1 km,100 m"
        indexed_value = spatial_resolution(self.dataset)()

        self.assertEqual(len(indexed_value), 2)
        self.assertIn("1 km", indexed_value)
        self.assertIn("100 m", indexed_value)

    def test_temporal_extent_indexer(self):
        """ test the temporal extent indexer"""
        self.dataset.temporalExtentStart = "2015-01-01"
        self.dataset.temporalExtentEnd = "2020-12-31"

        indexed_value = temporal_extent(self.dataset)()
        self.assertEqual(len(indexed_value), len(range(2015, 2021)))

    def test_temporal_extend_invalid_end(self):
        """ test with open end """
        self.dataset.temporalExtentStart = "2015-01-01"
        self.dataset.temporalExtentEnd = ""

        indexed_value = temporal_extent(self.dataset)()
        self.assertEqual(
            len(indexed_value),
            len(range(2015, datetime.datetime.now().year + 1)),
        )

    def test_temporal_extent_invalid_start(self):
        """ test with invalid start """
        self.dataset.temporalExtentStart = ""
        self.dataset.temporalExtentEnd = ""

        indexed_value = temporal_extent(self.dataset)()
        self.assertEqual(indexed_value, [])

    def test_temporal_extent_invalid_date_values(self):
        """ test with invalid date values"""
        self.dataset.temporalExtentStart = "2021-13-45"
        self.dataset.temporalExtentEnd = "2029-12-31"

        indexed_value = temporal_extent(self.dataset)()
        self.assertEqual(indexed_value, [])

    def test_temportal_extent_not_date_values(self):
        """ test with not valid input"""
        self.dataset.temporalExtentStart = "Monday 23 of october 1998"
        self.dataset.temporalExtentEnd = "This is not a date"

        indexed_value = temporal_extent(self.dataset)()
        self.assertEqual(indexed_value, [])
