"""
classify datasets according to their coordinates into spatial categories
"""
# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.content.data_set import IDataSet


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDataSet)
def dataset_geographical_classification(obj):
    """Calculate and return the value for the indexer"""
    bounding_boxes = obj.geographicBoundingBox.get("items", [])
    return classify_bounding_boxes(bounding_boxes)


def classify_bounding_boxes(bounding_boxes):
    """classify the bounding boxes according to their location"""
    terms = []

    for bounding_box in bounding_boxes:
        if is_eea(bounding_box):
            terms.append("European Economic Area")
        elif is_northern_hemisphere(bounding_box):
            terms.append("Northern hemisphere")
        else:
            terms.append("Global")

    return list(set(terms))


def expand_bounding_box(bounding_box):
    """given a dict with the bounding box, expand its values to a list"""
    north = bounding_box.get("north")
    east = bounding_box.get("east")
    south = bounding_box.get("south")
    west = bounding_box.get("west")

    return float(north), float(east), float(south), float(west)


def is_eea(bounding_box):
    """check if the bounding box corresponds to EEA"""
    north, east, south, west = expand_bounding_box(bounding_box)

    return north <= 90.0 and south >= 20.0 and east <= 74.0 and west >= -60.0


def is_northern_hemisphere(bounding_box):
    """check if the bounding box corresponds to the northern hemisphere"""
    north, east, south, west = expand_bounding_box(bounding_box)

    return north <= 90.0 and south >= 0.0 and east <= 180.0 and west >= -180.0
