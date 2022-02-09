""" test the vocabulary"""
# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.uuid.interfaces import IUUID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized
from clms.downloadtool.utils import DATASET_SOURCES
from clms.types import _
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


class TestGemetInspireThemesVocabularyIntegrationTest(unittest.TestCase):
    """ test the vocabulary"""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.dataset1 = api.content.create(
            container=self.portal,
            type="DataSet",
            id="dataset1",
            gemetInspireThemes=["theme1", "theme2"],
        )

        self.dataset2 = api.content.create(
            container=self.portal,
            type="DataSet",
            id="dataset2",
            gemetInspireThemes=["theme2"],
        )

    def test_vocabulary(self):
        """test that the values come from the custodian_information
        index in the catalog (those with role=custodian)
        """
        vocab_name = "clms.types.GemetInspireThemesVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertIn("theme1", vocabulary)
        self.assertIn("theme2", vocabulary)
        self.assertNotIn("theme3", vocabulary)
        self.assertNotIn("theme4", vocabulary)
