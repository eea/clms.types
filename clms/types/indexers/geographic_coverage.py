# -*- coding: utf-8 -*-
"""Associated products indexers"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.content.data_set import IDataSet


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDataSet)
def geographic_coverage(obj):
    """Calculate and return the value for the indexer"""
    items = obj.geographicCoverage.get("geolocation", [])
    return [item.get("label") for item in items]
