"""
REST API endpoint to get the mapviewer configuration data
"""
from plone import api
from plone.restapi.services import Service


class RootMapViewerServiceGet(Service):
    """" Return the mapviewer configuration """

    def reply(self):
        """ main method """
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
            "Components": components,
        }

    def get_datasets(self):
        """ get all datasets """
        brains = api.content.find(
            portal_type="DataSet",
            context=api.portal.get_navigation_root(self.context),
        )
        return [brain.getObject() for brain in brains]

    def get_map_components(self):
        """ get dataset information grouped by components """
        components = {}
        datasets = self.get_datasets()
        for dataset in datasets:
            component = components.get(dataset.mapviewer_component, [])
            serialized_dataset = self.serialize_dataset(dataset)
            component.append(serialized_dataset)
            components[dataset.mapviewer_component] = component

        for key, value in components.items():
            yield {
                "title": key,
                "products": value,
            }

    def serialize_dataset(self, dataset):
        """ serialize one dataset using the keys needed by the mapviewer """
        layers = []
        layers_value = dataset.mapviewer_layers
        for layer_item in layers_value.get("items", []):
            layers.append(
                {
                    "LayerId": layer_item.get("id", ""),
                    "Title": layer_item.get("title", ""),
                }
            )

        return {
            "DatasetId": dataset.mapviewer_datasetid,
            "DatasetTitle": dataset.Title(),
            "DatasetDescription": dataset.Description(),
            "ViewService": dataset.mapviewer_viewservice,
            "Layer": layers,
            "DownloadService": dataset.mapviewer_downloadservice,
            "DownloadType": dataset.mapviewer_downloadtype,
            "IsTimeSeries": dataset.mapviewer_istimeseries,
            "TimeSeriesService": dataset.mapviewer_timeseriesservice,
        }
