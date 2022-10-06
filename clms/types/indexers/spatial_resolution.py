# -*- coding: utf-8 -*-
"""Associated products indexers"""

import re
from decimal import Decimal

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer

from clms.types.content.data_set import IDataSet


def convert_spatial_resolutions(values):
    """convert spatial resolution values from degrees to meters"""
    new_values = []
    for value in values:
        if value and value.strip().endswith("deg"):
            new_values.append(convert_spatial_resolution_from_deg_to_m(value))
        elif value and value.strip().endswith("m"):
            new_values.append(convert_spatial_resolution(value))
        else:
            try:
                new_values.append(
                    convert_spatial_resolution_from_anything(value)
                )
            except ValueError:
                pass

    return new_values


def convert_spatial_resolution(value):
    """remove the meeter and return a number"""
    value = re.sub(r"[m|km]", "", value.replace(",", "."))
    return str(value.strip())


def convert_spatial_resolution_from_anything(value):
    """try to convert from a number"""
    return str(value)


def convert_spatial_resolution_from_deg_to_m(value):
    """convert from degrees to meters"""
    numeric_value = value.replace("deg", "").strip()
    decimal_numeric_value = Decimal(numeric_value)
    # pylint: disable=line-too-long
    decimal_numeric_value_quantized = decimal_numeric_value.quantize(
        Decimal("1.0000")
    )  # noqa
    result = decimal_numeric_value_quantized * Decimal("10007566.8") / 90
    return convert_spatial_resolution(str(result.to_integral()))


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDataSet)
def spatial_resolution(obj):
    """Calculate and return the value for the indexer"""
    items = obj.qualitySpatialResolution_line
    return convert_spatial_resolutions(items.split(",") if items else [])
