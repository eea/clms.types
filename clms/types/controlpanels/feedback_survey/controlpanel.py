"""
control panel to save feedback survey configuration
"""

# -*- coding: utf-8 -*-
from clms.types import _
from clms.types.interfaces import IClmsTypesLayer
from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.restapi.controlpanels.interfaces import IControlpanel
from plone.z3cform import layout
from zope import schema
from zope.component import adapter
from zope.interface import Interface, implementer


class IFeedbackSurveyControlPanel(IControlpanel):
    """marker interface for the control panel"""


class IFeedbackSurvey(Interface):
    """control panel schema"""

    is_active = schema.Bool(
        title=_("Is survey active?"),
        description=_("Check this to activate the survey."),
        required=False,
        default=False,
    )
    text = schema.TextLine(
        title=_("Survey text"),
        description=_("Example: Take a moment to fill out the CLMS Survey!"),
        required=False,
        default=_(""),
    )
    link = schema.TextLine(
        title=_("Survey link"),
        description=_("Example: https://ec.europa.eu/eusurvey/Survey2024"),
        required=False,
        default=_(""),
    )


class FeedbackSurveyView(RegistryEditForm):
    """control panel view"""

    schema = IFeedbackSurvey
    schema_prefix = "clms.types.feedback_survey"
    label = _("Feedback Survey Control Panel")


FeedbackSurveyViewView = layout.wrap_form(FeedbackSurveyView, ControlPanelFormWrapper)


@adapter(Interface, IClmsTypesLayer)
@implementer(IFeedbackSurveyControlPanel)
class FeedbackSurveyConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IFeedbackSurvey
    configlet_id = "feedback-survey-controlpanel"
    configlet_category_id = "Products"
    title = _("Feedback Survey Control Panel")
    group = ""
    schema_prefix = "clms.types.feedback_survey"
