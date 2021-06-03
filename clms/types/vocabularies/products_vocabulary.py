# -*- coding: utf-8 -*-
"""
Topics vocabulary definition
"""

from clms.types import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone import api


@implementer(IVocabularyFactory)
class ProductsVocabulary(object):
    """
    Products vocabulary class
    """

    def __call__(self, context):
        products = api.content.find(portal_type='Product')
        productsList = [(p.getObject().id, p.getObject().title)
                        for p in products]
        terms = [SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
                 for pair in productsList]
        return SimpleVocabulary(terms)


ProductsVocabularyFactory = ProductsVocabulary()