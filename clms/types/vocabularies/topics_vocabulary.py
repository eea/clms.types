# -*- coding: utf-8 -*-
"""
Topics vocabulary definition
"""

from clms.types import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class VocabItem:
    """
    VocabItem class
    """

    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class TopicsVocabulary:
    """
    Topics vocabulary class
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem("1", _("Biota")),
            VocabItem("2", _("Boundaries")),
            VocabItem("3", _("Climatology / Meteorology / Atmosphere")),
            VocabItem("4", _("Economy")),
            VocabItem("5", _("Elevation")),
            VocabItem("6", _("Environment")),
            VocabItem("7", _("Farming")),
            VocabItem("8", _("Geoscientific Information")),
            VocabItem("9", _("Health")),
            VocabItem("10", _("Imagery / Base Maps / Earth Cover")),
            VocabItem("11", _("Inland Waters")),
            VocabItem("12", _("Intelligence / Military")),
            VocabItem("13", _("Location")),
            VocabItem("14", _("Oceans")),
            VocabItem("15", _("Planning / Cadastre")),
            VocabItem("16", _("Society")),
            VocabItem("17", _("Structure")),
            VocabItem("18", _("Transportation")),
            VocabItem("19", _("Utilities / Communication")),
        ]

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


TopicsVocabularyFactory = TopicsVocabulary()
