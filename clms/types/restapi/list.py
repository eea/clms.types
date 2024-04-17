"""
serializer for list-like fields
"""
# -*- coding: utf-8 -*-
from clms.types.behaviors.dataset_relation import IDataSetRelationMarker
from clms.types.behaviors.product_relation import IProductRelationMarker
from clms.types.content.use_case import IUseCase
from clms.types.interfaces import IClmsTypesLayer
from plone import api
from plone.restapi.interfaces import IFieldSerializer, ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxfields import CollectionFieldSerializer
from zExceptions import Unauthorized
from zope.component import adapter, getMultiAdapter
from zope.interface import implementer
from zope.schema.interfaces import IList


class BaseListFieldSerializer(CollectionFieldSerializer):
    """base serializer for list-like fields"""

    def __init__(self, field, context, request):
        """constructor"""
        self.context = context
        self.request = request
        self.field = field

    def __call__(self):
        """serializer implementation"""
        # Shortcut for taxonomy items. These are standard list fields
        # and they should be handled as they are
        if self.field.__name__.startswith("taxonomy_"):
            return json_compatible(super().__call__())

        # Specific implementation for those items having a UUID
        # We query the ISerializeToJsonSummary to have extra
        # information about them in the REST API
        value = self.get_value()
        new_value = []
        if value:
            for item in value:
                try:
                    referenced_object = api.content.get(UID=item)
                except Unauthorized:
                    # Handle non-existing objects
                    # or objects which we can't access
                    # Unauthorized errors
                    referenced_object = None
                if referenced_object:

                    new_item = getMultiAdapter(
                        (referenced_object, self.request),
                        ISerializeToJsonSummary,
                    )()
                    new_item["token"] = item

                    new_value.append(new_item)
                else:
                    new_value.append(item)

        return json_compatible(new_value)

    def get_value(self, default=None):
        """get the value of the field"""
        return getattr(
            self.field.interface(self.context), self.field.__name__, default
        )


@adapter(IList, IDataSetRelationMarker, IClmsTypesLayer)
@implementer(IFieldSerializer)
class DataSetRelationListFieldSerializer(BaseListFieldSerializer):
    """specific serializer for dataset relations"""


@adapter(IList, IProductRelationMarker, IClmsTypesLayer)
@implementer(IFieldSerializer)
class ProductRelationListFieldSerializer(BaseListFieldSerializer):
    """specific serializer for product relations"""


@adapter(IList, IUseCase, IClmsTypesLayer)
@implementer(IFieldSerializer)
class DataSetAndProductRelationListFieldSerializerUseCase(
    BaseListFieldSerializer
):
    """specific serializer for dataset relations"""
