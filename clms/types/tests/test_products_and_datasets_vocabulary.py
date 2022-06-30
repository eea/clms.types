""" test the vocabulary"""
# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.uuid.interfaces import IUUID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


class TestProductsVocabularyIntegrationTest(unittest.TestCase):
    """test the vocabulary"""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.product1 = api.content.create(
            container=self.portal, type="Product", id="product1"
        )
        self.product2 = api.content.create(
            container=self.portal, type="Product", id="product2"
        )

        self.dataset1 = api.content.create(
            container=self.product1, type="DataSet", id="dataset1"
        )
        self.dataset2 = api.content.create(
            container=self.product1, type="DataSet", id="dataset2"
        )
        self.dataset3 = api.content.create(
            container=self.product2, type="DataSet", id="dataset3"
        )

    def test_vocabulary(self):
        """test that the values of the product and datasets are in the
        vocabulary
        """
        vocab_name = "clms.types.ProductsAndDatasetsVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertIn(IUUID(self.product1), vocabulary)
        self.assertIn(IUUID(self.product2), vocabulary)
        self.assertIn(IUUID(self.dataset1), vocabulary)
        self.assertIn(IUUID(self.dataset2), vocabulary)
        self.assertIn(IUUID(self.dataset3), vocabulary)
