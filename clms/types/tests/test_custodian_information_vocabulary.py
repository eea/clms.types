""" test the vocabulary"""
# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types import _
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


class TestCustodianInformationVocabularyIntegrationTest(unittest.TestCase):
    """ test the vocabulary"""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.dataset1 = api.content.create(
            container=self.portal, type="DataSet", id="dataset1"
        )
        responsibleParty1 = {
            "organisationName": "The Organization",
            "roleCode": "custodian",
        }
        responsibleParty2 = {
            "organisationName": "The Organization 1",
            "roleCode": "owner",
        }
        responsibleParty3 = {
            "organisationName": "The Organization 2",
            "roleCode": "reviewer",
        }

        self.dataset1.responsiblePartyWithRole = {
            "items": [
                responsibleParty1,
                responsibleParty2,
            ]
        }

        self.dataset2 = api.content.create(
            container=self.portal, type="DataSet", id="dataset2"
        )
        self.dataset2.responsiblePartyWithRole = {
            "items": [
                responsibleParty1,
                responsibleParty3,
            ]
        }

    def test_vocabulary(self):
        """test that the values come from the custodian_information
        index in the catalog (those with role=custodian)
        """
        vocab_name = "clms.types.CustodianInformationVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(
            vocabulary.getTerm("The Organization").title,
            _(u"The Organization"),
        )

        self.assertIn("The Organization", vocabulary)
        self.assertNotIn("The Organization 1", vocabulary)
        self.assertNotIn("The Organization 2", vocabulary)
