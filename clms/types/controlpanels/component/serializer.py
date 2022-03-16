""" specific serializer for the control panel"""
# -*- coding: utf-8 -*-
import json

from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from zope.component import adapter
from zope.interface import implementer

from .controlpanel import IProductComponentControlPanel


@implementer(ISerializeToJson)
@adapter(IProductComponentControlPanel)
class ProductComponentControlpanelSerializeToJson(ControlpanelSerializeToJson):
    """ serializer adapter """
    def __call__(self):
        """ serializer call"""
        json_data = super().__call__()
        conf = json_data["data"].get("product_components", "")
        if conf:
            json_data["data"]["product_components"] = json.loads(conf)
        return json_data
