# -*- coding: utf-8 -*-
"""Associated products indexers"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.content.data_set import IDataSet
from decimal import Decimal


def convert_spatial_resolutions(values):
    """convert spatial resolution values from degrees to meters"""
    new_values = []
    for value in values:
        if value and value.strip().endswith("deg"):
            new_values.append(convert_spatial_resolution(value))
        else:
            new_values.append(value)

    return new_values


def convert_spatial_resolution(value):
    """convert from degrees to meters"""
    numeric_value = value.replace("deg", "").strip()
    decimal_numeric_value = Decimal(numeric_value)
    decimal_numeric_value_quantized = decimal_numeric_value.quantize(Decimal('1.0000'))
    result = decimal_numeric_value_quantized * Decimal('10007566.8') / 90
    return f'{result.to_integral()} m'


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDataSet)
def spatial_resolution(obj):
    """Calculate and return the value for the indexer"""
    items = obj.qualitySpatialResolution_line
    return convert_spatial_resolutions(items.split(",") if items else [])
