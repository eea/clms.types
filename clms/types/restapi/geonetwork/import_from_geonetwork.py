# -*- coding: utf-8 -*-
"""
Import from geonetwork
"""

import json
from datetime import datetime

import requests
from lxml import etree
from plone.app.textfield.value import RichTextValue
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.services import Service
from zope.interface import alsoProvides

from clms.types.utils import (
    EEA_GEONETWORK_BASE_URL,
    NAMESPACES,
    VITO_GEONETWORK_BASE_URL,
)

ISO_DATETIME_FORMAT = "%Y-%m-%d"


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
            self.xml_data,
            geonetwork_id,
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
        print(f"    Getting {url}")
        result = requests.get(url)
        if result.ok:
            return result.text
        return ""

    def get_json_data(
        self,
        xml_data,
        geo_id,
    ):
        """
        json data from xml data
        """
        result = {}
        doc = etree.fromstring(xml_data.encode("utf-8"))
        print(f"    Getting JSON DATA for {geo_id}")

        fields_to_get = [
            {
                "field_id": "dataResourceTitle",
                "xml_key": (
                    "//gmd:identificationInfo/"
                    "gmd:MD_DataIdentification/gmd:citation/"
                    "gmd:CI_Citation/gmd:title/gco:CharacterString"
                ),
                "type": "string",
            },
            {
                "field_id": "resourceEffective",
                "xml_key": (
                    "//gmd:identificationInfo/"
                    "gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation"
                    "/gmd:date/gmd:CI_Date[gmd:dateType/"
                    "gmd:CI_DateTypeCode[@codeListValue='publication']]/"
                    "gmd:date/gco:Date"
                ),
                "type": "date",
            },
            {
                "field_id": "resourceModified",
                "xml_key": (
                    "//gmd:identificationInfo/"
                    "gmd:MD_DataIdentification/gmd:citation/"
                    "gmd:CI_Citation/gmd:date/gmd:CI_Date[gmd:dateType/"
                    "gmd:CI_DateTypeCode[@codeListValue='revision']]/"
                    "gmd:date/gco:Date"
                ),
                "type": "date",
            },
            {
                "field_id": "dataResourceAbstract",
                "xml_key": "//gmd:abstract/gco:CharacterString",
                "type": "text",
            },
            # {
            #     "field_id": "keywords",
            #     "xml_key": "",
            #     # "xml_key": "//gmd:descriptiveKeywords/" \
            #       "gmd:MD_Keywords/gmd:keyword/gco:CharacterString",
            #     "type": "string",
            # },
            {
                "field_id": "geographicCoverage",
                "xml_key": (
                    "//gmd:descriptiveKeywords/gmd:MD_Keywords"
                    "[gmd:type/gmd:MD_KeywordTypeCode"
                    "[@codeListValue='place']]/gmd:keyword/"
                    "gco:CharacterString"
                ),
                "type": "json",
            },
            {
                "field_id": "accessAndUseLimitationPublic_line",
                "xml_key": (
                    "//gmd:resourceConstraints/"
                    "gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor"
                ),
                "type": "string",
            },
            {
                "field_id": "accessAndUseConstraints",
                "xml_key": (
                    "//gmd:resourceConstraints/"
                    "gmd:MD_LegalConstraints/gmd:otherConstraints/"
                    "gco:CharacterString"
                ),
                "type": "text",
            },
            {
                "field_id": "qualitySpatialResolution_line",
                "xml_key": (
                    "//gmd:spatialResolution/gmd:MD_Resolution/"
                    "gmd:distance/gco:Distance"
                ),
                "type": "resolution",
                "attribute": "uom",
            },
            {
                "field_id": "classificationTopicCategory",
                "xml_key": (
                    "//gmd:MD_DataIdentification/gmd:topicCategory/"
                    "gmd:MD_TopicCategoryCode"
                ),
                "type": "list",
            },
            {
                "field_id": "geographicBoundingBox",
                "xml_key": (
                    "//gmd:extent/gmd:EX_Extent/"
                    "gmd:geographicElement/gmd:EX_GeographicBoundingBox"
                ),
                "type": "json",
            },
            {
                "field_id": "temporalCoverage",
                "xml_key": (
                    "//gmd:extent/gmd:EX_Extent/"
                    "gmd:temporalElement/gmd:EX_TemporalExtent/"
                    "gmd:extent/gml:TimePeriod"
                ),
                "type": "list",
            },
            {
                "field_id": "gemet",
                "xml_key": (
                    "//gmd:descriptiveKeywords/gmd:MD_Keywords"
                    "[gmd:thesaurusName/gmd:CI_Citation/"
                    "gmd:title/gco:CharacterString"
                    "[contains(text(),'GEMET')]]"
                    "/gmd:keyword/gco:CharacterString"
                ),
                "type": "list",
            },
            {
                "field_id": "gemetInspireThemes",
                "xml_key": (
                    "//gmd:descriptiveKeywords/gmd:MD_Keywords"
                    "[gmd:thesaurusName/gmd:CI_Citation/"
                    "gmd:title/gmx:Anchor"
                    "[@xlink:href='http://inspire.ec.europa.eu/theme']]"
                    "/gmd:keyword/gco:CharacterString"
                ),
                "if_not_xml_key": (
                    "//gmd:descriptiveKeywords/gmd:MD_Keywords"
                    "[gmd:thesaurusName/gmd:CI_Citation/"
                    "gmd:title/gco:CharacterString"
                    "[contains(text(),"
                    "'GEMET - INSPIRE themes, version 1.0')]]"
                    "/gmd:keyword/gco:CharacterString"
                ),
                "type": "list",
            },
            {
                "field_id": "dataResourceType",
                "xml_key": "//gmd:hierarchyLevel/gmd:MD_ScopeCode",
                "type": "string",
                "attribute": "codeListValue",
            },
            {
                "field_id": "responsiblePartyWithRole",
                "xml_key": "//gmd:pointOfContact/gmd:CI_ResponsibleParty",
                "type": "contact",
            },
            {
                "field_id": "coordinateReferenceSystemList",
                "xml_key": (
                    "//gmd:referenceSystemInfo/"
                    "gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
                    "gmd:RS_Identifier/gmd:code/gmx:Anchor"
                ),
                "if_not_xml_key": (
                    "//gmd:referenceSystemInfo/"
                    "gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
                    "gmd:RS_Identifier/gmd:code/gco:CharacterString"
                ),
                "type": "list",
            },
            {
                "field_id": "conformitySpecification",
                "xml_key": (
                    "//gmd:report/gmd:DQ_DomainConsistency/"
                    "gmd:result/gmd:DQ_ConformanceResult/gmd:specification/"
                    "gmd:CI_Citation/gmd:title/gco:CharacterString"
                ),
                "type": "text",
            },
            {
                "field_id": "conformityPass",
                "xml_key": (
                    "//gmd:DQ_DomainConsistency/gmd:result/"
                    "gmd:DQ_ConformanceResult/gmd:pass/gco:Boolean"
                ),
                "type": "choice",
            },
            {
                "field_id": "qualityLineage",
                "xml_key": (
                    "//gmd:lineage/gmd:LI_Lineage/"
                    "gmd:statement/gco:CharacterString"
                ),
                "type": "text",
            },
            {
                "field_id": "distributionInfo",
                "xml_key": (
                    "//gmd:distributionInfo/gmd:MD_Distribution/"
                    "gmd:transferOptions/gmd:MD_DigitalTransferOptions/"
                    "gmd:onLine/gmd:CI_OnlineResource"
                ),
                "type": "distribution",
            },
            {
                "field_id": "identifier",
                "xml_key": (
                    "//gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString"
                ),
                "type": "string",
            },
            {
                "field_id": "point_of_contact_data",
                "xml_key": (
                    "//gmd:contact/gmd:CI_ResponsibleParty[gmd:role/"
                    "gmd:CI_RoleCode[@codeListValue='pointOfContact']]"
                ),
                "type": "contact",
            },
            {
                "field_id": "update_frequency",
                "xml_key": (
                    "//gmd:resourceMaintenance/"
                    "gmd:MD_MaintenanceInformation/"
                    "gmd:maintenanceAndUpdateFrequency/"
                    "gmd:MD_MaintenanceFrequencyCode"
                ),
                "type": "string",
                "attribute": "codeListValue",
            },
            {
                "field_id": "distribution_format_list",
                "xml_key": (
                    "//gmd:distributionInfo/gmd:MD_Distribution/"
                    "gmd:distributionFormat/"
                    "gmd:MD_Format/gmd:name/gco:CharacterString"
                ),
                "type": "list",
            },
            {
                "field_id": "hierarchy_level",
                "xml_key": "//gmd:hierarchyLevel/gmd:MD_ScopeCode",
                "type": "string",
                "attribute": "codeListValue",
            },
            {
                "field_id": "metadata_language",
                "xml_key": "//gmd:MD_Metadata/gmd:language/gmd:LanguageCode",
                "type": "string",
                "attribute": "codeListValue",
            },
            {
                "field_id": "character_set",
                # pylint: disable=line-too-long
                "xml_key": "//gmd:MD_Metadata/gmd:characterSet/gmd:MD_CharacterSetCode",  # noqa: E501
                "type": "string",
                "attribute": "codeListValue",
            },
            {
                "field_id": "date_stamp",
                "xml_key": "//gmd:MD_Metadata/gmd:dateStamp/gco:DateTime",
                "type": "string",
            },
            {
                "field_id": "metadata_standard_name",
                # pylint: disable=line-too-long
                "xml_key": "//gmd:MD_Metadata/gmd:metadataStandardName/gco:CharacterString",  # noqa: E501
                "type": "string",
            },
            {
                "field_id": "metadata_standard_version",
                # pylint: disable=line-too-long
                "xml_key": "//gmd:MD_Metadata/gmd:metadataStandardVersion/gco:CharacterString",  # noqa: E501
                "type": "string",
            },
        ]

        for field in fields_to_get:
            if field.get("xml_key"):
                fields_data = doc.xpath(
                    field["xml_key"],
                    namespaces=NAMESPACES,
                )
                if len(fields_data) == 0 and field.get("if_not_xml_key"):
                    fields_data = doc.xpath(
                        field["if_not_xml_key"],
                        namespaces=NAMESPACES,
                    )
                    if len(fields_data) > 0:
                        result[field["field_id"]] = {
                            "data": [item.text for item in fields_data],
                            "type": field["type"],
                        }
                        print(
                            f"    OK DATA for {field['type']} field"
                            f" {field['field_id']}"
                        )
                    else:
                        print(
                            "    WARNING!!! No DATA for field"
                            f" {field['field_id']} with search keys"
                            f" {field['xml_key']} first attempt with 0 results"
                            f" and {field['if_not_xml_key']}"
                        )
                elif len(fields_data) == 0:
                    print(
                        "    WARNING!!! No DATA for field"
                        f" {field['field_id']} with search key"
                        f" {field['xml_key']}"
                    )
                elif field["field_id"] == "geographicBoundingBox":
                    bbox_data = {"items": []}
                    bbox_items = []
                    i = 0
                    for item in fields_data:
                        west = item.xpath(
                            f"{field['xml_key']}/gmd:westBoundLongitude"
                            "/gco:Decimal",
                            namespaces=NAMESPACES,
                        )
                        east = item.xpath(
                            f"{field['xml_key']}/gmd:eastBoundLongitude"
                            "/gco:Decimal",
                            namespaces=NAMESPACES,
                        )
                        south = item.xpath(
                            f"{field['xml_key']}/gmd:southBoundLatitude"
                            "/gco:Decimal",
                            namespaces=NAMESPACES,
                        )
                        north = item.xpath(
                            f"{field['xml_key']}/gmd:northBoundLatitude"
                            "/gco:Decimal",
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
                    bbox_data["items"] = bbox_items
                    result[field["field_id"]] = {
                        "data": bbox_data,
                        "type": field["type"],
                    }
                    print(f"    OK DATA for field {field['field_id']}")
                elif field["field_id"] == "geographicCoverage":
                    geo_data = {}
                    geo_items = []
                    for item in fields_data:
                        geo_items.append(
                            {
                                "label": item.text,
                                "value": item.text.lower(),
                            }
                        )
                    geo_data["geolocation"] = geo_items
                    result[field["field_id"]] = {
                        "data": geo_data,
                        "type": field["type"],
                    }
                    print(f"    OK DATA for field {field['field_id']}")
                elif field["field_id"] == "temporalCoverage":
                    temporalExtent = []
                    item = fields_data[0]
                    start = item.xpath(
                        "gml:beginPosition",
                        namespaces=NAMESPACES,
                    )
                    end = item.xpath(
                        "gml:endPosition",
                        namespaces=NAMESPACES,
                    )
                    dt_start_obj = None
                    dt_end_obj = None
                    if start[0].text:
                        dt_start_obj = datetime.strptime(
                            start[0].text,
                            ISO_DATETIME_FORMAT,
                        )
                        result["temporalExtentStart"] = {
                            "data": start[0].text,
                            "type": "string",
                        }
                    if end[0].text:
                        dt_end_obj = datetime.strptime(
                            end[0].text,
                            ISO_DATETIME_FORMAT,
                        )
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
                        print(f"    OK DATA for field {field['field_id']}")
                    else:
                        print(f"    ERROR DATA for field {field['field_id']}")
                elif field["type"] == "contact":
                    contact_data = {"items": []}
                    contact_items = []
                    i = 0
                    for item in fields_data:
                        organisationName = item.xpath(
                            f"{field['xml_key']}/gmd:organisationName/"
                            "gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        deliveryPoint = item.xpath(
                            f"{field['xml_key']}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:deliveryPoint/"
                            "gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        city = item.xpath(
                            f"{field['xml_key']}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:city/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        administrativeArea = item.xpath(
                            f"{field['xml_key']}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:administrativeArea/"
                            "gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        postalCode = item.xpath(
                            f"{field['xml_key']}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:postalCode/"
                            "gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        country = item.xpath(
                            f"{field['xml_key']}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:country/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        electronicMailAddress = item.xpath(
                            f"{field['xml_key']}/gmd:contactInfo/"
                            "gmd:CI_Contact/gmd:address/"
                            "gmd:CI_Address/gmd:electronicMailAddress/"
                            "gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        url = item.xpath(
                            f"{field['xml_key']}/gmd:onlineResource/"
                            "gmd:CI_OnlineResource/"
                            "gmd:linkage/gmd:URL",
                            namespaces=NAMESPACES,
                        )
                        urlTitle = item.xpath(
                            f"{field['xml_key']}/gmd:onlineResource/"
                            "gmd:CI_OnlineResource/"
                            "gmd:name/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        roleCode = item.xpath(
                            f"{field['xml_key']}/gmd:role/gmd:CI_RoleCode",
                            namespaces=NAMESPACES,
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

                    print(f"    OK DATA for contact field {field['field_id']}")
                elif field["type"] == "distribution":
                    distribution_data = {"items": []}
                    distribution_items = []
                    i = 0
                    for item in fields_data:
                        resourceLocator = item.xpath(
                            field["xml_key"] + "/gmd:linkage/gmd:URL",
                            namespaces=NAMESPACES,
                        )
                        services = item.xpath(
                            f"{field['xml_key']}/gmd:protocol/"
                            "gco:CharacterString",
                            namespaces=NAMESPACES,
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
                    print(f"    OK DATA for field {field['field_id']}")
                elif field["type"] == "resolution":
                    item = fields_data[0]
                    resolution = item.attrib.get(field.get("attribute"))
                    # pylint: disable=line-too-long
                    if (
                        resolution.startswith("http")
                        and resolution.find("#") != -1  # noqa: E501
                    ):  # noqa: E501
                        resolution = resolution.split("#")[1]
                    result[field["field_id"]] = {
                        "data": f"{item.text} {resolution}",
                        "type": field["type"],
                    }
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
                    print(f"    OK DATA for field {field['field_id']}")
                elif len(fields_data) > 1 and not field["type"] == "list":
                    fields_data_array = []
                    for field_data in fields_data:
                        fields_data_array.append(field_data.text)
                    result[field["field_id"]] = {
                        "data": ", ".join(fields_data_array),
                        "type": field["type"],
                    }
                    print(f"    OK DATA for field {field['field_id']}")
                else:
                    result[field["field_id"]] = {
                        "data": [item.text for item in fields_data],
                        "type": field["type"],
                    }
                    print(
                        f"    OK DATA for {field['type']} field"
                        f" {field['field_id']}"
                    )
            else:
                result[field["field_id"]] = {
                    "data": "### NOT TESTED ###",
                    "type": field["type"],
                }
                print(f"    No XML Key for {field['field_id']}")
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
                    date_data = datetime.strptime(
                        data,
                        ISO_DATETIME_FORMAT,
                    )
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
