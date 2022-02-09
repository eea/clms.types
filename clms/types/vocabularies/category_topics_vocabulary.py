# -*- coding: utf-8 -*-
"""
Category Topics vocabulary definition
"""

from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

# from plone import api
from clms.types import _


class VocabItem:
    """
    VocabItem class
    """

    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class CategoryTopicsVocabulary:
    """
    CategoryTopics vocabulary class
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem(u"farming", _(u"Farming")),
            VocabItem(u"biota", _(u"Biota")),
            VocabItem(u"boundaries", _(u"Boundaries")),
            VocabItem(
                u"climatologyMeteorologyAtmosphere",
                _(u"Climatology/Meteorology/Atmosphere"),
            ),
            VocabItem(u"economy", _(u"Economy")),
            VocabItem(u"environment", _(u"Environment")),
            VocabItem(
                u"geoscientificInformation", _(u"Geoscientific Information")
            ),
            VocabItem(u"health", _(u"Health")),
            VocabItem(
                u"imageryBaseMapsEarthCover",
                _(u"Imagery/Base Maps/Earth Cover"),
            ),
            VocabItem(u"intelligence", _(u"Intelligence")),
            VocabItem(u"inlandWater", _(u"Inland Water")),
            VocabItem(u"location", _(u"Location")),
            VocabItem(u"oceans", _(u"Oceans")),
            VocabItem(u"planningCadastre", _(u"Planning/Cadastre")),
            VocabItem(u"society", _(u"Society")),
            VocabItem(u"transportation", _(u"Transportation")),
            VocabItem(
                u"utilitiesCommunication", _(u"Utilities/Communication")
            ),
        ]

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


CategoryTopicsVocabularyFactory = CategoryTopicsVocabulary()
