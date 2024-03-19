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
def dataset_characteristics_projections(obj):
    """Calculate and return the value for the indexer"""
    dataset_projection = obj.characteristics_projection
    projections = dataset_projection.split("/")

    cleaned_projections = map(clean, projections)
    return list(cleaned_projections)


def clean(item):
    """clean a EPSG value"""
    new_item = item.strip()
    if not new_item.startswith("EPSG"):
        new_item = f"EPSG:{new_item}"

    return new_item
