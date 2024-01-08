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


class ImportAPILayers(Service):
    """API endpoint to import WMS layers from the specified
    REST API service
    """

    def reply(self):
        """Reply to the request"""
        alsoProvides(self.request, IDisableCSRFProtection)
        # pylint: disable=line-too-long
        if (
            self.context.metadata_rest_api_url
            and self.context.metadata_rest_api_url.startswith("http")
        ):  # noqa: E501
            result = self.import_wms_from_metadata_rest_api_url()
            if result:
                self.request.response.setStatus(200)
                return {
                    "status": "ok",
                    "message": (
                        "WMS layers imported successfully from the REST API"
                    ),
                }
        self.request.response.setStatus(200)
        return {
            "status": "ok",
            "message": "Nothing to import",
        }

    def import_wms_from_metadata_rest_api_url(self):
        """Import WMS layers from REST API"""
        url = self.context.metadata_rest_api_url

        # XXX
        url += '?f=json'

        request = requests.get(url, timeout=5)
        if request.ok:
            wms_layers = []
            result = request.json()
            layers = result.get("layers", [])
            if layers:
                for layer in layers:
                    wms_layers.append(
                        {
                            "@id": uuid.uuid4().hex,
                            "id": str(layer.get('id')),
                            "title": layer.get('name'),
                            "default_active": False,
                            "hide": False,
                        }
                    )

            if wms_layers:
                current_layers = self.context.mapviewer_layers.get("items", [])
                new_layers = self.merge_layers(current_layers, wms_layers)
                self.context.mapviewer_layers = {"items": new_layers}
                return True

        return None

    def merge_layers(self, current_layers, new_layers):
        """Merge the new layers with the current layers"""
        merged_layers = current_layers
        current_layer_ids = [layer["id"] for layer in current_layers]
        for new_layer in new_layers:
            if new_layer["id"] not in current_layer_ids:
                merged_layers.append(new_layer)

        return merged_layers
