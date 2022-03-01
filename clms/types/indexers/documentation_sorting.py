# -*- coding: utf-8 -*-
"""
An indexer to index the position of the taxonomy selected in a
Technical Library to be able to sort on it.
"""


from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from clms.types.content.technical_library import ITechnicalLibrary


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(ITechnicalLibrary)
def documentation_sorting(obj):
    """Calculate and return the value for the indexer:
    we need to check the position of the selected value in the vocabulary
    and return the minimum, because documents may be related to more than
    one taxonomy item
    """
    items = obj.taxonomy_technical_library_categorization
    factory = getUtility(
        IVocabularyFactory,
        name="collective.taxonomy.technical_library_categorization",
    )
    vocabulary = factory(obj)

    result = []

    for item in items:
        for i, vocabulary_item in enumerate(vocabulary):
            if vocabulary_item.value == item:
                result.append(i)
    return min(result)
