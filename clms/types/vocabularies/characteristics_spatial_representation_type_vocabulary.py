# -*- coding: utf-8 -*-
"""
Spatial representation type vocabulary definition
"""

from plone import api
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
class CharacteristicsSpatialRepresentationType:
    """
    CategoryTopics vocabulary class
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        catalog = api.portal.get_tool("portal_catalog")
        items = catalog.uniqueValuesFor(
            "characteristics_spatial_representation_type")

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item,
                    token=str(item),
                    title=item,
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)

# pylint: disable=line-too-long
CharacteristicsSpatialRepresentationTypeFactory = CharacteristicsSpatialRepresentationType() # noqa
