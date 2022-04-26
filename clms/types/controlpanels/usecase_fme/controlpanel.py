"""
control panel to save FME configuration for use-cases
"""
# -*- coding: utf-8 -*-

from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope import schema
from zope.component import adapter
from zope.interface import Interface

from clms.types import _
from clms.types.interfaces import IClmsTypesLayer


class IUseCaseFMEControlPanel(Interface):
    """ control panel schema"""

    fme_url = schema.URI(
        title=_(
            u"Enter the URL of FME",
        ),
        description=_(
            u"",
        ),
        default=u"https://fme.server.com",
        required=True,
        readonly=False,
    )

    token = schema.TextLine(
        title=_(
            u"Enter the authentication token for FME",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=True,
        readonly=False,
    )


class UseCaseControlPanelForm(RegistryEditForm):
    """ control panel view"""

    schema = IUseCaseFMEControlPanel
    schema_prefix = "clms.types.usecase_fme"
    label = _("Product Component Control Panel")


UseCaseControlPanelFormView = layout.wrap_form(
    UseCaseControlPanelForm, ControlPanelFormWrapper
)


@adapter(Interface, IClmsTypesLayer)
class UseCaseControlPanelFormConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IUseCaseFMEControlPanel
    configlet_id = "usecase-fme-controlpanel"
    configlet_category_id = "Products"
    title = _("FME Control Panel for Use Cases")
    group = ""
    schema_prefix = "clms.types.usecase_fme"
