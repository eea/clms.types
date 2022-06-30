# -*- coding: utf-8 -*-
"""
Test the vocabulary
"""
import json

import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


class TestComponentTitleVocabularyIntegrationTest(unittest.TestCase):
    """test the vocabulary"""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        value = json.dumps(
            {
                "items": [
                    {"@id": "id1", "name": "id-1", "description": "name_1"},
                    {"@id": "id2", "name": "id-2", "description": "name_2"},
                ]
            }
        )

        api.portal.set_registry_record(
            "clms.types.product_component.product_components", value
        )

    def test_vocabulary(self):
        """test values are those defined"""
        vocab_name = "clms.types.ComponentTitleVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertIn("id1", vocabulary)
        self.assertIn("id2", vocabulary)
        self.assertNotIn("id3", vocabulary)
        self.assertNotIn("id4", vocabulary)
