# -*- coding: utf-8 -*-
"""distribution format list indexers"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.content.data_set import IDataSet

FORMAT_CONVERSION = {"netCDF": "NetCDF", "GTiff": "GeoTIFF"}


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDataSet)
def distribution_format_list(obj):
    """Calculate and return the value for the indexer"""
    values = []
    if obj.distribution_format_list:
        for value in obj.distribution_format_list:
            values.append(FORMAT_CONVERSION.get(value, value))
    return values
