# -*- coding: utf-8 -*-
"""Associated products indexers"""

from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from clms.types.content.data_set import IDataSet


CUSTODIAN_NAME_CORRECTIONS = [
    (
        "European Commission Directorate-General Joint Research Center",
        "European Commission Directorate-General Joint Research Centre",
    )
]


def convert_names(value):
    """convert several names to some others to unify"""
    for wrong, correct in CUSTODIAN_NAME_CORRECTIONS:
        value = value.replace(wrong, correct)

    return value


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDataSet)
def custodian_information(obj):
    """Calculate and return the value for the indexer"""
    items = obj.responsiblePartyWithRole.get("items", [])
    # pylint: disable=line-too-long
    return [
        convert_names(item.get("organisationName", ""))
        for item in items
        if item.get("roleCode", "") == "custodian"
    ]  # noqa: E501
