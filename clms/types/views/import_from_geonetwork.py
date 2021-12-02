# -*- coding: utf-8 -*-
"""
Import from geonetwork
"""

from datetime import datetime
from xml.etree import ElementTree as ET

import requests
from lxml import etree
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

# from plone.app.textfield.value import RichTextValue
# created_product.text = RichTextValue(product[u'Text'],'text/html', 'text/html')

EEA_GEONETWORK_BASE_URL = "https://sdi.eea.europa.eu/catalogue/copernicus/api/records/{uid}/formatters/xml?approved=true"

NAMESPACES = {
    "gmd": "http://www.isotc211.org/2005/gmd",
    "gco": "http://www.isotc211.org/2005/gco",
    "wms_default": "http://www.opengis.net/wms",
    "srv": "http://www.isotc211.org/2005/srv",
    "gmx": "http://www.isotc211.org/2005/gmx",
    "gts": "http://www.isotc211.org/2005/gts",
    "gsr": "http://www.isotc211.org/2005/gsr",
    "gmi": "http://www.isotc211.org/2005/gmi",
    "gml": "http://www.opengis.net/gml/3.2",
    "xlink": "http://www.w3.org/1999/xlink",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "schemaLocation": "http://www.isotc211.org/2005/gmd http://schemas.opengis.net/csw/2.0.2/profiles/apiso/1.0.0/apiso.xsd",
}


class InvalidMetadata(Exception):
    """
    Invalid Metadata
    """


class ImportFromGeoNetworkView(BrowserView):
    """
    ImportFromGeoNetworkView
    """

    def __call__(self):
        # Implement your own actions:

        alsoProvides(self.request, IDisableCSRFProtection)
        self.geonetwork_ids = self.extract_ids_from_field(
            self.context.geonetwork_identifiers
        )
        self.xml_data = self.get_xml_data(self.geonetwork_ids[0])
        self.json_data = self.get_json_data(
            self.xml_data, self.geonetwork_ids[0]
        )
        return self.index()

    def extract_ids_from_field(self, jsondata):
        """
        extract ids from plone field
        """
        result = []
        for item in jsondata.get("items", []):
            result.append(item.get("id"))
        return result

    def get_xml_data(self, uid):
        """
        xml data from geonetwork
        """
        url = EEA_GEONETWORK_BASE_URL.format(uid=uid)
        print(f"    Getting {url}")
        result = requests.get(url)
        if result.ok:
            return result.text
        return ""

    def get_json_data(self, xml_data, geo_id):
        """
        json data from xml data
        """
        result = {}
        doc = etree.fromstring(xml_data.encode("utf-8"))
        print(f"    Getting JSON DATA for {geo_id}")

        fields_to_get = [
            {
                "field_id": "dataResourceTitle",
                "xml_key": "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString",
                "type": "string",
            },
            {
                "field_id": "resourceEffective",
                "xml_key": "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date[gmd:dateType/gmd:CI_DateTypeCode[@codeListValue='publication']]/gmd:date/gco:Date",
                "type": "string",
            },
            {
                "field_id": "resourceModified",
                "xml_key": "//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date[gmd:dateType/gmd:CI_DateTypeCode[@codeListValue='revision']]/gmd:date/gco:Date",
                "type": "string",
            },
            {
                "field_id": "dataResourceAbstract",
                "xml_key": "//gmd:abstract/gco:CharacterString",
                "type": "string",
            },
            {
                "field_id": "keywords",
                "xml_key": "",
                # "xml_key": "//gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString",
                "type": "string",
            },
            {
                "field_id": "geographicCoverage",
                "xml_key": "",
                "type": "string",
            },
            {
                "field_id": "accessAndUseLimitationPublic",
                "xml_key": "//gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor",
                "type": "text",
            },
            {
                "field_id": "accessAndUseConstraints",
                "xml_key": "//gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString",
                "type": "text",
            },
            {
                "field_id": "qualitySpatialResolution",
                "xml_key": "//gmd:supplementalInformation/gco:CharacterString",
                "type": "text",
            },
            {
                "field_id": "classificationTopicCategory",
                "xml_key": "//gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode",
                "type": "list",
            },
            {
                "field_id": "geographicBoundingBox",
                "xml_key": "//gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox",
                "type": "json",
            },
            {
                "field_id": "temporalExtent",
                "xml_key": "//gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod",
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
                "field_id": "responsibleParty",
                "xml_key": "",
                "type": "text",
            },
            {
                "field_id": "responsiblePartyRole",
                "xml_key": "",
                "type": "text",
            },
            {
                "field_id": "coordinateReferenceSystem",
                "xml_key": "//gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gmx:Anchor",
                "type": "list",
            },
            {
                "field_id": "conformitySpecification",
                "xml_key": "//gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:specification/gmd:CI_Citation/gmd:title/gco:CharacterString",
                "type": "text",
            },
            {
                "field_id": "conformityPass",
                "xml_key": "//gmd:DQ_ConformanceResult/gmd:pass/gco:Boolean",
                "type": "choice",
            },
            {
                "field_id": "qualityLineage",
                "xml_key": "//gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString",
                "type": "text",
            },
            {
                "field_id": "distributionInfo",
                "xml_key": "//gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource",
                "type": "distribution",
            },
            {
                "field_id": "dataResourceLocator",
                "xml_key": "",
                "type": "string",
            },
            {"field_id": "dataServices", "xml_key": "", "type": "text"},
            {
                "field_id": "identifier",
                "xml_key": "//gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString",
                "type": "string",
            },
            {
                "field_id": "point_of_contact_data",
                "xml_key": "//gmd:contact/gmd:CI_ResponsibleParty[gmd:role/gmd:CI_RoleCode[@codeListValue='pointOfContact']]",
                "type": "contact",
            },
            {
                "field_id": "update_frequency",
                "xml_key": "//gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode",
                "type": "text",
                "attribute": "codeListValue",
            },
            {
                "field_id": "distribution_format",
                "xml_key": "//gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:name/gco:CharacterString",
                "type": "text",
            },
            {
                "field_id": "hierarchy_level",
                "xml_key": "//gmd:hierarchyLevel/gmd:MD_ScopeCode",
                "type": "string",
                "attribute": "codeListValue",
            },
        ]

        for field in fields_to_get:
            if field.get("xml_key"):
                fields_data = doc.xpath(
                    field["xml_key"], namespaces=NAMESPACES
                )
                if len(fields_data) == 0:
                    result[field["field_id"]] = {
                        "data": "Null",
                        "type": field["type"],
                    }
                    print(
                        f"    WARNING!!! No DATA for field {field['field_id']} with search key {field['xml_key']}"
                    )
                elif field["field_id"] == "geographicBoundingBox":
                    bbox_data = {"items": []}
                    bbox_items = []
                    i = 0
                    for item in fields_data:
                        west = item.xpath(
                            field["xml_key"]
                            + "/gmd:westBoundLongitude/gco:Decimal",
                            namespaces=NAMESPACES,
                        )
                        east = item.xpath(
                            field["xml_key"]
                            + "/gmd:eastBoundLongitude/gco:Decimal",
                            namespaces=NAMESPACES,
                        )
                        south = item.xpath(
                            field["xml_key"]
                            + "/gmd:southBoundLatitude/gco:Decimal",
                            namespaces=NAMESPACES,
                        )
                        north = item.xpath(
                            field["xml_key"]
                            + "/gmd:northBoundLatitude/gco:Decimal",
                            namespaces=NAMESPACES,
                        )
                        bbox_items.append(
                            {
                                "@id": "geographicBoundingBox" + str(i),
                                "west": west[i].text if west[i] else 0,
                                "east": east[i].text if east[i] else 0,
                                "south": south[i].text if south[i] else 0,
                                "north": north[i].text if north[i] else 0,
                            }
                        )
                        i += 1
                    bbox_data["items"] = bbox_items
                    result[field["field_id"]] = {
                        "data": bbox_data,
                        "type": field["type"],
                    }
                    print(f"    OK DATA for field {field['field_id']}")
                elif field["type"] == "contact":
                    contact_data = {"items": []}
                    contact_items = []
                    i = 0
                    for item in fields_data:
                        organisationName = item.xpath(
                            field["xml_key"]
                            + "/gmd:organisationName/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        deliveryPoint = item.xpath(
                            field["xml_key"]
                            + "/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        city = item.xpath(
                            field["xml_key"]
                            + "/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        administrativeArea = item.xpath(
                            field["xml_key"]
                            + "/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        postalCode = item.xpath(
                            field["xml_key"]
                            + "/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        country = item.xpath(
                            field["xml_key"]
                            + "/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        electronicMailAddress = item.xpath(
                            field["xml_key"]
                            + "/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        url = item.xpath(
                            field["xml_key"]
                            + "/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL",
                            namespaces=NAMESPACES,
                        )
                        urlTitle = item.xpath(
                            field["xml_key"]
                            + "/gmd:onlineResource/gmd:CI_OnlineResource/gmd:name/gco:CharacterString",
                            namespaces=NAMESPACES,
                        )
                        roleCode = item.xpath(
                            field["xml_key"] + "/gmd:role/gmd:CI_RoleCode",
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
                            field["xml_key"]
                            + "/gmd:protocol/gco:CharacterString",
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
                    distribution_data["items"] = distribution_items
                    result[field["field_id"]] = {
                        "data": distribution_data,
                        "type": field["type"],
                    }
                    print(f"    OK DATA for field {field['field_id']}")

                elif len(fields_data) == 1 and not field["type"] == "list":
                    item = fields_data[0]
                    # if field["field_id"] == "point_of_contact":
                    #     organisationName = item.xpath(
                    #         "//gmd:organisationName/gco:CharacterString",
                    #         namespaces=NAMESPACES,
                    #     )
                    #     deliveryPoint = item.xpath(
                    #         "//gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString",
                    #         namespaces=NAMESPACES,
                    #     )
                    #     city = item.xpath(
                    #         "//gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString",
                    #         namespaces=NAMESPACES,
                    #     )
                    #     administrativeArea = item.xpath(
                    #         "//gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString",
                    #         namespaces=NAMESPACES,
                    #     )
                    #     postalCode = item.xpath(
                    #         "//gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString",
                    #         namespaces=NAMESPACES,
                    #     )
                    #     country = item.xpath(
                    #         "//gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString",
                    #         namespaces=NAMESPACES,
                    #     )
                    #     electronicMailAddress = item.xpath(
                    #         "//gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString",
                    #         namespaces=NAMESPACES,
                    #     )
                    #     data = f"{organisationName[0].text}<br />{deliveryPoint[0].text}<br />{city[0].text}<br />{administrativeArea[0].text}<br />{postalCode[0].text}<br />{country[0].text}<br />{electronicMailAddress[0].text}"
                    if field.get("attribute"):
                        data = item.attrib.get(field.get("attribute"))
                    else:
                        data = item.text
                    result[field["field_id"]] = {
                        "data": data,
                        "type": field["type"],
                    }
                    print(f"    OK DATA for field {field['field_id']}")
                else:
                    if field["field_id"] == "temporalExtent":
                        temporalExtent = []
                        item = fields_data[0]
                        start = item.xpath(
                            "gml:beginPosition", namespaces=NAMESPACES
                        )
                        end = item.xpath(
                            "gml:endPosition", namespaces=NAMESPACES
                        )
                        dt_start_obj = datetime.strptime(
                            start[0].text, "%Y-%m-%d"
                        )
                        dt_end_obj = datetime.strptime(end[0].text, "%Y-%m-%d")
                        for year in range(
                            dt_start_obj.year, dt_end_obj.year + 1
                        ):
                            temporalExtent.append(str(year))
                        result[field["field_id"]] = {
                            "data": temporalExtent,
                            "type": field["type"],
                        }
                        print(f"    OK DATA for field {field['field_id']}")
                    else:
                        result[field["field_id"]] = {
                            "data": [item.text for item in fields_data],
                            "type": field["type"],
                        }
                    print(f"    OK DATA for list field {field['field_id']}")
            else:
                result[field["field_id"]] = {
                    "data": "####################### NOT TESTED ########################",
                    "type": field["type"],
                }
                print(f"    No XML Key for {field['field_id']}")
        # gmd:identificationInfo
        return result
