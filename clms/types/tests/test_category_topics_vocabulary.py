"""
Test the vocabulary
"""
# -*- coding: utf-8 -*-
import unittest

import transaction
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types import _
from clms.types.testing import CLMS_TYPES_FUNCTIONAL_TESTING


class TestCategoryTopicsVocabularyIntegrationTest(unittest.TestCase):
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
            classificationTopicCategory=["category1", "category2"],
        )
        self.dataset2 = api.content.create(
            container=self.portal,
            type="DataSet",
            id="dataset2",
            classificationTopicCategory=["category2", "category3"],
        )

        transaction.commit()

    def test_vocabulary(self):
        """ test values are those defined"""
        vocab_name = "clms.types.CategoryTopicsVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertIn("category1", vocabulary)
        self.assertIn("category2", vocabulary)
        self.assertIn("category3", vocabulary)
        self.assertNotIn("category4", vocabulary)
