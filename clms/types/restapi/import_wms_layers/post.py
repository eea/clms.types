"""
API endpoint to import WMS layers from the specified mapviewer_viewservice URL
"""
# -*- coding: utf-8 -*-
import uuid
from logging import getLogger
from urllib.parse import urlparse

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


class ImportWMSLayers(Service):
    """API endpoint to import WMS layers from the specified
    mapviewer_viewservice URL"""

    def reply(self):
        """ Reply to the request """
        alsoProvides(self.request, IDisableCSRFProtection)

        if (
            self.context.mapviewer_viewservice
            and self.context.mapviewer_viewservice.startswith("http")
        ):
            result = self.import_wms_from_mapviewer_viewservice()
            if result:
                self.request.response.setStatus(200)
                return {
                    "status": "ok",
                    "message": (
                        "WMS layers imported successfully from the mapviewer"
                        " service"
                    ),
                }

        geonetwork_identifiers = self.context.geonetwork_identifiers
        if not geonetwork_identifiers:
            self.request.response.setStatus(400)
            return {
                "status": "error",
                "message": (
                    "Without geonetwork_identifiers we can't import any WMS"
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
                        "message": "WMS layers imported successfully",
                    }

        self.request.response.setStatus(200)
        return {
            "status": "ok",
            "message": "Nothing to import",
        }

    def import_wms_from_mapviewer_viewservice(self):
        """Import WMS layers from the specified mapviewer_viewservice URL"""
        mapviewer_viewservice = self.context.mapviewer_viewservice
        return self.import_wms_layers(mapviewer_viewservice)

    def build_geonetwork_url(self, geonetwork_id, geonetwork_type):
        """Build the URL to the geonetwork service"""
        if geonetwork_type == "EEA":
            return EEA_GEONETWORK_BASE_URL.format(uid=geonetwork_id)
        elif geonetwork_type == "VITO":
            return VITO_GEONETWORK_BASE_URL.format(uid=geonetwork_id)
        return None

    def import_wms_layers_from_geonetwork(
        self, geonetwork_id, geonetwork_type
    ):
        """Import WMS layers from the specified mapviewer_viewservice URL"""

        url = self.build_geonetwork_url(geonetwork_id, geonetwork_type)
        if url and url.startswith("http"):
            wms_urls = self.extract_wms_urls(url)
            for wms_url in wms_urls:
                result = self.import_wms_layers(wms_url)
                if result:
                    # The import was successful
                    # update the mapviewer_viewservice
                    self.context.mapviewer_viewservice = wms_url
                    return True

        return False

    def extract_wms_urls(self, url):
        """ given a geonetwork metadata url, extract the WMS urls """
        wms_urls = []
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
                        if protocol.xpath(
                            ".//gco:CharacterString", namespaces=NAMESPACES
                        )[0].text in ["OGC:WMS", "OGC:WMTS"]:

                            for linkage in layer.xpath(
                                ".//gmd:URL", namespaces=NAMESPACES
                            ):
                                if linkage.text:
                                    wms_urls.append(linkage.text)
        except requests.exceptions.ConnectionError:
            log = getLogger(__name__)
            log.info("Could not extract WMS urls from %s", url)
        except requests.exceptions.ReadTimeout:
            log = getLogger(__name__)
            log.info("Could not extract WMS urls from %s", url)

        return wms_urls

    def import_wms_layers(self, url):
        """Import WMS layers from the specified URL"""

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

    def merge_layers(self, current_layers, new_layers):
        """Merge the new layers with the current layers"""
        merged_layers = current_layers
        current_layer_ids = [layer["id"] for layer in current_layers]
        for new_layer in new_layers:
            if new_layer["id"] not in current_layer_ids:
                merged_layers.append(new_layer)

        return merged_layers
