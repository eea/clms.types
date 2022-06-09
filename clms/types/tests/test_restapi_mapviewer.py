"""
Test the @mapviewer service
"""
# -*- coding: utf-8 -*-
import json
import unittest

import transaction
from plone import api
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    setRoles,
    applyProfile,
)
from plone.restapi.testing import RelativeSession
from plone.uuid.interfaces import IUUID

from clms.types.testing import CLMS_TYPES_RESTAPI_TESTING


class TestLRFMapViewer(unittest.TestCase):
    """test the @mapviewer endpoint applied to a LRF"""

    layer = CLMS_TYPES_RESTAPI_TESTING

    def setUp(self):
        """set up"""
        self.portal = self.layer["portal"]

        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        language_tool = api.portal.get_tool("portal_languages")
        language_tool.addSupportedLanguage("en")
        language_tool.addSupportedLanguage("fr")
        language_tool.addSupportedLanguage("de")
        applyProfile(self.portal, "plone.app.multilingual:default")

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        product_components = {
            "items": [
                {
                    "@id": "id-1",
                    "name": "Component 1",
                    "description": "Component 1 description",
                },
                {
                    "@id": "id-2",
                    "name": "Component 2",
                    "description": "Component 2 description",
                },
            ]
        }

        api.portal.set_registry_record(
            "clms.types.product_component.product_components",
            json.dumps(product_components),
        )

        self.product1 = api.content.create(
            container=self.portal.en,
            type="Product",
            id="product1",
            title="Product 1",
            mapviewer_component="id-1",
        )

        self.dataset1_1 = api.content.create(
            container=self.product1,
            type="DataSet",
            id="dataset1_1",
            title="Dataset 1",
            description="Dataset 1 description",
            mapviewer_viewservice="http://myservice.com/service",
            mapviewer_default_active=True,
            mapviewer_istimeseries=False,
            mapviewer_timeseriesservice="",
            downloadable_full_dataset=True,
            mapviewer_handlinglevel=False,
            mapviewer_layers={
                "items": [
                    {
                        "id": "layer1",
                        "title": "Layer 1",
                        "default_active": False,
                        "hide": False,
                        "static_legend_url": "http://myservice.com/service",
                    },
                    {
                        "id": "layer2",
                        "title": "Layer 2",
                        "default_active": True,
                        "hide": False,
                        "static_legend_url": "",
                    },
                    {
                        "id": "layer3",
                        "title": "Layer 3",
                        "default_active": False,
                        "hide": False,
                        "static_legend_url": "",
                    },
                ]
            },
        )

        self.dataset1_2 = api.content.create(
            container=self.product1,
            type="DataSet",
            id="dataset1_2",
            title="Dataset 2",
            description="Dataset 2 description",
            mapviewer_viewservice="http://myservice.com/service",
            mapviewer_default_active=True,
            mapviewer_istimeseries=True,
            mapviewer_timeseriesservice="",
            downloadable_full_dataset=True,
            mapviewer_handlinglevel=True,
            mapviewer_layers={
                "items": [
                    {
                        "id": "layer1",
                        "title": "Layer 1",
                        "default_active": False,
                        "hide": True,
                        "static_legend_url": "http://myservice.com/service",
                    },
                    {
                        "id": "layer2",
                        "title": "Layer 2",
                        "default_active": True,
                        "hide": False,
                        "static_legend_url": "",
                    },
                    {
                        "id": "layer3",
                        "title": "Layer 3",
                        "default_active": False,
                        "hide": False,
                        "static_legend_url": "",
                    },
                ]
            },
        )

        self.product2 = api.content.create(
            container=self.portal.en,
            type="Product",
            id="product2",
            title="Product 2",
            mapviewer_component="id-2",
        )
        self.dataset2_1 = api.content.create(
            container=self.product1,
            type="DataSet",
            id="dataset2_1",
            title="Dataset 1",
            description="Dataset 1 description",
            mapviewer_viewservice="http://myservice.com/service",
            mapviewer_default_active=True,
            mapviewer_istimeseries=False,
            mapviewer_timeseriesservice="",
            downloadable_full_dataset=True,
            mapviewer_handlinglevel=False,
            mapviewer_layers={
                "items": [
                    {
                        "id": "layer1",
                        "title": "Layer 1",
                        "default_active": False,
                        "hide": True,
                        "static_legend_url": "http://myservice.com/service",
                    },
                    {
                        "id": "layer2",
                        "title": "Layer 2",
                        "default_active": True,
                        "hide": False,
                        "static_legend_url": "",
                    },
                    {
                        "id": "layer3",
                        "title": "Layer 3",
                        "default_active": False,
                        "hide": False,
                        "static_legend_url": "",
                    },
                ]
            },
        )

        self.dataset2_2 = api.content.create(
            container=self.product1,
            type="DataSet",
            id="dataset2_2",
            title="Dataset 2",
            description="Dataset 2 description",
            mapviewer_viewservice="http://myservice.com/service",
            mapviewer_default_active=True,
            mapviewer_istimeseries=True,
            mapviewer_timeseriesservice="",
            downloadable_full_dataset=True,
            mapviewer_handlinglevel=True,
            mapviewer_layers={
                "items": [
                    {
                        "id": "layer1",
                        "title": "Layer 1",
                        "default_active": False,
                        "hide": True,
                        "static_legend_url": "http://myservice.com/service",
                    },
                    {
                        "id": "layer2",
                        "title": "Layer 2",
                        "default_active": True,
                        "hide": False,
                        "static_legend_url": "",
                    },
                    {
                        "id": "layer3",
                        "title": "Layer 3",
                        "default_active": False,
                        "hide": False,
                        "static_legend_url": "",
                    },
                ]
            },
        )

        self.product3 = api.content.create(
            container=self.portal.en,
            type="Product",
            id="product3",
            title="Product 3",
            mapviewer_component="id-1",
        )

        transaction.commit()

    def tearDown(self):
        """teardown"""
        self.api_session.close()

    def test_response(self):
        """test response"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.portal.en.absolute_url())
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-type"), "application/json"
        )

        result = response.json()

        self.assertIn("Map", result)
        self.assertIn("Components", result)
        self.assertIn("Download", result)
        self.assertFalse(result["Download"])

    def test_component_in_response(self):
        """test the component is in the response"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.portal.en.absolute_url())
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-type"), "application/json"
        )

        result = response.json()

        self.assertIn("Components", result)
        self.assertEqual(len(result["Components"]), 1)
        self.assertEqual(
            result["Components"][0]["ComponentTitle"], "Component 1"
        )
        self.assertIn("Products", result["Components"][0])

    def test_product_info(self):
        """test product info in endpoint"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.portal.en.absolute_url())
        )
        result = response.json()
        products = result["Components"][0]["Products"]
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["ProductTitle"], self.product1.Title())
        self.assertEqual(
            products[0]["ProductDescription"], self.product1.Description()
        )
        self.assertEqual(products[0]["ProductId"], IUUID(self.product1))
        self.assertIn("Datasets", products[0])

    def test_dataset_info(self):
        """test dataset info in endpoint"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.portal.en.absolute_url())
        )
        result = response.json()
        products = result["Components"][0]["Products"]
        datasets = products[0]["Datasets"]

        self.assertEqual(len(datasets), 4)
        dataset1 = datasets[0]
        self.assertEqual(dataset1["DatasetTitle"], self.dataset1_1.title)
        self.assertEqual(
            dataset1["DatasetDescription"], self.dataset1_1.description
        )
        self.assertEqual(
            dataset1["DatasetDescription"], self.dataset1_1.description
        )
        self.assertEqual(
            dataset1["ViewService"], self.dataset1_1.mapviewer_viewservice
        )
        self.assertEqual(
            dataset1["Default_active"],
            self.dataset1_1.mapviewer_default_active,
        )
        self.assertEqual(
            dataset1["IsTimeSeries"], self.dataset1_1.mapviewer_istimeseries
        )
        self.assertEqual(
            dataset1["TimeSeriesService"],
            self.dataset1_1.mapviewer_timeseriesservice,
        )
        self.assertEqual(
            dataset1["Downloadable"], self.dataset1_1.downloadable_full_dataset
        )
        self.assertEqual(
            dataset1["HandlingLevel"], self.dataset1_1.mapviewer_handlinglevel
        )

    def test_dataset_layers(self):
        """test layer info"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.portal.en.absolute_url())
        )
        result = response.json()
        products = result["Components"][0]["Products"]
        datasets = products[0]["Datasets"]
        dataset = datasets[0]
        layers = dataset["Layer"]
        self.assertEqual(len(layers), 3)
        for layer in layers:
            self.assertIn("LayerId", layer)
            self.assertIn("Title", layer)
            self.assertIn("Default_active", layer)
            self.assertIn("StaticImageLegend", layer)


class TestDataSetMapViewer(unittest.TestCase):
    """test the @mapviewer endpoint applied to a DataSet"""

    layer = CLMS_TYPES_RESTAPI_TESTING

    def setUp(self):
        """set up"""
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        product_components = {
            "items": [
                {
                    "@id": "id-1",
                    "name": "Component 1",
                    "description": "Component 1 description",
                },
                {
                    "@id": "id-2",
                    "name": "Component 2",
                    "description": "Component 2 description",
                },
            ]
        }

        api.portal.set_registry_record(
            "clms.types.product_component.product_components",
            json.dumps(product_components),
        )

        self.product1 = api.content.create(
            container=self.portal,
            type="Product",
            id="product1",
            title="Product 1",
            mapviewer_component="id-1",
        )

        self.dataset1_1 = api.content.create(
            container=self.product1,
            type="DataSet",
            id="dataset1_1",
            title="Dataset 1",
            description="Dataset 1 description",
            mapviewer_viewservice="http://myservice.com/service",
            mapviewer_default_active=True,
            mapviewer_istimeseries=False,
            mapviewer_timeseriesservice="",
            downloadable_full_dataset=True,
            mapviewer_handlinglevel=False,
            mapviewer_layers={
                "items": [
                    {
                        "id": "layer1",
                        "title": "Layer 1",
                        "default_active": False,
                    },
                    {
                        "id": "layer2",
                        "title": "Layer 2",
                        "default_active": True,
                    },
                    {
                        "id": "layer3",
                        "title": "Layer 3",
                        "default_active": False,
                    },
                ]
            },
        )

        self.dataset1_2 = api.content.create(
            container=self.product1,
            type="DataSet",
            id="dataset1_2",
            title="Dataset 2",
            description="Dataset 2 description",
            mapviewer_viewservice="http://myservice.com/service",
            mapviewer_default_active=True,
            mapviewer_istimeseries=True,
            mapviewer_timeseriesservice="",
            downloadable_full_dataset=True,
            mapviewer_handlinglevel=True,
            mapviewer_layers={
                "items": [
                    {
                        "id": "layer1",
                        "title": "Layer 1",
                        "default_active": False,
                        "hide": True,
                    },
                    {
                        "id": "layer2",
                        "title": "Layer 2",
                        "default_active": True,
                        "hide": False,
                    },
                    {
                        "id": "layer3",
                        "title": "Layer 3",
                        "default_active": False,
                        "hide": False,
                    },
                ]
            },
        )

        self.product2 = api.content.create(
            container=self.portal,
            type="Product",
            id="product2",
            title="Product 2",
            mapviewer_component="id-2",
        )
        self.dataset2_1 = api.content.create(
            container=self.product1,
            type="DataSet",
            id="dataset2_1",
            title="Dataset 1",
            description="Dataset 1 description",
            mapviewer_viewservice="http://myservice.com/service",
            mapviewer_default_active=True,
            mapviewer_istimeseries=False,
            mapviewer_timeseriesservice="",
            downloadable_full_dataset=True,
            mapviewer_handlinglevel=False,
            mapviewer_layers={
                "items": [
                    {
                        "id": "layer1",
                        "title": "Layer 1",
                        "default_active": False,
                    },
                    {
                        "id": "layer2",
                        "title": "Layer 2",
                        "default_active": True,
                    },
                    {
                        "id": "layer3",
                        "title": "Layer 3",
                        "default_active": False,
                    },
                ]
            },
        )

        self.dataset2_2 = api.content.create(
            container=self.product1,
            type="DataSet",
            id="dataset2_2",
            title="Dataset 2",
            description="Dataset 2 description",
            mapviewer_viewservice="http://myservice.com/service",
            mapviewer_default_active=True,
            mapviewer_istimeseries=True,
            mapviewer_timeseriesservice="",
            downloadable_full_dataset=True,
            mapviewer_handlinglevel=True,
            mapviewer_layers={
                "items": [
                    {
                        "id": "layer1",
                        "title": "Layer 1",
                        "default_active": False,
                        "hide": True,
                    },
                    {
                        "id": "layer2",
                        "title": "Layer 2",
                        "default_active": True,
                        "hide": False,
                    },
                    {
                        "id": "layer3",
                        "title": "Layer 3",
                        "default_active": False,
                        "hide": False,
                    },
                ]
            },
        )

        self.product3 = api.content.create(
            container=self.portal,
            type="Product",
            id="product3",
            title="Product 3",
            mapviewer_component="id-1",
        )

        transaction.commit()

    def test_mapviewer_response_json(self):
        """test the response defaults"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.dataset1_1.absolute_url())
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-type"), "application/json"
        )

        result = response.json()

        self.assertIn("Map", result)
        self.assertIn("Components", result)
        self.assertIn("Download", result)
        self.assertTrue(result["Download"])

    def test_component_in_response(self):
        """test the component is in the response"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.dataset1_1.absolute_url())
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-type"), "application/json"
        )

        result = response.json()

        self.assertIn("Components", result)
        self.assertEqual(len(result["Components"]), 1)
        self.assertEqual(
            result["Components"][0]["ComponentTitle"], "Component 1"
        )
        self.assertIn("Products", result["Components"][0])

    def test_product_info(self):
        """test product info in endpoint"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.dataset1_1.absolute_url())
        )
        result = response.json()
        products = result["Components"][0]["Products"]
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["ProductTitle"], self.product1.Title())
        self.assertEqual(
            products[0]["ProductDescription"], self.product1.Description()
        )
        self.assertEqual(products[0]["ProductId"], IUUID(self.product1))
        self.assertIn("Datasets", products[0])

    def test_dataset_info(self):
        """test dataset info in endpoint"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.dataset1_1.absolute_url())
        )
        result = response.json()
        products = result["Components"][0]["Products"]
        datasets = products[0]["Datasets"]

        self.assertEqual(len(datasets), 1)
        dataset1 = datasets[0]
        self.assertEqual(dataset1["DatasetTitle"], self.dataset1_1.title)
        self.assertEqual(
            dataset1["DatasetDescription"], self.dataset1_1.description
        )
        self.assertEqual(
            dataset1["DatasetDescription"], self.dataset1_1.description
        )
        self.assertEqual(
            dataset1["ViewService"], self.dataset1_1.mapviewer_viewservice
        )
        self.assertEqual(
            dataset1["Default_active"],
            self.dataset1_1.mapviewer_default_active,
        )
        self.assertEqual(
            dataset1["IsTimeSeries"], self.dataset1_1.mapviewer_istimeseries
        )
        self.assertEqual(
            dataset1["TimeSeriesService"],
            self.dataset1_1.mapviewer_timeseriesservice,
        )
        self.assertEqual(
            dataset1["Downloadable"], self.dataset1_1.downloadable_full_dataset
        )
        self.assertEqual(
            dataset1["HandlingLevel"], self.dataset1_1.mapviewer_handlinglevel
        )

    def test_dataset_layers(self):
        """test layer info"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.dataset1_1.absolute_url())
        )
        result = response.json()
        products = result["Components"][0]["Products"]
        datasets = products[0]["Datasets"]
        dataset = datasets[0]
        layers = dataset["Layer"]
        self.assertEqual(len(layers), 3)
        for layer in layers:
            self.assertIn("LayerId", layer)
            self.assertIn("Title", layer)
            self.assertIn("Default_active", layer)
            self.assertIn("StaticImageLegend", layer)
