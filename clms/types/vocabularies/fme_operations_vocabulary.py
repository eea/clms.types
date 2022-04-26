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
class FMEOperationsVocabulary:
    """
    ConformityPass vocabulary class
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem(u"DELETE", _(u"DELETE")),
            VocabItem(u"INSERT", _(u"INSERT")),
            VocabItem(u"UPDATE", _(u"UPDATE")),
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


FMEOperationsVocabularyFactory = FMEOperationsVocabulary()
