# -*- coding: utf-8 -*-
"""
Products and datasets vocabulary
"""

from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone import api
from plone.uuid.interfaces import IUUID


@implementer(IVocabularyFactory)
class ProductsAndDatasetsVocabulary:
    """
    Products vocabulary class
    """

    def __call__(self, context):
        items = api.content.find(
            context=api.portal.get_navigation_root(context),
            portal_type=["Product"],
            sort_on="sortable_title",
        )
        term_items = []
        for item in items:
            term_items.append(
                (IUUID(item.getObject(), None), item.getObject().title)
            )
            brains = api.content.find(
                context=item.getObject(),
                portal_type="DataSet",
                sort_on="sortable_title",
            )
            for brain in brains:
                dataset_title = "{} » {}".format(
                    item.getObject().title, brain.getObject().title
                )
                term_items.append(
                    (IUUID(brain.getObject(), None), dataset_title)
                )

        terms = [
            SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
            for pair in term_items
        ]
        return SimpleVocabulary(terms)


ProductsAndDatasetsVocabularyFactory = ProductsAndDatasetsVocabulary()
