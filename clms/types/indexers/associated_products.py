# -*- coding: utf-8 -*-
"""Associated products indexers"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.behaviors.product_relation import IProductRelationMarker


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IProductRelationMarker)
def associated_products_behavior(obj):
    """Calculate and return the value for the indexer"""
    return obj.products
