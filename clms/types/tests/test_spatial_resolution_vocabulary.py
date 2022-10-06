""" test the vocabulary"""
# -*- coding: utf-8 -*-
import unittest

import transaction
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types.testing import CLMS_TYPES_FUNCTIONAL_TESTING


class TestSpatialResolutionVocabularyIntegrationTest(unittest.TestCase):
    """test the vocabulary"""

    layer = CLMS_TYPES_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.dataset1 = api.content.create(
            container=self.portal,
            type="DataSet",
            id="dataset1",
            qualitySpatialResolution_line="1 km,2 km,3 km",
        )
        self.dataset2 = api.content.create(
            container=self.portal,
            type="DataSet",
            id="dataset2",
            qualitySpatialResolution_line="20m,1km",
        )

        transaction.commit()

    def test_vocabulary(self):
        """test that the values come from the spatial_resolution index"""
        vocab_name = "clms.types.SpatialResolutionVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertIn("1", vocabulary)
        self.assertIn("2", vocabulary)
        self.assertIn("3", vocabulary)
        self.assertIn("20", vocabulary)
        self.assertNotIn("100", vocabulary)
