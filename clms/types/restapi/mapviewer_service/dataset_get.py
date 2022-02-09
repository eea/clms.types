"""
REST API endpoint to get the mapviewer configuration data for a given dataset
"""
from Acquisition import aq_inner, aq_parent
from OFS.interfaces import IOrderedContainer
from plone import api
from plone.restapi.services import Service


def getObjPositionInParent(obj):
    """get the position of the object in the parent"""
    parent = aq_parent(aq_inner(obj))
    ordered = IOrderedContainer(parent, None)
    if ordered is not None:
        return ordered.getObjectPosition(obj.getId())
    return 0


class DataSetMapViewerServiceGet(Service):
    """Return the mapviewer configuration"""

    def reply(self):
        """main method"""
        components = []

        for component in self.get_map_components():
            components.append(
                {
                    "ComponentTitle": component.get("title"),
                    "Products": sorted(
                        component.get("products"),
                        key=lambda x: x.get("PositionInParent"),
                    ),  # noqa: E501
                }
            )

        return {
            "Map": {
                "div": "mapDiv",
                "center": [15, 50],
                "zoom": 3,
            },
            "Download": True,
            "Components": sorted(
                components, key=lambda x: x.get("PositionInParent")
            ),  # noqa: E501
        }

    def get_map_components(self):
        """get product information grouped by components"""
        components = {}
        products = self.get_products()
        for product_info in products:
            product_key = product_info.get("Component")
            del product_info["Component"]
            product = components.get(product_key, [])
            product.append(product_info)
            components[product_key] = product

        for component, products in components.items():
            yield {
                "title": component,
                "products": products,
            }

    def get_products(self):
        """get all products"""
        product = aq_parent(self.context)
        if product.portal_type == "Product":
            datasets = [self.serialize_dataset(self.context)]
            if datasets:
                yield {
                    "Component": product.component_title,
                    "ProductTitle": product.Title(),
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

    def get_item_volto_url(self, dataset):
        """get the volto url for a given dataset"""
        context_url = dataset.absolute_url()
        plone_domain = api.portal.get().absolute_url()
        frontend_domain = api.portal.get_registry_record(
            "volto.frontend_domain"
        )
        if frontend_domain.endswith("/"):
            frontend_domain = frontend_domain[:-1]

        return context_url.replace(plone_domain, frontend_domain)
