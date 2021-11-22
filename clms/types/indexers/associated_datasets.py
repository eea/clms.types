# -*- coding: utf-8 -*-
"""Associated products indexers"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.behaviors.dataset_relation import IDataSetRelationMarker


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDataSetRelationMarker)
def associated_datasets_behavior(obj):
    """Calculate and return the value for the indexer"""
    return obj.datasets
