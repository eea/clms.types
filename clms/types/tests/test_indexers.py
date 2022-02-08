"""
Tests indexers on this package
"""
# -*- coding: utf-8 -*-
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING
from clms.types.behaviors.dataset_relation import IDataSetRelationMarker
from clms.types.behaviors.product_relation import IProductRelationMarker
from clms.types.indexers.associated_datasets import (
    associated_datasets_behavior,
)
from plone.uuid.interfaces import IUUID
import unittest
from plone import api


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
        self.newsitem1.datasets = [IUUID(self.product)]
        self.assertEqual(
            associated_datasets_behavior(self.newsitem1)(),
            [IUUID(self.product)],
        )
