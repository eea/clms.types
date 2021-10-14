# -*- coding: utf-8 -*-
"""
Category Topics vocabulary definition
"""

# from plone import api
# from clms.types import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


values = [
    ("Addresses", "Addresses"),
    ("Administrative units", "Administrative units"),
    (
        "Agricultural and aquaculture facilities",
        "Agricultural and aquaculture facilities",
    ),
    (
        "Area management/restriction/regulation zones and reporting units",
        "Area management/restriction/regulation zones and reporting units",
    ),
    ("Atmospheric conditions", "Atmospheric conditions"),
    ("Bio-geographical regions", "Bio-geographical regions"),
    ("Buildings", "Buildings"),
    ("Cadastral parcels", "Cadastral parcels"),
    ("Coordinate reference systems", "Coordinate reference systems"),
    ("Elevation", "Elevation"),
    ("Energy resources", "Energy resources"),
    (
        "Environmental monitoring facilities",
        "Environmental monitoring facilities",
    ),
    ("Geographical grid systems", "Geographical grid systems"),
    ("Geographical names", "Geographical names"),
    ("Geology", "Geology"),
    ("Habitats and biotopes", "Habitats and biotopes"),
    ("Human health and safety", "Human health and safety"),
    ("Hydrography", "Hydrography"),
    ("Land cover", "Land cover"),
    ("Land use", "Land use"),
    (
        "Meteorological geographical features",
        "Meteorological geographical features",
    ),
    ("Mineral resources", "Mineral resources"),
    ("Natural risk zones", "Natural risk zones"),
    (
        "Oceanographic geographical features",
        "Oceanographic geographical features",
    ),
    ("Orthoimagery", "Orthoimagery"),
    (
        "Population distribution — demography",
        "Population distribution — demography",
    ),
    (
        "Production and industrial facilities",
        "Production and industrial facilities",
    ),
    ("Protected sites", "Protected sites"),
    ("Sea regions", "Sea regions"),
    ("Soil", "Soil"),
    ("Species distribution", "Species distribution"),
    ("Statistical units", "Statistical units"),
    ("Transport networks", "Transport networks"),
    (
        "Utility and governmental services    ",
        "Utility and governmental services    ",
    ),
]


class VocabItem:
    """
    VocabItem class
    """

    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class InspireThemesVocabulary:
    """
    InspireTheme vocabulary class
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [VocabItem(value[0], value[0]) for value in values]

        # Fix context if you are using the vocabulary in DataGridField.
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item.token,
                    token=str(item.token),
                    title=item.value,
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


InspireThemesVocabularyFactory = InspireThemesVocabulary()
