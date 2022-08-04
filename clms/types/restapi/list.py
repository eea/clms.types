"""
serializer for list-like fields
"""
# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IFieldSerializer, ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter, getMultiAdapter
from zope.interface import implementer
from zope.schema.interfaces import IList

from clms.types.behaviors.dataset_relation import IDataSetRelationMarker
from clms.types.behaviors.product_relation import IProductRelationMarker
from clms.types.interfaces import IClmsTypesLayer
from clms.types.content.use_case import IUseCase


class BaseListFieldSerializer:
    """base serializer for list-like fields"""

    def __init__(self, field, context, request):
        """constructor"""
        self.context = context
        self.request = request
        self.field = field

    def __call__(self):
        """serializer implementation"""
        value = self.get_value()
        new_value = []
        if value:
            for item in value:
                referenced_object = api.content.get(UID=item)
                if referenced_object:

                    new_item = getMultiAdapter(
                        (referenced_object, self.request),
                        ISerializeToJsonSummary,
                    )()
                    new_item["token"] = item

                    new_value.append(new_item)

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
