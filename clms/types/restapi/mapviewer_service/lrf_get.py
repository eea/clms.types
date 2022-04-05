"""
REST API endpoint to get the mapviewer configuration data
"""
import json

from Acquisition import aq_inner, aq_parent
from OFS.interfaces import IOrderedContainer
from plone import api
from plone.restapi.services import Service
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


def getObjPositionInParent(obj):
    """get the position of the object in the parent"""
    parent = aq_parent(aq_inner(obj))
    ordered = IOrderedContainer(parent, None)
    if ordered is not None:
        return ordered.getObjectPosition(obj.getId())
    return 0


class RootMapViewerServiceGet(Service):
    """Return the mapviewer configuration"""

    def reply(self):
        """main method"""
        components = []

        for component in self.get_map_components():
            components.append(
                {
                    "ComponentTitle": component.get("title"),
                    "ComponentDescription": component.get("description"),
                    # pylint: disable=line-too-long
                    "Products": sorted(component.get("products"), key=lambda x: x.get("PositionInParent")),  # noqa: E501
                }
            )

        return {
            "Map": {
                "div": "mapDiv",
                "center": [15, 50],
                "zoom": 3,
            },
            "Download": False,
            # pylint: disable=line-too-long
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
            component_title, component_description = component
            yield {
                "title": component_title,
                "description": component_description,
                "products": products,
            }

    def get_products(self):
        """get all products"""
        brains = api.content.find(
            portal_type="Product",
            context=api.portal.get_navigation_root(self.context),
        )
        for brain in brains:
            product = brain.getObject()
            datasets = self.get_datasets_for_product(product)
            if datasets:
                # pylint: disable=line-too-long
                component_title, component_description = self.get_component_info(product)  # noqa: E501
                yield {
                    "Component": (component_title, component_description),
                    "ProductTitle": product.Title(),
                    "ProductDescription": product.Description(),
                    "ProductId": product.UID(),
                    # pylint: disable=line-too-long
                    "Datasets": sorted(datasets, key=lambda x: x.get("PositionInParent")),  # noqa: E501
                    "PositionInParent": getObjPositionInParent(product),
                }

    def get_component_description(self, term):
        """get the component description"""
        available_components = api.portal.get_registry_record(
            'clms.types.product_component.product_components')
        components = json.loads(available_components).get('items', [])
        for item in components:
            if item.get('@id') == term:
                return item.get('description', "")

        return ""

    def get_component_info(self, product):
        """get the component information for a product"""
        vocab = getUtility(
            IVocabularyFactory,
            name="clms.types.ComponentTitleVocabulary"
        )
        terms = vocab(product)
        try:
            term = terms.getTerm(product.mapviewer_component)
            description = self.get_component_description(term.value)
            return term.title, description

        except LookupError:
            return "", ""

    def get_datasets_for_product(self, product):
        """get all datasets for a product"""
        datasets = []
        brains = api.content.find(
            portal_type="DataSet",
            context=product,
        )
        for brain in brains:
            dataset = brain.getObject()
            serialized_dataset = self.serialize_dataset(dataset)
            if serialized_dataset is not None:
                datasets.append(serialized_dataset)

        return datasets

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
                return {
                    # Datasets are saved inside product, so the Title name is
                    # its parent's name
                    # pylint: disable=line-too-long
                    "Product": parent.portal_type == "Product" and parent.Title() or "Default",  # noqa: E501
                    "ProductId": parent.portal_type == "Product" and api.content.get_uuid(obj=parent) or "",  # noqa: E501
                    "DatasetId": api.content.get_uuid(obj=dataset),
                    "DatasetTitle": dataset.Title(),
                    "DatasetDescription": dataset.Description(),
                    "DatasetURL": self.get_item_volto_url(dataset),
                    "ViewService": dataset.mapviewer_viewservice,
                    "Default_active": dataset.mapviewer_default_active,
                    "Layer": layers,
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
