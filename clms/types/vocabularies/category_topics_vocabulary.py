# -*- coding: utf-8 -*-
"""
Category Topics vocabulary definition
"""

# from plone import api
from clms.types import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class VocabItem(object):
    """
    VocabItem class
    """

    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class CategoryTopicsVocabulary(object):
    """
    CategoryTopics vocabulary class
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem(u"Farming", _(u"Farming")),
            VocabItem(u"Biota", _(u"Biota")),
            VocabItem(u"Boundaries", _(u"Boundaries")),
            VocabItem(
                u"Climatology/Meteorology/Atmosphere",
                _(u"Climatology/Meteorology/Atmosphere"),
            ),
            VocabItem(u"Economy", _(u"Economy")),
            VocabItem(u"Environment", _(u"Environment")),
            VocabItem(
                u"Geoscientific Information", _(u"Geoscientific Information")
            ),
            VocabItem(u"Health", _(u"Health")),
            VocabItem(
                u"Imagery/Base Maps/Earth Cover",
                _(u"Imagery/Base Maps/Earth Cover"),
            ),
            VocabItem(u"Intelligence", _(u"Intelligence")),
            VocabItem(u"Inland Water", _(u"Inland Water")),
            VocabItem(u"Location", _(u"Location")),
            VocabItem(u"Oceans", _(u"Oceans")),
            VocabItem(u"Planning/Cadastre", _(u"Planning/Cadastre")),
            VocabItem(u"Society", _(u"Society")),
            VocabItem(u"Transportation", _(u"Transportation")),
            VocabItem(
                u"Utilities/Communication", _(u"Utilities/Communication")
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
