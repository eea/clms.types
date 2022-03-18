""" specific deserializer for the control panel"""
# -*- coding: utf-8 -*-
import json

from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import \
    ControlpanelDeserializeFromJson
from plone.restapi.interfaces import IDeserializeFromJson
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer

from .controlpanel import IProductComponentControlPanel


@implementer(IDeserializeFromJson)
@adapter(IProductComponentControlPanel)
class ProductComponentControlpanelDeserializeFromJson(
    ControlpanelDeserializeFromJson
):
    """ deserializer class """
    def __call__(self):
        """ deserializer call """
        req = json_body(self.controlpanel.request)
        proxy = self.registry.forInterface(
            self.schema, prefix=self.schema_prefix
        )
        errors = []

        configurations = req.get("product_components", {})
        if not configurations:
            errors.append(
                {
                    "message": "Missing data",
                    "field": "product_components",
                }
            )
            raise BadRequest(errors)
        try:
            value = json.dumps(configurations)
            setattr(proxy, "product_components", value)
        except ValueError as e:
            errors.append(
                {
                    "message": str(e),
                    "field": "product_components",
                    "error": e,
                }
            )

        if errors:
            raise BadRequest(errors)
