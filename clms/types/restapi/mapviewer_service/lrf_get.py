"""
REST API endpoint to get the mapviewer configuration data
"""
import json
import re

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
                    "ComponentPosition": component.get("position"),
                    # pylint: disable=line-too-long
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
            "Download": False,
            # pylint: disable=line-too-long
            "Components": sorted(
                components, key=lambda x: x.get("ComponentPosition")
            ),  # noqa: E501
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
            (
                component_title,
                component_description,
                component_position,
            ) = component
            yield {
                "title": component_title,
                "description": component_description,
                "position": component_position,
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
                (
                    component_title,
                    component_description,
                    component_position,
                ) = self.get_component_info(
                    product
                )  # noqa: E501
                yield {
                    "Component": (
                        component_title,
                        component_description,
                        component_position,
                    ),
                    "ProductTitle": product.Title(),
                    "ProductDescription": product.Description(),
                    "ProductId": product.UID(),
                    # pylint: disable=line-too-long
                    "Datasets": sorted(
                        datasets, key=lambda x: x.get("PositionInParent")
                    ),  # noqa: E501
                    "PositionInParent": getObjPositionInParent(product),
                }

    def get_component_description(self, term):
        """get the component description"""
        available_components = api.portal.get_registry_record(
            "clms.types.product_component.product_components"
        )
        components = json.loads(available_components).get("items", [])
        for item in components:
            if item.get("@id") == term:
                return item.get("description", "")

        return ""

    def get_component_position(self, term):
        """get the component position"""
        available_components = api.portal.get_registry_record(
            "clms.types.product_component.product_components"
        )
        components = json.loads(available_components).get("items", [])
        for i, item in enumerate(components):
            if item.get("@id") == term:
                return i

        return 99

    def get_component_info(self, product):
        """get the component information for a product"""
        vocab = getUtility(
            IVocabularyFactory, name="clms.types.ComponentTitleVocabulary"
        )
        terms = vocab(product)
        try:
            term = terms.getTerm(product.mapviewer_component)
            description = self.get_component_description(term.value)
            position = self.get_component_position(term.value)
            return clean_component_title(term.title), description, position

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
                            "StaticImageLegend": layer_item.get(
                                "static_legend_url", ""
                            ),
                            "FilterStaticImageLegend": layer_item.get(
                                "filter_static_legend_url", ""
                            ),
                            "Fields": layer_item.get("fields", ""),
                        }
                    )
            if layers:
                parent = aq_parent(dataset)
                return {
                    # Datasets are saved inside product, so the Title name is
                    # its parent's name
                    # pylint: disable=line-too-long
                    "Product": parent.portal_type == "Product" and parent.Title() or "Default",  # noqa: E501
                    # pylint: disable=line-too-long
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
                    "MarkAsDownloadableNoServiceToVisualize": bool(
                        dataset.show_pop_up_in_mapviewer
                    ),
                    "DownloadLimitAreaExtent": dataset.download_limit_area_extent,
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


def clean_component_title(value):
    """ we are using 03#title like titles for components, to be able
        to sort them in a custom way in the search block, so
        here we need to clean the component title, so the map viewer
        gets the correct value
    """
    if '#' in value:
        new_value = re.sub("^[0-9][0-9]#", '', value)
        return new_value

    return value
