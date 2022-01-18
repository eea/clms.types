# -*- coding: utf-8 -*-
"""Associated products indexers"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.content.data_set import IDataSet
from datetime import datetime


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDataSet)
def temporal_extent(obj):
    """Calculate and return the value for the indexer"""
    try:
        dt_temporalExtentStart = datetime.strptime(
            obj.temporalExtentStart, "%Y-%m-%d"
        )
    except ValueError:
        return []

    try:
        dt_temporalExtentEnd = datetime.strptime(
            obj.temporalExtentEnd, "%Y-%m-%d"
        )
    except ValueError:
        dt_temporalExtentEnd = datetime.now()

    try:
        return range(
            dt_temporalExtentStart.year, dt_temporalExtentEnd.year + 1
        )
    except ValueError:
        return []
