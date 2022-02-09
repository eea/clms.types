"""
Test the @mapviewer service
"""
# -*- coding: utf-8 -*-
import unittest

import transaction
from plone import api
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    setRoles,
)
from plone.restapi.testing import RelativeSession
from plone.uuid.interfaces import IUUID

from clms.types.testing import CLMS_TYPES_RESTAPI_TESTING


class TestLRFMapViewer(unittest.TestCase):
    """ test the @mapviewer endpoint applied to a LRF """

    layer = CLMS_TYPES_RESTAPI_TESTING

    def setUp(self):
        """ set up"""
        self.portal = self.layer["portal"]

        transaction.commit()


class TestDataSetMapViewer(unittest.TestCase):
    """ test the @mapviewer endpoint applied to a DataSet """

    layer = CLMS_TYPES_RESTAPI_TESTING

    def setUp(self):
        """ set up"""
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url, test=self)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.product1 = api.content.create(
            container=self.portal,
            type="Product",
            id="product1",
            title="Product 1",
            component_title="Component 1",
        )

        self.dataset1_1 = api.content.create(
            container=self.product1,
            type="DataSet",
            id="dataset1_1",
            title="Dataset 1",
            description="Dataset 1 description",
            mapviewer_viewservice="http://myservice.com/service",
            mapviewer_default_active=True,
            mapviewer_downloadservice="EEA",
            mapviewer_downloadtype="ESRI REST Service",
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
            mapviewer_downloadservice="EEA",
            mapviewer_downloadtype="ESRI REST Service",
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
            component_title="Component 2",
        )
        self.dataset2_1 = api.content.create(
            container=self.product1,
            type="DataSet",
            id="dataset2_1",
            title="Dataset 1",
            description="Dataset 1 description",
            mapviewer_viewservice="http://myservice.com/service",
            mapviewer_default_active=True,
            mapviewer_downloadservice="EEA",
            mapviewer_downloadtype="ESRI REST Service",
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
            mapviewer_downloadservice="EEA",
            mapviewer_downloadtype="ESRI REST Service",
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
            component_title="Component 1",
        )

        transaction.commit()

    def test_mapviewer_response_json(self):
        """ test the response defaults """
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
        """ test the component is in the response """
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
        """ test product info in endpoint"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.dataset1_1.absolute_url())
        )
        result = response.json()
        products = result["Components"][0]["Products"]
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["ProductTitle"], "Product 1")
        self.assertEqual(products[0]["ProductId"], IUUID(self.product1))
        self.assertIn("Datasets", products[0])

    def test_dataset_info(self):
        """ test dataset info in endpoint"""
        response = self.api_session.get(
            "{}/@mapviewer".format(self.dataset1_1.absolute_url())
        )
        result = response.json()
        products = result["Components"][0]["Products"]
        datasets = products[0]["Datasets"]

        self.assertEqual(len(datasets), 1)
        dataset1 = datasets[0]
        self.assertEquals(dataset1["DatasetTitle"], self.dataset1_1.title)
        self.assertEquals(
            dataset1["DatasetDescription"], self.dataset1_1.description
        )
        self.assertEquals(
            dataset1["DatasetDescription"], self.dataset1_1.description
        )
        self.assertEquals(
            dataset1["ViewService"], self.dataset1_1.mapviewer_viewservice
        )
        self.assertEquals(
            dataset1["Default_active"],
            self.dataset1_1.mapviewer_default_active,
        )
        self.assertEquals(
            dataset1["DownloadService"],
            self.dataset1_1.mapviewer_downloadservice,
        )
        self.assertEquals(
            dataset1["DownloadType"], self.dataset1_1.mapviewer_downloadtype
        )
        self.assertEquals(
            dataset1["IsTimeSeries"], self.dataset1_1.mapviewer_istimeseries
        )
        self.assertEquals(
            dataset1["TimeSeriesService"],
            self.dataset1_1.mapviewer_timeseriesservice,
        )
        self.assertEquals(
            dataset1["Downloadable"], self.dataset1_1.downloadable_full_dataset
        )
        self.assertEquals(
            dataset1["HandlingLevel"], self.dataset1_1.mapviewer_handlinglevel
        )

    def test_dataset_layers(self):
        """ test layer info"""
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
