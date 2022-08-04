""" test the vocabulary"""
# -*- coding: utf-8 -*-
import unittest

import transaction
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types.testing import CLMS_TYPES_FUNCTIONAL_TESTING


class TestUpdateFrequencyVocabularyIntegrationTest(unittest.TestCase):
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
            update_frequency="anually",
        )
        self.dataset2 = api.content.create(
            container=self.portal,
            type="DataSet",
            id="dataset2",
            update_frequency="daily",
        )

        self.dataset1.reindexObject()
        self.dataset2.reindexObject()

        transaction.commit()

    def test_vocabulary(self):
        """test that the values come from the temporal_extent index"""
        vocab_name = "clms.types.UpdateFrequencyVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertIn("anually", vocabulary)
        self.assertIn("daily", vocabulary)
        self.assertNotIn("monthly", vocabulary)
