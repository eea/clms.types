""" test the vocabulary"""
# -*- coding: utf-8 -*-
import unittest

import transaction
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.uuid.interfaces import IUUID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types import _
from clms.types.testing import CLMS_TYPES_FUNCTIONAL_TESTING


class TestTemporalExtentVocabularyIntegrationTest(unittest.TestCase):
    """ test the vocabulary"""

    layer = CLMS_TYPES_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.dataset1 = api.content.create(
            container=self.portal,
            type="DataSet",
            id="dataset1",
            temporalExtentStart="2014-01-01",
            temporalExtentEnd="2018-12-31",
        )
        self.dataset2 = api.content.create(
            container=self.portal,
            type="DataSet",
            id="dataset2",
            temporalExtentStart="2015-01-01",
            temporalExtentEnd="2020-12-31",
        )

        self.dataset1.reindexObject()
        self.dataset2.reindexObject()

        transaction.commit()

    def test_vocabulary(self):
        """test that the values come from the temporal_extent index"""
        vocab_name = "clms.types.TemporalExtentVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertIn(2014, vocabulary)
        self.assertIn(2015, vocabulary)
        self.assertIn(2016, vocabulary)
        self.assertIn(2017, vocabulary)
        self.assertIn(2018, vocabulary)
        self.assertIn(2019, vocabulary)
        self.assertIn(2020, vocabulary)
