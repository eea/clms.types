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
        self.assertIn("ML", vocabulary)
        self.assertIn("MN", vocabulary)
        self.assertIn("MO", vocabulary)
        self.assertIn("MP", vocabulary)
        self.assertIn("NE", vocabulary)
        self.assertIn("MD", vocabulary)
        self.assertIn("ME", vocabulary)
        self.assertIn("MG", vocabulary)
        self.assertIn("MK", vocabulary)
        self.assertIn("MT", vocabulary)
        self.assertIn("MU", vocabulary)
        self.assertIn("KZ", vocabulary)
        self.assertIn("MW", vocabulary)
        self.assertIn("MY", vocabulary)
        self.assertIn("MZ", vocabulary)
        self.assertIn("NA", vocabulary)
        self.assertIn("NC", vocabulary)
        self.assertIn("NG", vocabulary)
        self.assertIn("NI", vocabulary)
        self.assertIn("NL", vocabulary)
        self.assertIn("PG", vocabulary)
        self.assertIn("PT", vocabulary)
        self.assertIn("PW", vocabulary)
        self.assertIn("PY", vocabulary)
        self.assertIn("QA", vocabulary)
        self.assertIn("RO", vocabulary)
        self.assertIn("NZ", vocabulary)
        self.assertIn("PE", vocabulary)
        self.assertIn("PF", vocabulary)
        self.assertIn("NF", vocabulary)
        self.assertIn("MX", vocabulary)
        self.assertIn("PH", vocabulary)
        self.assertIn("PK", vocabulary)
        self.assertIn("PL", vocabulary)
        self.assertIn("PM", vocabulary)
        self.assertIn("PN", vocabulary)
        self.assertIn("PR", vocabulary)
        self.assertIn("PS", vocabulary)
        self.assertIn("RS", vocabulary)
        self.assertIn("RU", vocabulary)
        self.assertIn("RW", vocabulary)
        self.assertIn("SA", vocabulary)
        self.assertIn("TF", vocabulary)
        self.assertIn("TG", vocabulary)
        self.assertIn("TH", vocabulary)
        self.assertIn("TJ", vocabulary)
        self.assertIn("TL", vocabulary)
        self.assertIn("SS", vocabulary)
        self.assertIn("ST", vocabulary)
        self.assertIn("SV", vocabulary)
        self.assertIn("SY", vocabulary)
        self.assertIn("SZ", vocabulary)
        self.assertIn("TC", vocabulary)
        self.assertIn("TD", vocabulary)
        self.assertIn("SC", vocabulary)
        self.assertIn("SB", vocabulary)
        self.assertIn("TT", vocabulary)
        self.assertIn("TR", vocabulary)
        self.assertIn("TZ", vocabulary)
        self.assertIn("SD", vocabulary)
        self.assertIn("SE", vocabulary)
        self.assertIn("SG", vocabulary)
        self.assertIn("SH", vocabulary)
        self.assertIn("SI", vocabulary)
        self.assertIn("SK", vocabulary)
        self.assertIn("SL", vocabulary)
        self.assertIn("SM", vocabulary)
        self.assertIn("SN", vocabulary)
        self.assertIn("TM", vocabulary)
        self.assertIn("TN", vocabulary)
        self.assertIn("TO", vocabulary)
        self.assertIn("SO", vocabulary)
        self.assertIn("SR", vocabulary)
        self.assertIn("SJ", vocabulary)
        self.assertIn("XV", vocabulary)
        self.assertIn("YE", vocabulary)
        self.assertIn("ZA", vocabulary)
        self.assertIn("ZM", vocabulary)
        self.assertIn("ZW", vocabulary)
        self.assertIn("UA", vocabulary)
        self.assertIn("UG", vocabulary)
        self.assertIn("UK", vocabulary)
        self.assertIn("XH", vocabulary)
        self.assertIn("XI", vocabulary)
        self.assertIn("XO", vocabulary)
        self.assertIn("XU", vocabulary)
        self.assertIn("VE", vocabulary)
        self.assertIn("VG", vocabulary)
        self.assertIn("VI", vocabulary)
        self.assertIn("VU", vocabulary)
        self.assertIn("VN", vocabulary)
        self.assertIn("WS", vocabulary)
        self.assertIn("XC", vocabulary)
        self.assertIn("XD", vocabulary)
        self.assertIn("XE", vocabulary)
        self.assertIn("XF", vocabulary)
        self.assertIn("XG", vocabulary)
        self.assertIn("US", vocabulary)
        self.assertIn("UY", vocabulary)
        self.assertIn("UZ", vocabulary)
        self.assertIn("VA", vocabulary)
        self.assertIn("VC", vocabulary)
        self.assertIn("EEA", vocabulary)
        self.assertIn("EU", vocabulary)
        self.assertIn("EU 27+UK", vocabulary)
