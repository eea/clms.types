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
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING


class TestInspireThemesVocabularyIntegrationTest(unittest.TestCase):
    """ test the vocabulary"""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocabulary(self):
        """test that the values come from the custodian_information
        index in the catalog (those with role=custodian)
        """
        vocab_name = "clms.types.InspireThemesVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertIn("Addresses", vocabulary)
        self.assertIn("Administrative units", vocabulary)
        self.assertIn("Agricultural and aquaculture facilities", vocabulary)
        self.assertIn(
            "Area management/restriction/regulation zones and reporting units",
            vocabulary,
        )
        self.assertIn("Atmospheric conditions", vocabulary)
        self.assertIn("Bio-geographical regions", vocabulary)
        self.assertIn("Buildings", vocabulary)
        self.assertIn("Cadastral parcels", vocabulary)
        self.assertIn("Coordinate reference systems", vocabulary)
        self.assertIn("Elevation", vocabulary)
        self.assertIn("Energy resources", vocabulary)
        self.assertIn("Environmental monitoring facilities", vocabulary)
        self.assertIn("Geographical grid systems", vocabulary)
        self.assertIn("Geographical names", vocabulary)
        self.assertIn("Geology", vocabulary)
        self.assertIn("Habitats and biotopes", vocabulary)
        self.assertIn("Human health and safety", vocabulary)
        self.assertIn("Hydrography", vocabulary)
        self.assertIn("Land cover", vocabulary)
        self.assertIn("Land use", vocabulary)
        self.assertIn("Meteorological geographical features", vocabulary)
        self.assertIn("Mineral resources", vocabulary)
        self.assertIn("Natural risk zones", vocabulary)
        self.assertIn("Oceanographic geographical features", vocabulary)
        self.assertIn("Orthoimagery", vocabulary)
        self.assertIn("Population distribution — demography", vocabulary)
        self.assertIn("Production and industrial facilities", vocabulary)
        self.assertIn("Protected sites", vocabulary)
        self.assertIn("Sea regions", vocabulary)
        self.assertIn("Soil", vocabulary)
        self.assertIn("Species distribution", vocabulary)
        self.assertIn("Statistical units", vocabulary)
        self.assertIn("Transport networks", vocabulary)
        self.assertIn("Utility and governmental services    ", vocabulary)
