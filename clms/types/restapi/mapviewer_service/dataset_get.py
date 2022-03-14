"""
REST API endpoint to get the mapviewer configuration data for a given dataset
"""
import json

from Acquisition import aq_inner, aq_parent
from OFS.interfaces import IOrderedContainer
from plone import api
from plone.restapi.services import Service
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from .lrf_get import RootMapViewerServiceGet


def getObjPositionInParent(obj):
    """get the position of the object in the parent"""
    parent = aq_parent(aq_inner(obj))
    ordered = IOrderedContainer(parent, None)
    if ordered is not None:
        return ordered.getObjectPosition(obj.getId())
    return 0


class DataSetMapViewerServiceGet(RootMapViewerServiceGet):
    """Return the mapviewer configuration"""

    def reply(self):
        """ return the JSON """
        result = super().reply()
        result["Download"] = True
        return result

    def get_products(self):
        """get all products"""
        product = aq_parent(self.context)
        if product.portal_type == "Product":
            datasets = [self.serialize_dataset(self.context)]
            if datasets:
                # pylint: disable=line-too-long
                (
                    component_title,
                    component_description,
                ) = self.get_component_info(
                    product
                )  # noqa: E501
                yield {
                    "Component": (component_title, component_description),
                    "ProductTitle": product.Title(),
                    "ProductDescription": product.Description(),
                    "ProductId": product.UID(),
                    "Datasets": sorted(
                        datasets, key=lambda x: x.get("DatasetTitle")
                    ),  # noqa: E501
                    "PositionInParent": getObjPositionInParent(product),
                }

    def serialize_dataset(self, dataset):
        """serialize one dataset using the keys needed by the mapviewer"""
        if dataset.mapviewer_viewservice:
            layers = []
            layers_value = dataset.mapviewer_layers
            for layer_item in layers_value.get("items", []):
                if "hide" not in layer_item or not layer_item["hide"]:
                    layers.append(
                        {
                            "LayerId": layer_item.get("id", ""),
                            "Title": layer_item.get("title", ""),
                            "Default_active": layer_item.get(
                                "default_active", False
                            ),
                        }
                    )
            if layers:
                parent = aq_parent(dataset)
                if parent.portal_type == "Product":
                    title = parent.Title()
                    productId = api.content.get_uuid(obj=parent)
                else:
                    title = "Default"
                    productId = ""
                return {
                    # Datasets are saved inside product, so the Title name is
                    # its parent's name
                    "Product": title,
                    "ProductId": productId,  # noqa: E501
                    "DatasetId": api.content.get_uuid(obj=dataset),
                    "DatasetTitle": dataset.Title(),
                    "DatasetDescription": dataset.Description(),
                    "DatasetURL": self.get_item_volto_url(dataset),
                    "ViewService": dataset.mapviewer_viewservice,
                    "Default_active": dataset.mapviewer_default_active,
                    "Layer": layers,
                    "DownloadService": dataset.mapviewer_downloadservice,
                    "DownloadType": dataset.mapviewer_downloadtype,
                    "IsTimeSeries": dataset.mapviewer_istimeseries,
                    "TimeSeriesService": dataset.mapviewer_timeseriesservice,
                    "Downloadable": bool(dataset.downloadable_full_dataset),
                    "PositionInParent": getObjPositionInParent(dataset),
                    "HandlingLevel": bool(dataset.mapviewer_handlinglevel),
                }

        return None
