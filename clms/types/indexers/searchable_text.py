# -*- coding: utf-8 -*-
"""Searchable text indexers"""

from plone.indexer import indexer

from clms.types.content.data_set import IDataSet


def get_from_json(field, keys):
    """
    Get data from JSON
    """
    result = ""
    items = field.get("items", [])
    if len(items) == 0:
        return ""
    for item in items:
        for key in keys:
            if item.get(key) is not None:
                result += item.get(key) + " "

    return result


@indexer(IDataSet)
def searchable_text(obj):
    """Calculate and return the value for the indexer"""

    dataResourceAbstract = (
        obj.dataResourceAbstract.output if obj.dataResourceAbstract else ""
    )
    accessAndUseConstraints = (
        obj.accessAndUseConstraints.output
        if obj.accessAndUseConstraints
        else ""
    )

    conformitySpecification = (
        obj.conformitySpecification.output
        if obj.conformitySpecification
        else ""
    )
    qualityLineage = obj.qualityLineage.output if obj.qualityLineage else ""
    distributionInfo = get_from_json(
        obj.distributionInfo, ["resourceLocator", "services"]
    )

    responsiblePartyWithRole = get_from_json(
        obj.responsiblePartyWithRole,
        [
            "organisationName",
            "deliveryPoint",
            "city",
            "administrativeArea",
            "postalCode",
            "country",
            "electronicMailAddress",
            "url",
            "urlTitle",
            "roleCode",
        ],
    )

    point_of_contact_data = get_from_json(
        obj.point_of_contact_data,
        [
            "organisationName",
            "deliveryPoint",
            "city",
            "administrativeArea",
            "postalCode",
            "country",
            "electronicMailAddress",
            "url",
            "urlTitle",
            "roleCode",
        ],
    )

    return " ".join(
        [
            # obj.dataResourceTitle or "",
            dataResourceAbstract,
            obj.accessAndUseLimitationPublic_line or "",
            accessAndUseConstraints,
            obj.qualitySpatialResolution_line or "",
            responsiblePartyWithRole,
            conformitySpecification,
            qualityLineage,
            distributionInfo,
            point_of_contact_data,
            obj.update_frequency or "",
            obj.hierarchy_level or "",
            obj.metadata_standard_name or "",
        ]
    )
