# -*- coding: utf-8 -*-
"""
Component Title vocabulary definition
"""

import json

from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class VocabItem:
    """
    VocabItem class
    """

    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class ComponentTitleVocabulary:
    """
    Component Title vocabulary class
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items_raw = api.portal.get_registry_record(
            "clms.types.product_component.product_components"
        )
        items = json.loads(items_raw)
        items = items.get("items", [])

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item.get("@id"),
                    token=str(item.get("name", "")),
                    title=item.get("name", ""),
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


ComponentTitleVocabularyFactory = ComponentTitleVocabulary()
