""" test the vocabulary"""
# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types import _
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


class TestCoordinateReferenceSystemVocabularyIntegrationTest(
    unittest.TestCase
):
    """ test the vocabulary"""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.dataset1 = api.content.create(
            container=self.portal, type="DataSet", id="dataset1"
        )
        self.dataset1.coordinateReferenceSystemList = [
            "EPSG:4326",
            "EPSG:3857",
        ]

        self.dataset2 = api.content.create(
            container=self.portal, type="DataSet", id="dataset2"
        )
        self.dataset2.coordinateReferenceSystemList = ["EPSG:4326"]

    def test_vocabulary(self):
        """ test that the values come from indexed values"""
        vocab_name = "clms.types.CoordinateReferenceSystemVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(
            vocabulary.getTerm("EPSG:4326").title,
            _(u"EPSG:4326"),
        )

        self.assertEqual(
            vocabulary.getTerm(u"EPSG:3857").title, _(u"EPSG:3857")
        )
