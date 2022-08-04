# -*- coding: utf-8 -*-
"""Associated products indexers"""
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer

from clms.types.content.data_set import IDataSet
from clms.types.content.product import IProduct


FORMAT_CONVERSION = {
    "annually": "Anually",
    "asNeeded": "As needed",
    "continual": "Continual",
}


def convert_values(values):
    """convert values to a standard values to be shown"""
    new_values = []
    for value in values:
        new_values.append(FORMAT_CONVERSION.get(value, value))

    return new_values


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IProduct)
def update_frequency_product(obj):
    """index value for products"""
    update_frequencies = []
    for dataset in obj.values():
        if dataset.portal_type == "DataSet":
            # pylint disable=not-callable
            value = update_frequency_dataset(dataset)()
            if value is not None:
                update_frequencies.extend(value)

    return convert_values(update_frequencies)


@indexer(IDataSet)
def update_frequency_dataset(obj):
    """Calculate and return the value for the indexer"""
    return convert_values(
        obj.update_frequency and [obj.update_frequency.strip()] or []
    )
