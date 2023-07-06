"""
control panel to save component configuration
"""
# -*- coding: utf-8 -*-
import json

from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.restapi.controlpanels.interfaces import IControlpanel
from plone.z3cform import layout
from zope.component import adapter
from zope.interface import Interface, Invalid, implementer
from zope.schema import SourceText

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
        ) from e
    if not isinstance(jv, dict):
        raise Invalid(
            _("invalid_cfg_no_dict", "JSON root must be a mapping (dict)")
        )
    return True


class IProductComponentControlPanel(IControlpanel):
    """marker interface for the control panel"""


class IProductComponent(Interface):
    """control panel schema"""

    product_components = SourceText(
        title=_("Product components"),
        description=_(
            "Add a valid JSON object with the configuration, on its root it"
            " must contain an 'items' key"
        ),
        required=False,
        default=(
            '{"items": [{"@id": "2a04c969-7f91-476f-8ab2-6fb4a7588896",'
            ' "description": "Land cover classifications complemented by'
            " detailed layers on vegetated and non-vegetated land cover"
            ' characteristics", "name": "01#Land Cover and Land Use Mapping"},'
            ' {"@id": "76c4d5c5-3da2-4abe-aba7-4eb9e23b2258", "description":'
            ' "Tailored land cover and land use information with a higher'
            " level of detail for specific areas of interest prone to"
            ' environmental changes", "name": "02#Priority Area Monitoring"},'
            ' {"@id": "38900ec1-a308-44f4-88c1-b4a9dd0fb2b8", "description":'
            ' "A series of qualified bio-geophysical products on the status'
            ' and evolution of the land surface", "name": "03#Bio-geophysical'
            ' Parameters"}, {"@id": "f6bcd2e4-c823-4617-8245-ebd406f65481",'
            ' "description": "Information on the natural and anthropogenic'
            ' ground motion throughout Europe", "name": "04#European Ground'
            ' Motion Service"}, {"@id":'
            ' "6bc28f66-6546-4c99-b13a-841668520ea1", "description":'
            ' "Satellite image mosaics from Copernicus and commercial'
            ' satellite missions monitoring land surface conditions ", "name":'
            ' "05#Satellite Data"}, {"@id":'
            ' "06b9468d-0c70-4221-b569-adb05faa9ba9", "name": "06#Reference'
            ' and Validation Data", "description": "Ground-based observations,'
            " geospatial reference data used in CLMS product creation or"
            ' validation"}]}'
        ),
        missing_value='{"items": []}',
        constraint=validate_cfg_json,
    )


class ProductComponentView(RegistryEditForm):
    """control panel view"""

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
