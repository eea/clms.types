""" Import fields from WMS REST API"""
# -*- coding: utf-8 -*-
import json

import requests
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.services import Service
from zope.interface import alsoProvides

FIELDS_IMPORTED = 1
FIELDS_NOT_IMPORTED = 2
ERROR = 3


class ImportWMSFields(Service):
    """Service to import fields from WMS REST API"""

    def reply(self):
        """return"""
        alsoProvides(self.request, IDisableCSRFProtection)
        # pylint: disable=line-too-long
        if (
            self.context.mapviewer_viewservice
            and self.context.mapviewer_viewservice.startswith("http")
        ):  # noqa: E501
            result = self.import_wms_fields()
            if result == FIELDS_IMPORTED:
                self.request.response.setStatus(200)
                return {
                    "status": "ok",
                    "message": (
                        "WMS fields imported successfully from the mapviewer"
                        " service"
                    ),
                }
            elif result == FIELDS_NOT_IMPORTED:
                self.request.response.setStatus(200)
                return {
                    "status": "ok",
                    "message": (
                        "WMS fields could not be imported because they do not"
                        " exist"
                    ),
                }

            self.request.response.setStatus(500)
            return {
                "status": "error",
                "message": "There was an error processing the request.",
            }

    def import_wms_fields(self):
        import pdb

        pdb.set_trace()
        a = 1

        base_url = self.context.mapviewer_viewservice
        if base_url.find("/arcgis/") != -1:
            layers = self.context.mapviewer_layers.get("items", [])
            new_layers = []
            for layer in layers:
                rest_api_url = base_url.replace("/arcgis/", "/arcgis/rest/")
                rest_api_url = rest_api_url.replace("/MapServer", "")
                rest_api_url = f"{rest_api_url}/{layer['id']}?f=pjson"
                try:
                    field_data = extract_fields_from_rest_api(rest_api_url)
                    from logging import getLogger

                    log = getLogger(__name__)
                    log.info(
                        "Layer: {} field_data: {}".format(
                            layer["id"], field_data
                        )
                    )
                    layer.update({"fields": field_data})
                    new_layers.append(layer)
                except:
                    return ERROR

            self.context.mapviewer_layers["items"] = new_layers
            return FIELDS_IMPORTED

        return FIELDS_NOT_IMPORTED


def extract_fields_from_rest_api(url):
    """given an Arcgis server REST API url, extract the fields stated there
    and return the JSON"""
    result = requests.get(url, timeout=5)
    fields = []
    if result.ok:
        data = result.json()
        fields = data.get("fields", [])

    return json.dumps(fields)
