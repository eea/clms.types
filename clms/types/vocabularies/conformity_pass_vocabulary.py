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
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem(u"false", _(u"False")),
            VocabItem(u"true", _(u"True")),
            VocabItem(u"Null", _(u"Null")),
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
