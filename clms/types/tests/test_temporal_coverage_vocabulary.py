""" test the vocabulary"""
# -*- coding: utf-8 -*-
import unittest

import transaction
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types.testing import CLMS_TYPES_FUNCTIONAL_TESTING


class TestTemporalCoverageVocabularyIntegrationTest(unittest.TestCase):
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
            temporalCoverage=["2000", "2001"],
        )
        self.dataset2 = api.content.create(
            container=self.portal,
            type="DataSet",
            id="dataset2",
            temporalCoverage=["2001", "2002"],
        )

        self.dataset1.reindexObject()
        self.dataset2.reindexObject()

        transaction.commit()

    def test_vocabulary(self):
        """test that the values come from the temportalCoverage index"""
        vocab_name = "clms.types.TemporalCoverageVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertIn("2000", vocabulary)
        self.assertIn("2001", vocabulary)
        self.assertIn("2002", vocabulary)
        self.assertNotIn("2003", vocabulary)
