# -*- coding: utf-8 -*-
"""spatial representation type indexer indexer for datasets"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.content.data_set import IDataSet


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDataSet)
def spatial_representation_type(obj):
    """Calculate and return the value for the indexer"""
    values = []
    if obj.spatial_representation_type:
        for value in obj.spatial_representation_type:
            if value:
                values.append(value)
    return values
