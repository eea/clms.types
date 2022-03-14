from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.interface import implementer
from .controlpanel import IProductComponentControlPanel
import json


@implementer(ISerializeToJson)
@adapter(IProductComponentControlPanel)
class ProductComponentControlpanelSerializeToJson(ControlpanelSerializeToJson):
    def __call__(self):
        json_data = super(
            ProductComponentControlpanelSerializeToJson, self
        ).__call__()
        conf = json_data["data"].get("product_components", "")
        if conf:
            json_data["data"]["product_components"] = json.loads(
                json.loads(conf)
            )
        return json_data
