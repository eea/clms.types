# -*- coding: utf-8 -*-
"""
An indexer to index the position of the taxonomy selected in a
Technical Library to be able to sort on it.
"""
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from zope.component import getUtility
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory
from clms.types.utils import get_taxonomy_tree

from clms.types.content.technical_library import ITechnicalLibrary


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


def build_index_value(first, second):
    """build an index value to return
    the first value is more important than the second
    """

    return (first * 1000) + second


@indexer(ITechnicalLibrary)
def documentation_sorting(obj):
    """Calculate and return the value for the indexer:
    we need to check the position of the selected value in the vocabulary
    and return the minimum, because documents may be related to more than
    one taxonomy item
    """
    taxonomy_name = "collective.taxonomy.technical_library_categorization"
    taxonomy_tree = get_taxonomy_tree(taxonomy_name)
    items = obj.taxonomy_technical_library_categorization
    if items:
        factory = getUtility(
            IVocabularyFactory,
            name=taxonomy_name,
        )
        vocabulary = factory(obj)

        result = []

        for item in items:
            try:
                term = vocabulary.getTerm(item)
                title = translate(term.title)
                try:
                    item_id, _ = title.split("#")
                    result.append(int(item_id))
                except ValueError:
                    result.append(999)
            except KeyError:
                # It has an unexisting taxonomy assigned
                # do nothing
                pass

        value = min(result) or 999
        return build_index_value(
            value, get_index_in_subtree(taxonomy_tree, value, items)
        )

    return build_index_value(999, 999)


def get_index_in_subtree(tree, value, registered_values):
    """given a tree, a value and a list of registered values
    return the lowest index of the first registered_value seen
    in the tree that corresponds to the subtree of the value.

    Otherwise, return a big value
    """
    values = []
    for item in tree:
        item_title = item.get("title", "")
        try:
            # pylint: disable=unused-variable
            number, rest = item_title.split("#")
            if int(number) == value:
                for child_index, child in enumerate(item.get("children", [])):
                    if child.get("key", "") in registered_values:
                        values.append(child_index)
        except ValueError:
            # Catch any error that can happen
            pass

    values.sort()
    if values:
        return values[0]

    return 999
