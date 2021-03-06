""" test the vocabulary"""
# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


class TestUseCaseSpatialCoverageVocabularyIntegrationTest(unittest.TestCase):
    """test the vocabulary"""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocabulary(self):
        """test that the values come from the custodian_information
        index in the catalog (those with role=custodian)
        """
        vocab_name = "clms.types.UseCaseSpatialCoverageVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertIn("AD", vocabulary)
        self.assertIn("AE", vocabulary)
        self.assertIn("AF", vocabulary)
        self.assertIn("AG", vocabulary)
        self.assertIn("AI", vocabulary)
        self.assertIn("AL", vocabulary)
        self.assertIn("AM", vocabulary)
        self.assertIn("AO", vocabulary)
        self.assertIn("AR", vocabulary)
        self.assertIn("AS", vocabulary)
        self.assertIn("AT", vocabulary)
        self.assertIn("BW", vocabulary)
        self.assertIn("CG", vocabulary)
        self.assertIn("CH", vocabulary)
        self.assertIn("CI", vocabulary)
        self.assertIn("CK", vocabulary)
        self.assertIn("AQ", vocabulary)
        self.assertIn("BY", vocabulary)
        self.assertIn("BZ", vocabulary)
        self.assertIn("BJ", vocabulary)
        self.assertIn("BN", vocabulary)
        self.assertIn("BO", vocabulary)
        self.assertIn("BQ", vocabulary)
        self.assertIn("BT", vocabulary)
        self.assertIn("BV", vocabulary)
        self.assertIn("BR", vocabulary)
        self.assertIn("BS", vocabulary)
        self.assertIn("CA", vocabulary)
        self.assertIn("AU", vocabulary)
        self.assertIn("AW", vocabulary)
        self.assertIn("AZ", vocabulary)
        self.assertIn("BA", vocabulary)
        self.assertIn("BB", vocabulary)
        self.assertIn("BD", vocabulary)
        self.assertIn("BE", vocabulary)
        self.assertIn("BF", vocabulary)
        self.assertIn("BG", vocabulary)
        self.assertIn("BH", vocabulary)
        self.assertIn("BI", vocabulary)
        self.assertIn("CL", vocabulary)
        self.assertIn("CD", vocabulary)
        self.assertIn("CF", vocabulary)
        self.assertIn("CN", vocabulary)
        self.assertIn("DJ", vocabulary)
        self.assertIn("DM", vocabulary)
        self.assertIn("DO", vocabulary)
        self.assertIn("CO", vocabulary)
        self.assertIn("CR", vocabulary)
        self.assertIn("CU", vocabulary)
        self.assertIn("CV", vocabulary)
        self.assertIn("CW", vocabulary)
        self.assertIn("CY", vocabulary)
        self.assertIn("CZ", vocabulary)
        self.assertIn("FI", vocabulary)
        self.assertIn("CM", vocabulary)
        self.assertIn("DE", vocabulary)
        self.assertIn("DZ", vocabulary)
        self.assertIn("DK", vocabulary)
        self.assertIn("ER", vocabulary)
        self.assertIn("EL", vocabulary)
        self.assertIn("ET", vocabulary)
        self.assertIn("FM", vocabulary)
        self.assertIn("FO", vocabulary)
        self.assertIn("GA", vocabulary)
        self.assertIn("GD", vocabulary)
        self.assertIn("GE", vocabulary)
        self.assertIn("GG", vocabulary)
        self.assertIn("GH", vocabulary)
        self.assertIn("GI", vocabulary)
        self.assertIn("FR", vocabulary)
        self.assertIn("ES", vocabulary)
        self.assertIn("FJ", vocabulary)
        self.assertIn("FK", vocabulary)
        self.assertIn("EC", vocabulary)
        self.assertIn("EE", vocabulary)
        self.assertIn("EG", vocabulary)
        self.assertIn("EH", vocabulary)
        self.assertIn("GL", vocabulary)
        self.assertIn("GM", vocabulary)
        self.assertIn("GN", vocabulary)
        self.assertIn("GQ", vocabulary)
        self.assertIn("GS", vocabulary)
        self.assertIn("GT", vocabulary)
        self.assertIn("GU", vocabulary)
        self.assertIn("GW", vocabulary)
        self.assertIn("HR", vocabulary)
        self.assertIn("HT", vocabulary)
        self.assertIn("HU", vocabulary)
        self.assertIn("GY", vocabulary)
        self.assertIn("HK", vocabulary)
        self.assertIn("HM", vocabulary)
        self.assertIn("HN", vocabulary)
        self.assertIn("KH", vocabulary)
        self.assertIn("KI", vocabulary)
        self.assertIn("KM", vocabulary)
        self.assertIn("KN", vocabulary)
        self.assertIn("KP", vocabulary)
        self.assertIn("KW", vocabulary)
        self.assertIn("KY", vocabulary)
        self.assertIn("NP", vocabulary)
        self.assertIn("NR", vocabulary)
        self.assertIn("NU", vocabulary)
        self.assertIn("IT", vocabulary)
        self.assertIn("LC", vocabulary)
        self.assertIn("LI", vocabulary)
        self.assertIn("MR", vocabulary)
        self.assertIn("KR", vocabulary)
        self.assertIn("LA", vocabulary)
        self.assertIn("MS", vocabulary)
        self.assertIn("JP", vocabulary)
        self.assertIn("KG", vocabulary)
        self.assertIn("ID", vocabulary)
        self.assertIn("IE", vocabulary)
        self.assertIn("IL", vocabulary)
        self.assertIn("IM", vocabulary)
        self.assertIn("IO", vocabulary)
        self.assertIn("IN", vocabulary)
        self.assertIn("IQ", vocabulary)
        self.assertIn("IS", vocabulary)
        self.assertIn("JE", vocabulary)
        self.assertIn("JM", vocabulary)
        self.assertIn("JO", vocabulary)
        self.assertIn("IR", vocabulary)
        self.assertIn("KE", vocabulary)
        self.assertIn("OM", vocabulary)
        self.assertIn("LB", vocabulary)
        self.assertIn("LS", vocabulary)
        self.assertIn("LT", vocabulary)
        self.assertIn("LU", vocabulary)
        self.assertIn("LV", vocabulary)
        self.assertIn("LY", vocabulary)
        self.assertIn("MA", vocabulary)
        self.assertIn("MM", vocabulary)
        self.assertIn("NO", vocabulary)
        self.assertIn("PA", vocabulary)
        self.assertIn("LK", vocabulary)
        self.assertIn("LR", vocabulary)
