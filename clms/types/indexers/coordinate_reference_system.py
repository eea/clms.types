# -*- coding: utf-8 -*-
"""distribution format list indexers"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.content.data_set import IDataSet

ADMITTED_SYSTEM_LIST = [
    "EPSG:3035",
    "EPSG:32625",
    "EPSG:4326",
    "EPSG:32662",
]


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDataSet)
def coordinate_reference_system(obj):
    """Calculate and return the value for the indexer"""
    values = []
    if obj.coordinateReferenceSystemList:
        for value in obj.coordinateReferenceSystemList:
            if value in ADMITTED_SYSTEM_LIST:
                values.append(value)
    return values
