""" some constants"""
# -*- coding: utf-8 -*-
from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy.restapi.services.taxonomy.get import TaxonomyGet
from zope.component import getUtility
from zope.globalrequest import getRequest

EEA_GEONETWORK_BASE_URL = (
    "https://sdi.eea.europa.eu/catalogue/copernicus/"
    "api/records/{uid}/formatters/xml?approved=true"
)
VITO_GEONETWORK_BASE_URL = (
    "https://land.copernicus.vgt.vito.be/geonetwork/"
    "srv/api/records/{uid}/formatters/xml?approved=true"
)

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
    "schemaLocation": (
        "http://www.isotc211.org/2005/gmd"
        " http://schemas.opengis.net/csw/2.0.2/profiles/apiso/1.0.0/apiso.xsd"
    ),
}

NAMESPACES_VITO = {
    "gmd": "http://www.isotc211.org/2005/gmd",
    "gco": "http://www.isotc211.org/2005/gco",
    "wms_default": "http://www.opengis.net/wms",
    "srv": "http://www.isotc211.org/2005/srv",
    "gmx": "http://www.isotc211.org/2005/gmx",
    "gts": "http://www.isotc211.org/2005/gts",
    "gsr": "http://www.isotc211.org/2005/gsr",
    "gmi": "http://www.isotc211.org/2005/gmi",
    "gml": "http://www.opengis.net/gml",
    "xlink": "http://www.w3.org/1999/xlink",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "schemaLocation": (
        "http://www.isotc211.org/2005/gmd"
        " http://schemas.opengis.net/csw/2.0.2/profiles/apiso/1.0.0/apiso.xsd"
    ),
}

COLORS = {
    "end": "\033[0m",
    "fg": {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "orange": "\033[33m",
        "blue": "\033[34m",
        "purple": "\033[35m",
        "cyan": "\033[36m",
        "lightgrey": "\033[37m",
        "darkgrey": "\033[90m",
        "lightred": "\033[91m",
        "lightgreen": "\033[92m",
        "yellow": "\033[93m",
        "lightblue": "\033[94m",
        "pink": "\033[95m",
        "lightcyan": "\033[96m",
    },
    "bg": {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "orange": "\033[43m",
        "blue": "\033[44m",
        "purple": "\033[45m",
        "cyan": "\033[46m",
        "lightgrey": "\033[47m",
    },
}


def get_taxonomy_tree(taxonomy_identifier):
    """given a taxonomy identifer, return its corresponding tree"""
    request = getRequest()
    taxonomy = getUtility(ITaxonomy, taxonomy_identifier)
    taxonomy_view = TaxonomyGet(taxonomy, request)
    traversed_taxonomy_view = taxonomy_view.publishTraverse(
        request, taxonomy_identifier
    )
    json_data = traversed_taxonomy_view.get_data()
    return json_data.get("tree", [])
