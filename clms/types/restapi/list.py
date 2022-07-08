# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.interface import implementer
from zope.schema.interfaces import IList

from clms.types.behaviors.dataset_relation import IDataSetRelationMarker
from clms.types.behaviors.product_relation import IProductRelationMarker
from clms.types.interfaces import IClmsTypesLayer


class BaseListFieldSerializer:
    def __init__(self, field, context, request):
        self.context = context
        self.request = request
        self.field = field

    def __call__(self):
        value = self.get_value()
        new_value = []
        for item in value:
            referenced_object = api.content.get(UID=item)
            if referenced_object:
                new_item = {}
                new_item.update(
                    {
                        "@id": referenced_object.absolute_url(),
                        "description": referenced_object.Description(),
                        "title": referenced_object.Title(),
                        "UID": item,
                        # hard-coded for now
                        "image_field": "image",
                    }
                )
                new_value.append(new_item)

        return json_compatible(new_value)

    def get_value(self, default=None):
        return getattr(
            self.field.interface(self.context), self.field.__name__, default
        )


@adapter(IList, IDataSetRelationMarker, IClmsTypesLayer)
@implementer(IFieldSerializer)
class DataSetRelationListFieldSerializer(BaseListFieldSerializer):
    pass


@adapter(IList, IProductRelationMarker, IClmsTypesLayer)
@implementer(IFieldSerializer)
class ProductRelationListFieldSerializer(BaseListFieldSerializer):
    pass
