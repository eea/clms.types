# -*- coding: utf-8 -*-
"""
Import from geonetwork
"""

import json
from datetime import datetime
from logging import getLogger

import requests
from clms.types.indexers.dataset_geographical_classification import is_eea
from clms.types.utils import (
    COLORS,
    EEA_GEONETWORK_BASE_URL,
    NAMESPACES,
    NAMESPACES_VITO,
    VITO_GEONETWORK_BASE_URL,
)
from lxml import etree
from plone.app.textfield.value import RichTextValue
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.services import Service
from zope.interface import alsoProvides

ISO_DATETIME_FORMAT = "%Y-%m-%d"
ISO_DATETIME_FORMAT_WITH_TIME = "%Y-%m-%dT%H:%M:%S"
ISO_DATETIME_FORMAT_WITH_TIME_AND_FINAL_Z = "%Y-%m-%dT%H:%M:%SZ"
# pylint: disable=line-too-long
ISO_DATETIME_FORMAT_WITH_TIME_MICROSECONDS_AND_FINAL_Z = (
    "%Y-%m-%dT%H:%M:%S.%fZ"  # noqa
)


OK_STRING = (
    f"{COLORS['fg']['green']}    OK DATA{COLORS['end']} for field"
    f" {COLORS['fg']['blue']}"
    "{field_id}"
    f"{COLORS['end']}"
)


def handle_date_like_values(value):
    """handle datetime-like values coming in different formats"""
    datetime_object = None
    try:
        datetime_object = datetime.strptime(
            value,
            ISO_DATETIME_FORMAT,
        )
    except ValueError:
        pass
    try:
        datetime_object = datetime.strptime(
            value,
            ISO_DATETIME_FORMAT_WITH_TIME,
        )
    except ValueError:
        pass

    try:
        datetime_object = datetime.strptime(
            value,
            ISO_DATETIME_FORMAT_WITH_TIME_AND_FINAL_Z,
        )
    except ValueError:
        pass

    try:
        datetime_object = datetime.strptime(
            value,
            ISO_DATETIME_FORMAT_WITH_TIME_MICROSECONDS_AND_FINAL_Z,
        )
    except ValueError:
        pass

    if datetime_object is not None:
        return datetime_object.date()

    return None


def filter_bounding_boxes(bbox_items, geonetwork_type):
    """filter bounding boxes to use only EEA-wide bounding
    boxes in datasets coming from EEA geonetwork
    """
    log = getLogger(__name__)
    if geonetwork_type == "EEA":
        new_bbox_items = []
        for bbox_item in bbox_items:
            if is_eea(bbox_item):
                new_bbox_items.append(bbox_item)

        log.info(len(new_bbox_items))

        return new_bbox_items

    return bbox_items


class ImportFromGeoNetwork(Service):
    """
    ImportFromGeoNetwork
    """

    def __call__(
        self,
    ):
        # Implement your own actions:

        alsoProvides(
            self.request,
            IDisableCSRFProtection,
        )

        body_json = json.loads(self.request.get("BODY"))
        geonetwork_id = body_json.get("id")
        geonetwork_type = body_json.get("type")
        try:
            self.xml_data = self.get_xml_data(
                geonetwork_id,
                geonetwork_type,
            )
        except Exception:
            return {
                "status": "error",
                "message": "No data found",
            }
        self.json_data = self.get_json_data(
            self.xml_data, geonetwork_id, geonetwork_type
        )

        self.save_data()
        self.json_data["requested_geonetwork_id"] = geonetwork_id
        return json.dumps(self.json_data)

    def get_xml_data(
        self,
        uid,
        geonetwork_type,
    ):
        """
        xml data from geonetwork
        """
        if geonetwork_type == "EEA":
            url = EEA_GEONETWORK_BASE_URL.format(uid=uid)
        elif geonetwork_type == "VITO":
            url = VITO_GEONETWORK_BASE_URL.format(uid=uid)

        print(f"  Downloading {url}")
        result = requests.get(url)
        if result.ok:
            return result.text
        return ""

    def get_json_data(self, xml_data, geo_id, geonetwork_type):
        """
        json data from xml data
        """
        result = {}
        doc = etree.fromstring(xml_data.encode("utf-8"))
        print(f"   Processing XML to get JSON for geonetwork id {geo_id}")

        fields_to_get = [
            # {
            #     "field_id": "dataResourceTitle",
            #     "xml_key": (
            #         "//gmd:identificationInfo/"
            #         "gmd:MD_DataIdentification/gmd:citation/"
            #         "gmd:CI_Citation/gmd:title/gco:CharacterString"
            #     ),
            #     "type": "string",
            # },
            {
                "field_id": "resourceEffective",
                "xml_keys": [
                    # {
                    #     "xml_key": (
                    #         "//gmd:identificationInfo/"
                    #         "gmd:MD_DataIdentification/"
                    #         "gmd:citation/gmd:CI_Citation"
                    #         "/gmd:date/gmd:CI_Date[gmd:dateType/"
                    #         "gmd:CI_DateTypeCode"
                    #         "[@codeListValue='publication']]/"
                    #         "gmd:date/gco:Date"
                    #     ),
                    #     "namespace": NAMESPACES,
                    # },
                    # {
                    #     "xml_key": (
                    #         "//gmd:identificationInfo/"
                    #         "gmd:MD_DataIdentification/"
                    #         "gmd:citation/gmd:CI_Citation"
                    #         "/gmd:date/gmd:CI_Date[gmd:dateType/"
                    #         "gmd:CI_DateTypeCode"
                    #         "[@codeListValue='publication']]/"
                    #         "gmd:date/gco:DateTime"
                    #     ),
                    #     "namespace": NAMESPACES,
                    # },
                    # # Use Creation date if nothing is set in publication
                    # {
                    #     "xml_key": (
                    #         "//gmd:identificationInfo/"
                    #         "gmd:MD_DataIdentification/"
                    #         "gmd:citation/gmd:CI_Citation"
                    #         "/gmd:date/gmd:CI_Date[gmd:dateType/"
                    #         "gmd:CI_DateTypeCode"
                    #         "[@codeListValue='creation']]/"
                    #         "gmd:date/gco:Date"
                    #     ),
                    #     "namespace": NAMESPACES_VITO,
                    # },
                    {
                        "xml_key": "//gmd:dateStamp/gco:DateTime",
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "date",
            },
            {
                "field_id": "resourceModified",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:identificationInfo/"
                            "gmd:MD_DataIdentification/"
                            "gmd:citation/"
                            "gmd:CI_Citation/gmd:date/"
                            "gmd:CI_Date[gmd:dateType/"
                            "gmd:CI_DateTypeCode"
                            "[@codeListValue='revision']]/"
                            "gmd:date/gco:Date"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "date",
            },
            {
                "field_id": "dataResourceAbstract",
                "xml_keys": [
                    {
                        "xml_key": "//gmd:abstract/gco:CharacterString",
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "text",
            },
            {
                "field_id": "geographicCoverage",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:descriptiveKeywords/gmd:MD_Keywords"
                            "[gmd:type/gmd:MD_KeywordTypeCode"
                            "[@codeListValue='place']]/gmd:keyword/"
                            "gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "list",
            },
            {
                "field_id": "accessAndUseLimitationPublic_line",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:resourceConstraints/"
                            "gmd:MD_LegalConstraints/"
                            "gmd:otherConstraints/gmx:Anchor"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
            },
            {
                "field_id": "accessAndUseConstraints",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:resourceConstraints/"
                            "gmd:MD_LegalConstraints/gmd:otherConstraints/"
                            "gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "text",
            },
            {
                "field_id": "qualitySpatialResolution_line",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:spatialResolution/gmd:MD_Resolution/"
                            "gmd:distance/gco:Distance"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "resolution",
                "attribute": "uom",
            },
            {
                "field_id": "classificationTopicCategory",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:MD_DataIdentification/gmd:topicCategory/"
                            "gmd:MD_TopicCategoryCode"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "list",
            },
            {
                "field_id": "geographicBoundingBox",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:extent/gmd:EX_Extent/"
                            "gmd:geographicElement/"
                            "gmd:EX_GeographicBoundingBox"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "json",
            },
            {
                "field_id": "temporalCoverage",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:extent/gmd:EX_Extent/"
                            "gmd:temporalElement/gmd:EX_TemporalExtent/"
                            "gmd:extent/gml:TimePeriod"
                        ),
                        "namespace": NAMESPACES,
                    },
                    {
                        "xml_key": (
                            "//gmd:identificationInfo/"
                            "gmd:MD_DataIdentification/"
                            "gmd:extent/gmd:EX_Extent/"
                            "gmd:temporalElement/gmd:EX_TemporalExtent/"
                            "gmd:extent/gml:TimePeriod"
                        ),
                        "namespace": NAMESPACES_VITO,
                    },
                ],
                "type": "list",
            },
            {
                "field_id": "gemet",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:descriptiveKeywords/gmd:MD_Keywords"
                            "[gmd:thesaurusName/gmd:CI_Citation/"
                            "gmd:title/gco:CharacterString"
                            "[text()='GEMET']]"
                            "/gmd:keyword/gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    },
                    {
                        "xml_key": (
                            "//gmd:descriptiveKeywords/gmd:MD_Keywords"
                            "[gmd:thesaurusName/gmd:CI_Citation/"
                            "gmd:title/gco:CharacterString"
                            "[text()='GEMET - Concepts version 3.0']]"
                            "/gmd:keyword/gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    },
                ],
                "type": "list",
            },
            {
                "field_id": "gemetInspireThemes",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:descriptiveKeywords/gmd:MD_Keywords"
                            "[gmd:thesaurusName/gmd:CI_Citation/"
                            "gmd:title/gmx:Anchor"
                            "[text()="
                            "'GEMET - INSPIRE themes, version 1.0']]"
                            "/gmd:keyword/gmx:Anchor"
                        ),
                        "namespace": NAMESPACES,
                    },
                    {
                        "xml_key": (
                            "//gmd:descriptiveKeywords/gmd:MD_Keywords"
                            "[gmd:thesaurusName/gmd:CI_Citation/"
                            "gmd:title/gco:CharacterString"
                            "[text()="
                            "'GEMET - INSPIRE themes version 1.0']]"
                            "/gmd:keyword/gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    },
                    {
                        "xml_key": (
                            "//gmd:descriptiveKeywords/gmd:MD_Keywords"
                            "[gmd:thesaurusName/gmd:CI_Citation/"
                            "gmd:title/gco:CharacterString"
                            "[text()="
                            "'GEMET - INSPIRE themes, version 1.0']]"
                            "/gmd:keyword/gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    },
                ],
                "type": "list",
            },
            {
                "field_id": "dataResourceType",
                "xml_keys": [
                    {
                        "xml_key": "//gmd:hierarchyLevel/gmd:MD_ScopeCode",
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
                "attribute": "codeListValue",
            },
            {
                "field_id": "responsiblePartyWithRole",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:pointOfContact/gmd:CI_ResponsibleParty"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "contact",
            },
            {
                "field_id": "coordinateReferenceSystemList",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:referenceSystemInfo/"
                            "gmd:MD_ReferenceSystem/"
                            "gmd:referenceSystemIdentifier/"
                            "gmd:RS_Identifier/gmd:code/gmx:Anchor"
                        ),
                        "namespace": NAMESPACES,
                    },
                    {
                        "xml_key": (
                            "//gmd:referenceSystemInfo/"
                            "gmd:MD_ReferenceSystem/"
                            "gmd:referenceSystemIdentifier/"
                            "gmd:RS_Identifier/gmd:code/gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    },
                ],
                "type": "list",
            },
            {
                "field_id": "conformitySpecification",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:report/gmd:DQ_DomainConsistency/"
                            "gmd:result/gmd:DQ_ConformanceResult/"
                            "gmd:specification/"
                            "gmd:CI_Citation/gmd:title/gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "text",
            },
            {
                "field_id": "conformityPass",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:DQ_ConformanceResult/gmd:pass/gco:Boolean"
                        ),
                        "namespace": NAMESPACES,
                    },
                    {
                        "xml_key": (
                            "//gmd:DQ_ConformanceResult"
                            "/gmd:pass[@gco:nilReason]"
                        ),
                        "namespace": NAMESPACES,
                    },
                ],
                "type": "choice",
            },
            {
                "field_id": "qualityLineage",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:lineage/gmd:LI_Lineage/"
                            "gmd:statement/gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "text",
            },
            {
                "field_id": "distributionInfo",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:distributionInfo/gmd:MD_Distribution/"
                            "gmd:transferOptions/"
                            "gmd:MD_DigitalTransferOptions/"
                            "gmd:onLine/gmd:CI_OnlineResource"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "distribution",
            },
            {
                "field_id": "identifier",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:MD_Metadata/"
                            "gmd:fileIdentifier/gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
            },
            {
                "field_id": "point_of_contact_data",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:contact/gmd:CI_ResponsibleParty[gmd:role/"
                            "gmd:CI_RoleCode"
                            "[@codeListValue='pointOfContact']]"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "contact",
            },
            {
                "field_id": "update_frequency",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:resourceMaintenance/"
                            "gmd:MD_MaintenanceInformation/"
                            "gmd:maintenanceAndUpdateFrequency/"
                            "gmd:MD_MaintenanceFrequencyCode"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
                "attribute": "codeListValue",
            },
            {
                "field_id": "distribution_format_list",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:distributionInfo/gmd:MD_Distribution/"
                            "gmd:distributionFormat/"
                            "gmd:MD_Format/gmd:name/gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "list",
            },
            {
                "field_id": "hierarchy_level",
                "xml_keys": [
                    {
                        "xml_key": "//gmd:hierarchyLevel/gmd:MD_ScopeCode",
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
                "attribute": "codeListValue",
            },
            {
                "field_id": "metadata_language",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:MD_Metadata/gmd:language/gmd:LanguageCode"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
                "attribute": "codeListValue",
            },
            {
                "field_id": "character_set",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:MD_Metadata/"
                            "gmd:characterSet/"
                            "gmd:MD_CharacterSetCode"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
                "attribute": "codeListValue",
            },
            {
                "field_id": "date_stamp",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:MD_Metadata/gmd:dateStamp/gco:DateTime"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
            },
            {
                "field_id": "metadata_standard_name",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:MD_Metadata/"
                            "gmd:metadataStandardName/"
                            "gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
            },
            {
                "field_id": "metadata_standard_version",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:MD_Metadata/"
                            "gmd:metadataStandardVersion/"
                            "gco:CharacterString"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
            },
            {
                "field_id": "spatial_representation_type",
                "xml_keys": [
                    {
                        "xml_key": (
                            "//gmd:spatialRepresentationType/"
                            "gmd:MD_SpatialRepresentationTypeCode"
                        ),
                        "namespace": NAMESPACES,
                    }
                ],
                "attribute": "codeListValue",
                "type": "list",
            },
            {
                "field_id": "metadata_wms_url",
                "xml_keys": [
                    {
                        "xml_key": "//gmd:CI_OnlineResource",
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
            },
            {
                "field_id": "metadata_wmts_url",
                "xml_keys": [
                    {
                        "xml_key": "//gmd:CI_OnlineResource",
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
            },
            {
                "field_id": "metadata_rest_api_url",
                "xml_keys": [
                    {
                        "xml_key": "//gmd:CI_OnlineResource",
                        "namespace": NAMESPACES,
                    }
                ],
                "type": "string",
            },
        ]

        # pylint: disable=too-many-nested-blocks
        for field in fields_to_get:
            for key in field.get("xml_keys", []):
                xml_key = key["xml_key"]
                namespace = key["namespace"]
                fields_data = doc.xpath(
                    xml_key,
                    namespaces=namespace,
                )
                if len(fields_data) == 0:
                    print(
                        f"{COLORS['fg']['red']}    No DATA{COLORS['end']} for"
                        f" field {COLORS['fg']['blue']}{field['field_id']}"
                        f"{COLORS['end']} with search key {xml_key}"
                    )
                elif field["field_id"] == "conformityPass":
                    data = fields_data[0]
                    if data.text:
                        value = bool(data.text)
                        value = str(value).lower()
                    else:
                        value = "Null"

                    result[field["field_id"]] = {
                        "data": value,
                        "type": "string",
                    }
                elif field["field_id"] == "geographicBoundingBox":
                    bbox_data = {"items": []}
                    bbox_items = []
                    i = 0
                    for item in fields_data:
                        west = item.xpath(
                            f"{xml_key}/gmd:westBoundLongitude/gco:Decimal",
                            namespaces=NAMESPACES,
                        )
                        east = item.xpath(
                            f"{xml_key}/gmd:eastBoundLongitude/gco:Decimal",
                            namespaces=NAMESPACES,
                        )
                        south = item.xpath(
                            f"{xml_key}/gmd:southBoundLatitude/gco:Decimal",
                            namespaces=NAMESPACES,
                        )
                        north = item.xpath(
                            f"{xml_key}/gmd:northBoundLatitude/gco:Decimal",
                            namespaces=NAMESPACES,
                        )

                        bbox_items.append(
                            {
                                "@id": "geographicBoundingBox" + str(i),
                                "west": west[i].text
                                if west[i] is not None
                                else 0,
                                "east": east[i].text
                                if east[i] is not None
                                else 0,
                                "south": south[i].text
                                if south[i] is not None
                                else 0,
                                "north": north[i].text
                                if north[i] is not None
                                else 0,
                            }
                        )
                        i += 1
                    bbox_data["items"] = filter_bounding_boxes(
                        bbox_items, geonetwork_type
                    )
                    result[field["field_id"]] = {
                        "data": bbox_data,
                        "type": field["type"],
                    }
                    print(OK_STRING.format(field_id=field["field_id"]))

                elif field["field_id"] == "temporalCoverage":
                    temporalExtent = []
                    item = fields_data[0]
                    start = item.xpath(
                        "gml:beginPosition",
                        namespaces=namespace,
                    )

                    end = item.xpath(
                        "gml:endPosition",
                        namespaces=namespace,
                    )

                    dt_start_obj = None
                    dt_end_obj = None
                    if start[0].text:
                        dt_start_obj = handle_date_like_values(start[0].text)

                        result["temporalExtentStart"] = {
                            "data": start[0].text,
                            "type": "string",
                        }
                    if end[0].text:
                        dt_end_obj = handle_date_like_values(end[0].text)
                        result["temporalExtentEnd"] = {
                            "data": end[0].text,
                            "type": "string",
                        }
                    if dt_start_obj:
                        if not dt_end_obj:
                            dt_end_obj = datetime.now()
                        for year in range(
                            dt_start_obj.year,
                            dt_end_obj.year + 1,
                        ):
                            temporalExtent.append(str(year))
                        result[field["field_id"]] = {
                            "data": temporalExtent,
                            "type": field["type"],
                        }
                        print(OK_STRING.format(field_id=field["field_id"]))
                    else:
                        print(f"    ERROR DATA for field {field['field_id']}")
                elif field["type"] == "contact":
                    contact_data = {"items": []}
                    contact_items = []
                    i = 0
                    for item in fields_data:
                        organisationName = item.xpath(
                            f"{xml_key}/gmd:organisationName/"
                            "gco:CharacterString",
                            namespaces=namespace,
                        )
                        deliveryPoint = item.xpath(
                            f"{xml_key}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:deliveryPoint/"
                            "gco:CharacterString",
                            namespaces=namespace,
                        )
                        city = item.xpath(
                            f"{xml_key}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:city/gco:CharacterString",
                            namespaces=namespace,
                        )
                        administrativeArea = item.xpath(
                            f"{xml_key}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:administrativeArea/"
                            "gco:CharacterString",
                            namespaces=namespace,
                        )
                        postalCode = item.xpath(
                            f"{xml_key}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:postalCode/"
                            "gco:CharacterString",
                            namespaces=namespace,
                        )
                        country = item.xpath(
                            f"{xml_key}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:country/gco:CharacterString",
                            namespaces=namespace,
                        )
                        electronicMailAddress = item.xpath(
                            f"{xml_key}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:electronicMailAddress/"
                            "gco:CharacterString",
                            namespaces=namespace,
                        )
                        url = item.xpath(
                            f"{xml_key}/gmd:onlineResource/"
                            "gmd:CI_OnlineResource/"
                            "gmd:linkage/gmd:URL",
                            namespaces=namespace,
                        )
                        urlTitle = item.xpath(
                            f"{xml_key}/gmd:onlineResource/"
                            "gmd:CI_OnlineResource/"
                            "gmd:name/gco:CharacterString",
                            namespaces=namespace,
                        )
                        roleCode = item.xpath(
                            f"{xml_key}/gmd:role/gmd:CI_RoleCode",
                            namespaces=namespace,
                        )
                        contact_items.append(
                            {
                                "@id": "contactInfo" + str(i),
                                "organisationName": organisationName[i].text
                                if len(organisationName) > i
                                else "",
                                "deliveryPoint": deliveryPoint[i].text
                                if len(deliveryPoint) > i
                                else "",
                                "city": city[i].text if len(city) > i else "",
                                "administrativeArea": administrativeArea[
                                    i
                                ].text
                                if len(administrativeArea) > i
                                else "",
                                "postalCode": postalCode[i].text
                                if len(postalCode) > i
                                else "",
                                "country": country[i].text
                                if len(country) > i
                                else "",
                                "electronicMailAddress": electronicMailAddress[
                                    i
                                ].text
                                if len(electronicMailAddress) > i
                                else "",
                                "url": url[i].text if len(url) > i else "",
                                "urlTitle": urlTitle[i].text
                                if len(urlTitle) > i
                                else "",
                                "roleCode": roleCode[i].attrib.get(
                                    "codeListValue"
                                )
                                if len(roleCode) > i
                                else "",
                            }
                        )
                        i += 1
                    contact_data["items"] = contact_items
                    result[field["field_id"]] = {
                        "data": contact_data,
                        "type": field["type"],
                    }

                    print(OK_STRING.format(field_id=field["field_id"]))

                elif field["type"] == "distribution":
                    distribution_data = {"items": []}
                    distribution_items = []
                    i = 0
                    for item in fields_data:
                        resourceLocator = item.xpath(
                            xml_key + "/gmd:linkage/gmd:URL",
                            namespaces=namespace,
                        )
                        services = item.xpath(
                            f"{xml_key}/gmd:protocol/gco:CharacterString",
                            namespaces=namespace,
                        )
                        distribution_items.append(
                            {
                                "@id": "distributionInfo" + str(i),
                                "resourceLocator": resourceLocator[i].text
                                if len(resourceLocator) > i
                                else "",
                                "services": services[i].text
                                if len(services) > i
                                else "",
                            }
                        )
                        i = +1
                    distribution_data["items"] = distribution_items
                    result[field["field_id"]] = {
                        "data": distribution_data,
                        "type": field["type"],
                    }
                    print(OK_STRING.format(field_id=field["field_id"]))

                elif field["type"] == "resolution":
                    item = fields_data[0]
                    resolution = item.attrib.get(field.get("attribute"))
                    # pylint: disable=line-too-long
                    if (resolution.startswith("http") and resolution.find("#") != -1):  # noqa: E501
                        resolution = resolution.split("#")[1]
                    result[field["field_id"]] = {
                        "data": f"{item.text} {resolution}",
                        "type": field["type"],
                    }
                elif field["field_id"] == "metadata_wms_url":
                    for online_resource in fields_data:
                        character_strings = online_resource.xpath(
                            ".//gmd:protocol/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        for character_string in character_strings:
                            if character_string.text == "OGC:WMS":
                                result[field["field_id"]] = {
                                    "data": online_resource.xpath(
                                        ".//gmd:linkage/gmd:URL",
                                        namespaces=NAMESPACES,
                                    )[0].text,
                                    "type": "string",
                                }
                    if result.get(field["field_id"]) is not None:
                        print(OK_STRING.format(field_id=field["field_id"]))
                    else:
                        print(
                            f"{COLORS['fg']['red']}    No DATA{COLORS['end']} "
                            f"for field {COLORS['fg']['blue']}"
                            f"{field['field_id']} {COLORS['end']} with search "
                            f"key {xml_key}"
                        )

                elif field["field_id"] == "metadata_wmts_url":
                    for online_resource in fields_data:
                        character_strings = online_resource.xpath(
                            ".//gmd:protocol/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        for character_string in character_strings:
                            if character_string.text == "OGC:WMTS":
                                result[field["field_id"]] = {
                                    "data": online_resource.xpath(
                                        ".//gmd:linkage/gmd:URL",
                                        namespaces=NAMESPACES,
                                    )[0].text,
                                    "type": "string",
                                }
                    if result.get(field["field_id"]) is not None:
                        print(OK_STRING.format(field_id=field["field_id"]))
                    else:
                        print(
                            f"{COLORS['fg']['red']}    No DATA{COLORS['end']} "
                            f"for field {COLORS['fg']['blue']}"
                            f"{field['field_id']} {COLORS['end']} with search "
                            f"key {xml_key}"
                        )

                elif field["field_id"] == "metadata_rest_api_url":
                    for online_resource in fields_data:
                        character_strings = online_resource.xpath(
                            ".//gmd:protocol/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        for character_string in character_strings:
                            if character_string.text == "ESRI:REST":
                                result[field["field_id"]] = {
                                    "data": online_resource.xpath(
                                        ".//gmd:linkage/gmd:URL",
                                        namespaces=NAMESPACES,
                                    )[0].text,
                                    "type": "string",
                                }
                    if result.get(field["field_id"]) is not None:
                        print(OK_STRING.format(field_id=field["field_id"]))
                    else:
                        print(
                            f"{COLORS['fg']['red']}    No DATA{COLORS['end']} "
                            f"for field {COLORS['fg']['blue']}"
                            f"{field['field_id']} {COLORS['end']} with search "
                            f"key {xml_key}"
                        )

                elif len(fields_data) == 1 and not field["type"] == "list":
                    item = fields_data[0]
                    if field.get("attribute"):
                        data = item.attrib.get(field.get("attribute"))
                    else:
                        data = item.text
                    result[field["field_id"]] = {
                        "data": data,
                        "type": field["type"],
                    }
                    print(OK_STRING.format(field_id=field["field_id"]))

                elif len(fields_data) > 1 and not field["type"] == "list":
                    fields_data_array = []
                    for field_data in fields_data:
                        fields_data_array.append(field_data.text)
                    result[field["field_id"]] = {
                        "data": ", ".join(fields_data_array),
                        "type": field["type"],
                    }
                    print(OK_STRING.format(field_id=field["field_id"]))

                else:
                    field_attribute = field.get("attribute", None)
                    if field_attribute is None:
                        result[field["field_id"]] = {
                            "data": [item.text for item in fields_data],
                            "type": field["type"],
                        }
                    else:
                        result[field["field_id"]] = {
                            "data": [
                                item.attrib.get(field_attribute)
                                for item in fields_data
                            ],
                            "type": field["type"],
                        }

                    # print(
                    #     f"    OK DATA for {field['type']} field"
                    #     f" {field['field_id']}"
                    # )
                    print(OK_STRING.format(field_id=field["field_id"]))

        return result

    def save_data(
        self,
    ):
        """
        Save data into Plone
        """

        for key, value in self.json_data.items():
            data = value["data"]
            field_type = value["type"]
            if field_type == "text":
                setattr(
                    self.context,
                    key,
                    RichTextValue(
                        data,
                        "text/html",
                        "text/x-html-safe",
                    ),
                )
            elif field_type == "date":
                try:
                    date_data = handle_date_like_values(data)
                    setattr(
                        self.context,
                        key,
                        date_data,
                    )
                except Exception:
                    continue
            else:
                try:
                    setattr(
                        self.context,
                        key,
                        data,
                    )
                except Exception:
                    continue

        self.context.reindexObject()
