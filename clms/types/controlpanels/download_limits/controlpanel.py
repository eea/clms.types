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
from zope.interface import Interface, implementer

from clms.types import _
from clms.types.interfaces import IClmsTypesLayer
from zope import schema


class IDownloadLimitsControlPanel(IControlpanel):
    """marker interface for the control panel"""


class IDownloadLimits(Interface):
    """control panel schema"""

    area_extent = schema.Int(
        title=_(
            "Area extent max for downloads",
        ),
        description=_(
            "This number defines the maximun area to be downloaded by "
            "rectangle in the data viewer. It is an adimensional number. "
            "1600000000000 value, will allow to download data for a size "
            "similar to the Iberian Peninsula.",
        ),
        required=False,
        default=1600000000000,
    )


class DownloadLimitsView(RegistryEditForm):
    """control panel view"""

    schema = IDownloadLimits
    schema_prefix = "clms.types.download_limits"
    label = _("Download Limits Control Panel")


DownloadLimitsViewView = layout.wrap_form(
    DownloadLimitsView, ControlPanelFormWrapper
)


@adapter(Interface, IClmsTypesLayer)
@implementer(IDownloadLimitsControlPanel)
class DownloadLimitsConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IDownloadLimits
    configlet_id = "download-limits-controlpanel"
    configlet_category_id = "Products"
    title = _("Download Limits Control Panel")
    group = ""
    schema_prefix = "clms.types.download_limits"
