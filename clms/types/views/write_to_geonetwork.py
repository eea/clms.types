# -*- coding: utf-8 -*-
"""
Write into geonetwork
"""

from xml.etree import ElementTree as ET

import requests
from plone import api
from Products.Five.browser import BrowserView


class InvalidLoginException(Exception):
    """
    Invalid Login Exception
    """


GEONETWORK_BASE_URL = "http://localhost:7070/geonetwork"
GEONETWORK_API_URL = f"{GEONETWORK_BASE_URL}/srv/api"
EEA_GEONETWORK_BASE_URL = "https://sdi.eea.europa.eu/catalogue/srv/api"
AUTH = ("admin", "admin")


class InvalidMetadata(Exception):
    """
    Invalid Metadata
    """


class WriteToGeoNetworkView(BrowserView):
    """
    WriteToGeoNetworkView
    """

    def __call__(self):
        # Implement your own actions:

        self.context.geonetwork_identifier = self.write_into_geonetwork()
        return self.index()

    def write_one_metadata(self, metadata, token, update=False):
        """
        Write one metadata
        """

        # if "OVERWRITE" is passed, the metadata items are updated
        if update:
            processing = "OVERWRITE"
        else:
            processing = "GENERATEUUID"
        request = (
            f"{GEONETWORK_API_URL}/records?_csrf={token}"
            f"&metadataType=METADATA"
            f"&uuidProcessing={processing}"
            f"&transformWith=_none_"
            f"&group=2"
            f"&category="
            f"&publishToAll=true"
        )

        result = requests.put(
            request,
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
                f"""Created item with uuid: 
                {data.get('metadataInfos')
                .get(list(data.get('metadataInfos').keys())[0])[0]
                .get('uuid')}"""
            )
            return {
                "token": result.cookies.get("XSRF-TOKEN") or token,
                "metadatauuid": metadatauuid,
            }
        raise InvalidMetadata

    def parse_login_response(self, xmldata):
        """
        Parse login response
        """
        root = ET.fromstring(xmldata)
        value = root.find("me").get("authenticated")
        return value == "true"

    def login(self):
        """
        login
        """
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
        """
        Write into geonetwork
        """
        try:
            geo_id = self.context.geonetwork_identifier
            metadata = self.plone_to_xml().encode("utf-8")
            token = self.login()
            result = self.write_one_metadata(
                metadata, token=token, update=geo_id is not None
            )
            print(f"Done {result.get('metadatauuid')}")
            return result.get("metadatauuid")
        except InvalidMetadata:
            print(f"Error writing {self.context.title}")
            return None

    def plone_to_xml(self):
        """
        plone to xml
        """
        training_view = api.content.get_view(
            "geonetwork-xml-view", self.context, self.request
        )
        return training_view.__call__()
