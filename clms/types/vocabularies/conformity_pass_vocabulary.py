# -*- coding: utf-8 -*-
"""
Conformity pass vocabulary definition
"""

from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from clms.types import _


class VocabItem:
    """
    VocabItem class
    """

    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class ConformityPassVocabulary:
    """
    ConformityPass vocabulary class
    """

    def __call__(self, context):
        # pylint: disable=line-too-long
        # item names taken from:
        # https://inspire.ec.europa.eu/metadata-codelist/DegreeOfConformity
        items = [
            VocabItem(u"false", _(u"Not Conformant")),
            VocabItem(u"true", _(u"Conformant")),
            VocabItem(u"Null", _(u"Not evaluated")),
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


ConformityPassVocabularyFactory = ConformityPassVocabulary()
