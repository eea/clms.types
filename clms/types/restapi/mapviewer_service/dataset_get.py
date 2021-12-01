"""
REST API endpoint to get the mapviewer configuration data for a given dataset
"""
from Acquisition import aq_parent
from plone import api
from plone.restapi.services import Service


class DataSetMapViewerServiceGet(Service):
    """Return the mapviewer configuration"""

    def reply(self):
        """main method"""
        components = []

        for component in self.get_map_components():
            components.append(
                {
                    "ComponentTitle": component.get("title"),
                    "Products": sorted(component.get("products"), key=lambda x: x.get("ProductTitle")),  # noqa: E501
                }
            )

        return {
            "Map": {
                "div": "mapDiv",
                "center": [15, 50],
                "zoom": 3,
            },
            "Download": True,
            "Components": sorted(components, key=lambda x: x.get("ComponentTitle")),  # noqa: E501
        }

    def get_datasets(self):
        """get all datasets"""
        brains = api.content.find(
            portal_type="DataSet",
            context=api.portal.get_navigation_root(self.context),
        )
        return [brain.getObject() for brain in brains]

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
                    "Datasets": sorted(datasets, key=lambda x: x.get("DatasetTitle")),  # noqa: E501
                }

    def serialize_dataset(self, dataset):
        """serialize one dataset using the keys needed by the mapviewer"""
        if dataset.mapviewer_viewservice:
            layers = []
            layers_value = dataset.mapviewer_layers
            for layer_item in layers_value.get("items", []):
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
                return {
                    # Datasets are saved inside product, so the Title name is
                    # its parent's name
                    # pylint: disable=line-too-long
                    "Product": parent.portal_type == "Product" and parent.Title() or "Default",  # noqa: E501
                    "ProductId": parent.portal_type == "Product" and api.content.get_uuid(obj=parent) or "",  # noqa: E501
                    "DatasetId": api.content.get_uuid(obj=dataset),
                    "DatasetTitle": dataset.Title(),
                    "DatasetDescription": dataset.Description(),
                    "ViewService": dataset.mapviewer_viewservice,
                    "Default_active": dataset.mapviewer_default_active,
                    "Layer": sorted(layers, key=lambda x: x.get("Title")),
                    "DownloadService": dataset.mapviewer_downloadservice,
                    "DownloadType": dataset.mapviewer_downloadtype,
                    "IsTimeSeries": dataset.mapviewer_istimeseries,
                    "TimeSeriesService": dataset.mapviewer_timeseriesservice,
                }

        return None
