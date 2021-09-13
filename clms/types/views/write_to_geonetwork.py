# -*- coding: utf-8 -*-
"""
Write into geonetwork
"""

from xml.etree import ElementTree as ET

import requests
from plone import api
from Products.Five.browser import BrowserView


class InvalidLoginException(Exception):
    pass


GEONETWORK_BASE_URL = "http://localhost:7070/geonetwork"
GEONETWORK_API_URL = "{GEONETWORK_BASE_URL}/srv/api".format(
    GEONETWORK_BASE_URL=GEONETWORK_BASE_URL
)
EEA_GEONETWORK_BASE_URL = "https://sdi.eea.europa.eu/catalogue/srv/api"
AUTH = ("admin", "admin")


class InvalidMetadata(Exception):
    pass


class WriteToGeoNetworkView(BrowserView):
    def __call__(self):
        # Implement your own actions:

        self.context.geonetwork_identifier = self.write_into_geonetwork()
        return self.index()

    def write_one_metadata(self, metadata, token, update=False):
        # if "OVERWRITE" is passed, the metadata items are updated
        if update:
            processing = "OVERWRITE"
        else:
            processing = "GENERATEUUID"

        result = requests.put(
            f"{GEONETWORK_API_URL}/records?_csrf={token}"
            f"&metadataType=METADATA"
            f"&uuidProcessing={processing}"
            f"&transformWith=_none_"
            f"&group=2"
            f"&category="
            f"&publishToAll=true",
            data=metadata,
            auth=AUTH,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/xml",
                "X-XSRF-TOKEN": token,
            },
            cookies={"XSRF-TOKEN": token},
        )
        if result.ok:
            data = result.json()
            metadatauuid = (
                data.get("metadataInfos")
                .get(list(data.get("metadataInfos").keys())[0])[0]
                .get("uuid")
            )
            print(
                "Created item with uuid: {}".format(
                    data.get("metadataInfos")
                    .get(list(data.get("metadataInfos").keys())[0])[0]
                    .get("uuid")
                )
            )
            return {
                "token": result.cookies.get("XSRF-TOKEN") or token,
                "metadatauuid": metadatauuid,
            }
        else:
            raise InvalidMetadata

    def parse_login_response(self, xmldata):
        root = ET.fromstring(xmldata)
        value = root.find("me").get("authenticated")
        return value == "true"

    def login(self):
        result = requests.post(f"{GEONETWORK_API_URL}/info?type=me")
        token = result.cookies.get("XSRF-TOKEN")

        result2 = requests.post(
            f"{GEONETWORK_BASE_URL}/srv/eng/info?type=me",
            auth=AUTH,
            headers={"X-XSRF-TOKEN": token},
            cookies={"XSRF-TOKEN": token},
        )
        authenticated = self.parse_login_response(result2.text)
        if authenticated:
            return result2.cookies.get("XSRF-TOKEN") or token

        raise InvalidLoginException

    def write_into_geonetwork(self):
        try:
            geo_id = self.context.geonetwork_identifier
            metadata = self.plone_to_xml().encode("utf-8")
            token = self.login()
            if geo_id != "" or geo_id is not None:
                result = self.write_one_metadata(
                    metadata, token=token, update=True
                )
                print(f"Done {result.get('metadatauuid')}")
                return result.get("metadatauuid")
            else:
                result = self.write_one_metadata(metadata, token=token)
                print(f"Done {result.get('metadatauuid')}")
                return result.get("metadatauuid")
        except InvalidMetadata:
            print(f"Error writing {self.uuid}")

    def plone_to_xml(self):
        training_view = api.content.get_view(
            "geonetwork-xml-view", self.context, self.request
        )
        return training_view.__call__()
