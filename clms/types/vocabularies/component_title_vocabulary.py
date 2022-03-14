# -*- coding: utf-8 -*-
"""
Component Title vocabulary definition
"""

import pdb
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
import json


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
        # Fix context if you are using the vocabulary in DataGridField.
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

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
