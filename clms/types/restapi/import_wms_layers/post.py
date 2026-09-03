"""API endpoint to import layers from WMS and WMTS view services."""
# -*- coding: utf-8 -*-
import uuid
from logging import getLogger
from urllib.parse import parse_qs, urlparse

import requests
from lxml import etree
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.services import Service
from zope.interface import alsoProvides

from clms.types.utils import (
    EEA_GEONETWORK_BASE_URL,
    NAMESPACES,
    VITO_GEONETWORK_BASE_URL,
)

REQUEST_TIMEOUT = 10
SUPPORTED_SERVICE_TYPES = ("WMS", "WMTS")
WMTS_NAMESPACES = {
    "wmts": "http://www.opengis.net/wmts/1.0",
    "ows": "http://www.opengis.net/ows/1.1",
}


class ImportWMSLayers(Service):
    """Import layers from the configured OGC view service."""

    def reply(self):
        """Reply to the request."""
        alsoProvides(self.request, IDisableCSRFProtection)
        # pylint: disable=line-too-long
        if (self.context.mapviewer_viewservice and self.context.mapviewer_viewservice.startswith("http")):  # noqa: E501
            result = self.import_wms_from_mapviewer_viewservice()
            if result:
                self.request.response.setStatus(200)
                return {
                    "status": "ok",
                    "message": (
                        "Layers imported successfully from the mapviewer"
                        " service"
                    ),
                }

        geonetwork_identifiers = self.context.geonetwork_identifiers
        if not geonetwork_identifiers:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "message": (
                    "Without geonetwork_identifiers we can't import any"
                    " layers"
                ),
            }

        for geonetwork_identifier in geonetwork_identifiers.get("items", []):
            geonetwork_id = geonetwork_identifier.get("id")
            geonetwork_type = geonetwork_identifier.get("type")
            if geonetwork_id and geonetwork_type:
                result = self.import_wms_layers_from_geonetwork(
                    geonetwork_id, geonetwork_type
                )
                if result:
                    self.request.response.setStatus(200)
                    return {
                        "status": "ok",
                        "message": "Layers imported successfully",
                    }

        self.request.response.setStatus(200)
        return {
            "status": "ok",
            "message": "Nothing to import",
        }

    def import_wms_from_mapviewer_viewservice(self):
        """Import layers from the configured view service URL."""
        mapviewer_viewservice = self.context.mapviewer_viewservice
        return self.import_wms_layers(mapviewer_viewservice)

    def build_geonetwork_url(self, geonetwork_id, geonetwork_type):
        """Build the URL to the geonetwork service"""
        if geonetwork_type == "EEA":
            return EEA_GEONETWORK_BASE_URL.format(uid=geonetwork_id)
        if geonetwork_type == "VITO":
            return VITO_GEONETWORK_BASE_URL.format(uid=geonetwork_id)
        return None

    def import_wms_layers_from_geonetwork(
        self, geonetwork_id, geonetwork_type
    ):
        """Import layers from OGC services referenced by GeoNetwork."""

        url = self.build_geonetwork_url(geonetwork_id, geonetwork_type)
        if url and url.startswith("http"):
            ogc_services = self.extract_ogc_services(url)
            for service_url, service_type in ogc_services:
                result = self.import_wms_layers(service_url, service_type)
                if result:
                    # The import was successful
                    # update the mapviewer_viewservice
                    self.context.mapviewer_viewservice = service_url
                    return True

        return False

    def extract_ogc_services(self, url):
        """Extract WMS and WMTS service URLs from GeoNetwork metadata."""
        ogc_services = []
        # pylint: disable=too-many-nested-blocks
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            if response.ok:
                doc = etree.fromstring(response.text.encode("utf-8"))
                parsed_layers = doc.xpath(
                    "//gmd:onLine", namespaces=NAMESPACES
                )
                for layer in parsed_layers:
                    for protocol in layer.xpath(
                        ".//gmd:protocol", namespaces=NAMESPACES
                    ):
                        protocol_tag = protocol.xpath(
                            ".//gco:CharacterString", namespaces=NAMESPACES
                        )[0].text
                        if protocol_tag in ["OGC:WMS", "OGC:WMTS"]:
                            service_type = protocol_tag.split(":")[-1]

                            for linkage in layer.xpath(
                                ".//gmd:URL", namespaces=NAMESPACES
                            ):
                                if linkage.text:
                                    ogc_services.append(
                                        (linkage.text, service_type)
                                    )
        except requests.exceptions.ConnectionError:
            log = getLogger(__name__)
            log.info("Could not extract OGC service URLs from %s", url)
        except requests.exceptions.ReadTimeout:
            log = getLogger(__name__)
            log.info("Could not extract OGC service URLs from %s", url)

        return ogc_services

    def get_service_type(self, url):
        """Determine whether a configured view service is WMS or WMTS."""
        parsed_url = urlparse(url)
        for key, values in parse_qs(parsed_url.query).items():
            if key.lower() == "service" and values:
                service_type = values[0].upper()
                if service_type in SUPPORTED_SERVICE_TYPES:
                    return service_type

        path_segments = parsed_url.path.lower().split("/")
        return "WMTS" if "wmts" in path_segments else "WMS"

    def import_wms_layers(self, url, service_type=None):
        """Import layers from the specified WMS or WMTS URL."""

        service_type = service_type or self.get_service_type(url)
        if service_type == "WMTS":
            return self.import_wmts_layers(url)

        parsed_url = urlparse(url)

        new_url = "{}://{}{}?request=GetCapabilities&service=WMS".format(
            parsed_url.scheme, parsed_url.netloc, parsed_url.path
        )

        try:
            response = requests.get(new_url, timeout=REQUEST_TIMEOUT)
            doc = etree.fromstring(response.text.encode("utf-8"))
            parsed_layers = doc.xpath(
                "//wms_default:Layer", namespaces=NAMESPACES
            )
            wms_layers = []
            for layer in parsed_layers:
                name_tags = layer.xpath(
                    "./wms_default:Name", namespaces=NAMESPACES
                )
                title_tags = layer.xpath(
                    "./wms_default:Title", namespaces=NAMESPACES
                )
                if name_tags:
                    title = ""
                    if title_tags and title_tags[0].text:
                        title = title_tags[0].text
                    else:
                        title = name_tags[0].text

                    wms_layers.append(
                        {
                            "@id": uuid.uuid4().hex,
                            "id": name_tags[0].text,
                            "title": title,
                            "default_active": False,
                            "hide": False,
                        }
                    )

            if wms_layers:
                current_layers = self.context.mapviewer_layers.get("items", [])
                new_layers = self.merge_layers(current_layers, wms_layers)
                self.context.mapviewer_layers = {"items": new_layers}
                return True
        except requests.exceptions.ConnectionError:
            log = getLogger(__name__)
            log.info("Could not import WMS layers from %s", new_url)
        except requests.exceptions.ReadTimeout:
            log = getLogger(__name__)
            log.info("Could not import WMS layers from %s", new_url)
        except etree.XMLSyntaxError:
            log = getLogger(__name__)
            log.info("Could not import WMS layers from %s", new_url)

        return False

    def import_wmts_layers(self, url):
        """Import WMTS layers from the specified URL."""

        parsed_url = urlparse(url)
        new_url = (
            "{}://{}{}?SERVICE=WMTS&VERSION=1.0.0"
            "&REQUEST=GetCapabilities"
        ).format(parsed_url.scheme, parsed_url.netloc, parsed_url.path)

        try:
            response = requests.get(new_url, timeout=REQUEST_TIMEOUT)
            doc = etree.fromstring(response.text.encode("utf-8"))
            parsed_layers = doc.xpath(
                "//wmts:Layer", namespaces=WMTS_NAMESPACES
            )
            wmts_layers = []
            for layer in parsed_layers:
                identifier_tags = layer.xpath(
                    "./ows:Identifier", namespaces=WMTS_NAMESPACES
                )
                title_tags = layer.xpath(
                    "./ows:Title", namespaces=WMTS_NAMESPACES
                )
                if identifier_tags:
                    title = ""
                    if title_tags and title_tags[0].text:
                        title = title_tags[0].text
                    else:
                        title = identifier_tags[0].text

                    wmts_layers.append(
                        {
                            "@id": uuid.uuid4().hex,
                            "id": identifier_tags[0].text,
                            "title": title,
                            "default_active": False,
                            "hide": False,
                        }
                    )

            if wmts_layers:
                current_layers = self.context.mapviewer_layers.get("items", [])
                new_layers = self.merge_layers(current_layers, wmts_layers)
                self.context.mapviewer_layers = {"items": new_layers}
                return True
        except requests.exceptions.ConnectionError:
            log = getLogger(__name__)
            log.info("Could not import WMTS layers from %s", new_url)
        except requests.exceptions.ReadTimeout:
            log = getLogger(__name__)
            log.info("Could not import WMTS layers from %s", new_url)
        except etree.XMLSyntaxError:
            log = getLogger(__name__)
            log.info("Could not import WMTS layers from %s", new_url)

        return False

    def merge_layers(self, current_layers, new_layers):
        """Merge the new layers with the current layers"""
        merged_layers = current_layers
        current_layer_ids = [layer["id"] for layer in current_layers]
        for new_layer in new_layers:
            if new_layer["id"] not in current_layer_ids:
                merged_layers.append(new_layer)

        return merged_layers
