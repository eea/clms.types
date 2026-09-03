"""Tests for the WMS/WMTS layer import service."""
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from clms.types.restapi.import_wms_layers.post import (
    ImportWMSLayers,
    REQUEST_TIMEOUT,
)


WMS_CAPABILITIES = """\
<WMS_Capabilities xmlns="http://www.opengis.net/wms">
  <Capability>
    <Layer>
      <Title>Service title</Title>
      <Layer>
        <Name>snow:extent</Name>
        <Title>Snow Cover Extent</Title>
      </Layer>
    </Layer>
  </Capability>
</WMS_Capabilities>
"""

WMTS_CAPABILITIES = """\
<Capabilities xmlns="http://www.opengis.net/wmts/1.0"
              xmlns:ows="http://www.opengis.net/ows/1.1">
  <Contents>
    <Layer>
      <ows:Title>Gross Dry Matter Productivity</ows:Title>
      <ows:Identifier>GDMP</ows:Identifier>
    </Layer>
    <Layer>
      <ows:Identifier>NDVI</ows:Identifier>
    </Layer>
  </Contents>
</Capabilities>
"""

GEONETWORK_METADATA = """\
<gmd:MD_Metadata
    xmlns:gmd="http://www.isotc211.org/2005/gmd"
    xmlns:gco="http://www.isotc211.org/2005/gco">
  <gmd:distributionInfo>
    <gmd:MD_Distribution>
      <gmd:transferOptions>
        <gmd:MD_DigitalTransferOptions>
          <gmd:onLine>
            <gmd:CI_OnlineResource>
              <gmd:linkage>
                <gmd:URL>https://example.com/ogc-service</gmd:URL>
              </gmd:linkage>
              <gmd:protocol>
                <gco:CharacterString>OGC:WMTS</gco:CharacterString>
              </gmd:protocol>
            </gmd:CI_OnlineResource>
          </gmd:onLine>
        </gmd:MD_DigitalTransferOptions>
      </gmd:transferOptions>
    </gmd:MD_Distribution>
  </gmd:distributionInfo>
</gmd:MD_Metadata>
"""


class TestImportWMSLayers(unittest.TestCase):
    """Test capabilities URL construction and layer extraction."""

    def setUp(self):
        self.service = object.__new__(ImportWMSLayers)
        self.service.context = SimpleNamespace(
            mapviewer_layers={"items": []}
        )

    def test_detects_service_type_from_query_and_path(self):
        """Configured URLs identify WMS and WMTS services."""
        self.assertEqual(
            self.service.get_service_type(
                "https://example.com/ows?service=wmts"
            ),
            "WMTS",
        )
        self.assertEqual(
            self.service.get_service_type("https://example.com/ogc/wms/id"),
            "WMS",
        )
        self.assertEqual(
            self.service.get_service_type("https://example.com/ows"),
            "WMS",
        )

    def test_imports_wms_name_and_title(self):
        """The existing WMS import behavior remains supported."""
        response = Mock(text=WMS_CAPABILITIES)

        with patch(
            "clms.types.restapi.import_wms_layers.post.requests.get",
            return_value=response,
        ):
            imported = self.service.import_wms_layers(
                "https://example.com/ogc/wms"
            )

        self.assertTrue(imported)
        layers = self.service.context.mapviewer_layers["items"]
        self.assertEqual(layers[0]["id"], "snow:extent")
        self.assertEqual(layers[0]["title"], "Snow Cover Extent")

    def test_imports_wmts_identifiers_and_merges_layers(self):
        """WMTS ows:Identifier values populate mapviewer layer IDs."""
        existing_layer = {
            "@id": "existing-id",
            "id": "GDMP",
            "title": "Existing title",
            "default_active": True,
            "hide": False,
        }
        self.service.context.mapviewer_layers = {
            "items": [existing_layer]
        }
        response = Mock(text=WMTS_CAPABILITIES)

        with patch(
            "clms.types.restapi.import_wms_layers.post.requests.get",
            return_value=response,
        ) as request:
            imported = self.service.import_wms_layers(
                "https://sh.dataspace.copernicus.eu/ogc/wmts/service-id"
            )

        self.assertTrue(imported)
        request.assert_called_once_with(
            "https://sh.dataspace.copernicus.eu/ogc/wmts/service-id"
            "?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetCapabilities",
            timeout=REQUEST_TIMEOUT,
        )
        layers = self.service.context.mapviewer_layers["items"]
        self.assertEqual([layer["id"] for layer in layers], ["GDMP", "NDVI"])
        self.assertIs(layers[0], existing_layer)
        self.assertEqual(layers[1]["title"], "NDVI")

    def test_extracts_wmts_type_from_geonetwork(self):
        """GeoNetwork protocol metadata is passed through with its URL."""
        response = Mock(ok=True, text=GEONETWORK_METADATA)

        with patch(
            "clms.types.restapi.import_wms_layers.post.requests.get",
            return_value=response,
        ):
            services = self.service.extract_ogc_services(
                "https://example.com/metadata"
            )

        self.assertEqual(
            services,
            [("https://example.com/ogc-service", "WMTS")],
        )


if __name__ == "__main__":
    unittest.main()
