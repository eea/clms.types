"""
Test the vocabulary
"""
# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from clms.types import _
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


class TestCategoryTopicsVocabularyIntegrationTest(unittest.TestCase):
    """ test the vocabulary"""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocabulary(self):
        """ test values are those defined"""
        vocab_name = "clms.types.CategoryTopicsVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(
            vocabulary.getTerm("farming").title,
            _(u"Farming"),
        )

        self.assertEqual(vocabulary.getTerm(u"farming").title, _(u"Farming"))

        self.assertEqual(vocabulary.getTerm(u"biota").title, _(u"Biota"))

        self.assertEqual(
            vocabulary.getTerm(u"boundaries").title, _(u"Boundaries")
        )

        self.assertEqual(
            vocabulary.getTerm(u"climatologyMeteorologyAtmosphere").title,
            _(u"Climatology/Meteorology/Atmosphere"),
        )

        self.assertEqual(vocabulary.getTerm(u"economy").title, _(u"Economy"))

        self.assertEqual(
            vocabulary.getTerm(u"environment").title, _(u"Environment")
        )

        self.assertEqual(
            vocabulary.getTerm(u"geoscientificInformation").title,
            _(u"Geoscientific Information"),
        )

        self.assertEqual(vocabulary.getTerm(u"health").title, _(u"Health"))

        self.assertEqual(
            vocabulary.getTerm(u"imageryBaseMapsEarthCover").title,
            _(u"Imagery/Base Maps/Earth Cover"),
        )
        self.assertEqual(
            vocabulary.getTerm(u"intelligence").title, _(u"Intelligence")
        )

        self.assertEqual(
            vocabulary.getTerm(u"inlandWater").title, _(u"Inland Water")
        )

        self.assertEqual(vocabulary.getTerm(u"location").title, _(u"Location"))

        self.assertEqual(vocabulary.getTerm(u"oceans").title, _(u"Oceans"))

        self.assertEqual(
            vocabulary.getTerm(u"planningCadastre").title,
            _(u"Planning/Cadastre"),
        )

        self.assertEqual(vocabulary.getTerm(u"society").title, _(u"Society"))

        self.assertEqual(
            vocabulary.getTerm(u"transportation").title, _(u"Transportation")
        )

        self.assertEqual(
            vocabulary.getTerm(u"utilitiesCommunication").title,
            _(u"Utilities/Communication"),
        )
