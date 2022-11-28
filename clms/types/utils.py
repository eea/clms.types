""" some constants"""
# -*- coding: utf-8 -*-

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
