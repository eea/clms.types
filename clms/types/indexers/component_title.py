# -*- coding: utf-8 -*-
"""Component title indexers"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer

from clms.types.behaviors.mapviewer_component import IMapviewerComponentMarker


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IMapviewerComponentMarker)
def component_title_behavior(obj):
    """Calculate and return the value for the indexer"""

    return obj.mapviewer_component
