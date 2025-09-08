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
            # pylint: disable=not-callable
            value = geographic_coverage(dataset)()
            if value:
                geographic_coverages.extend(value)

    return geographic_coverages


def normalize_gcoverage_value(value):
    """Use Global instead of multiple variations"""
    if not value:
        return value

    normalized = str(value).strip().lower()

    if normalized in {"globe", "global", "world"}:
        return "Global"

    return value


def normalize_gcoverage(value):
    """ Keep values as they are, but normalize Global value and always return
    a list
    """
    if not value:
        return []
    if isinstance(value, dict):
        items = value.get("geolocation", [])
        values = [item.get("label") for item in items]
        return normalize_gcoverage(values)
    if isinstance(value, list):
        return [
            normalize_gcoverage_value(v) for v in value if v is not None]
    return normalize_gcoverage_value(value)


@indexer(IDataSet)
def geographic_coverage(obj):
    """Calculate and return the value for the indexer"""
    return normalize_gcoverage(obj.geographicCoverage) or []
