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
            product = aq_parent(dataset)
            if product.portal_type == "Product":
                # get the component title from the Product
                component_title = product.component_title
            else:
                # This should not happen
                # add them to the 'Default' component
                component_title = "Default"
            component = components.get(component_title, [])
            serialized_dataset = self.serialize_dataset(dataset)
            if serialized_dataset is not None:
                component.append(serialized_dataset)
                components[component_title] = component

        for component_name, component_datasets in components.items():

            products = self.group_by_products(component_datasets)

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
            parent = aq_parent(dataset)
            return {
                # Datasets are saved inside product, so the Title name is its
                # parent's name
                # pylint: disable=line-too-long
                "Product": parent.portal_type == "Product" and \
                           parent.Title() or "Default",  # no-qa
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
