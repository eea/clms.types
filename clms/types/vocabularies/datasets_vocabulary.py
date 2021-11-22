# -*- coding: utf-8 -*-
"""
Topics vocabulary definition
"""

from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone import api
from plone.uuid.interfaces import IUUID


@implementer(IVocabularyFactory)
class DataSetsVocabulary:
    """
    DataSets vocabulary class
    """

    def __call__(self, context):
        datasets = api.content.find(
            context=api.portal.get_navigation_root(context),
            portal_type="DataSet",
        )
        datasetsList = [
            (IUUID(p.getObject(), None), p.getObject().title) for p in datasets
        ]
        terms = [
            SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
            for pair in datasetsList
        ]
        return SimpleVocabulary(terms)


DataSetsVocabularyFactory = DataSetsVocabulary()
