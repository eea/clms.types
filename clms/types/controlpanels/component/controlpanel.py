# -*- coding: utf-8 -*-
import json

from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope.component import adapter
from zope.interface import Interface, Invalid, implementer
from zope.schema import SourceText
from plone.restapi.controlpanels.interfaces import IControlpanel
from clms.types import _
from clms.types.interfaces import IClmsTypesLayer

MIXEDFIELD_SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {"type": "object", "properties": {}},
            }
        },
    }
)


def validate_cfg_json(value):
    """check that we have at least valid json and its a dict"""
    try:
        jv = json.loads(value)
    except ValueError as e:
        raise Invalid(
            _(
                "invalid_json",
                "JSON is not valid, parser complained: ${message}",
                mapping={"message": e.message},
            )
        )
    if not isinstance(jv, dict):
        raise Invalid(
            _("invalid_cfg_no_dict", "JSON root must be a mapping (dict)")
        )
    return True


class IProductComponentControlPanel(IControlpanel):
    pass


class IProductComponent(Interface):
    product_components = SourceText(
        title=_("Product components"),
        description=_(
            "Add a valid JSON object with the configuration, on its root it"
            " must contain an 'items' key"
        ),
        required=False,
        default='{"items": []}',
        missing_value='{"items": []}',
        constraint=validate_cfg_json,
    )


class ProductComponentView(RegistryEditForm):
    schema = IProductComponent
    schema_prefix = "clms.types.product_component"
    label = _("Product Component Control Panel")


ProductComponentViewView = layout.wrap_form(
    ProductComponentView, ControlPanelFormWrapper
)


@adapter(Interface, IClmsTypesLayer)
@implementer(IProductComponentControlPanel)
class ProductComponentConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IProductComponent
    configlet_id = "product-component-controlpanel"
    configlet_category_id = "Products"
    title = _("Product Component Control Panel")
    group = ""
    schema_prefix = "clms.types.product_component"
