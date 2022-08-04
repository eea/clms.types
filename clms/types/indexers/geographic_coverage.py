# -*- coding: utf-8 -*-
"""Associated products indexers"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.content.data_set import IDataSet
from clms.types.content.product import IProduct


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IProduct)
def geographic_coverage_product(obj):
    """Calculate and return the value for the indexer"""
    geographic_coverages = []
    for dataset in obj.values():
        if dataset.portal_type == "DataSet":
            value = geographic_coverage(dataset)
            if value:
                geographic_coverages.extend(value)

    return geographic_coverages


@indexer(IDataSet)
def geographic_coverage(obj):
    """Calculate and return the value for the indexer"""
    items = obj.geographicCoverage.get("geolocation", [])
    return [item.get("label") for item in items]
