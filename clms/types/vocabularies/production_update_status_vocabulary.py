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
class ProductionUpdateStatusVocabulary:
    """
    Topics vocabulary class
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem("active", _("Active")),
            VocabItem("resolved", _("Resolved")),
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
        return SimpleVocabulary(sorted(terms, key=lambda x: x.title.lower()))


ProductionUpdateStatusVocabularyFactory = ProductionUpdateStatusVocabulary()
