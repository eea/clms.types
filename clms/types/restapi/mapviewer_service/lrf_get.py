"""
REST API endpoint to get the mapviewer configuration data
"""
from Acquisition import aq_parent
from plone import api
from plone.restapi.services import Service


class RootMapViewerServiceGet(Service):
    """ Return the mapviewer configuration"""

    def reply(self):
        """main method"""
        components = []

        for component in self.get_map_components():
            components.append(
                {
                    "ComponentTitle": component.get("title"),
                    "Products": component.get("products"),
                }
            )

        return {
            "Map": {
                "div": "mapDiv",
                "center": [15, 50],
                "zoom": 3,
            },
            "Download": False,
            "Components": components,
        }

    def get_datasets(self):
        """get all datasets"""
        brains = api.content.find(
            portal_type="DataSet",
            context=api.portal.get_navigation_root(self.context),
        )
        return [brain.getObject() for brain in brains]

    def get_map_components(self):
        """get dataset information grouped by components"""
        components = {}
        datasets = self.get_datasets()
        for dataset in datasets:
            component = components.get(dataset.mapviewer_component, [])
            serialized_dataset = self.serialize_dataset(dataset)
            if serialized_dataset is not None:
                component.append(serialized_dataset)
                components[dataset.mapviewer_component] = component

        for component_name in components.items():

            products = self.group_by_products(component)

            yield {
                "title": component_name,
                "products": products,
            }

    def group_by_products(self, datasets):
        """ group all datasets by product """
        products = {}
        for dataset in datasets:
            product = products.get(dataset.get("Product"), [])
            product.append(dataset)
            products[dataset.get("Product")] = product

        prepared_products = []
        for product_name, product_datasets in products.items():
            prepared_products.append(
                {
                    "ProductTitle": product_name,
                    "Datasets": product_datasets,
                }
            )

        return prepared_products

    def serialize_dataset(self, dataset):
        """serialize one dataset using the keys needed by the mapviewer"""
        if dataset.mapviewer_vieservice:
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

            return {
                # Datasets are saved inside product, so the Title name is its parent's name
                "Product": aq_parent(dataset).Title(),
                "DatasetId": api.content.get_uuid(obj=dataset),
                "DatasetTitle": dataset.Title(),
                "DatasetDescription": dataset.Description(),
                "ViewService": dataset.mapviewer_viewservice,
                "Default_active": dataset.mapviewer_default_active,
                "Layer": layers,
                "DownloadService": dataset.mapviewer_downloadservice,
                "DownloadType": dataset.mapviewer_downloadtype,
                "IsTimeSeries": dataset.mapviewer_istimeseries,
                "TimeSeriesService": dataset.mapviewer_timeseriesservice,
            }

        return None
