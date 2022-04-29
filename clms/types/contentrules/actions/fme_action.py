# -*- coding: utf-8 -*-
""" A content rule to make a FME request"""
from logging import getLogger

from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions import ActionAddForm, ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope import schema
from zope.component import adapter
from zope.interface import Interface, implementer

from clms.types.contentrules.actions.fme_utils import usecase_to_discomap


class IFMEAction(Interface):
    """ Interface for the configurable aspects of the FME action"""

    operation = schema.Choice(
        title=_(
            u"Select the operation to notify",
        ),
        description=_(
            u"",
        ),
        vocabulary="clms.types.FMEOperationsVocabulary",
        default="INSERT",
        # defaultFactory=get_default_operation,
        required=True,
        readonly=False,
    )


@implementer(IFMEAction, IRuleElementData)
class FMEAction(SimpleItem):
    """The actual persistent implementation of the notify action element."""

    operation = "INSERT"

    element = "clms.types.actions.FMEAction"

    @property
    def summary(self):
        """ return the summary for the rule edit form """
        return _(
            u"Notify FME the following operation: ${operation}",
            mapping=dict(operation=self.operation),
        )


@adapter(Interface, IFMEAction, Interface)
@implementer(IExecutable)
class FMEActionExecutor:
    """The executor for this action.

    This is registered as an adapter in configure.zcml
    """

    def __init__(self, context, element, event):
        """ initialize """
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        """
        execute the rule
        """
        # self.context = The context where the rule is executed
        # (the containing folder)
        # self.element = The rule itself.
        # self.element.operation is the operation
        # self.event = The event that triggered the action
        # self.event.object = The object upon the event was triggered
        result = usecase_to_discomap(self.event.object, self.element.operation)

        log = getLogger(__name__)
        log.info(result.get("status", ""))
        log.info(result.get("msg", ""))
        return True


class FMEActionForm(ActionAddForm):
    """An add form for notify rule actions."""

    schema = IFMEAction
    label = _(u"Add FME Action")
    description = _(
        u"An action to inform FME about the changes of this object."
    )
    form_name = _(u"Configure element")
    Type = FMEAction


class FMEActionAddFormView(ContentRuleFormWrapper):
    """ add view """

    form = FMEActionForm


class FMEActionEditForm(ActionEditForm):
    """An edit form for notify rule actions.

    z3c.form does all the magic here.
    """

    schema = IFMEAction
    label = _(u"Edit FME Action")
    description = _(
        u"An action to inform FME about the changes of this object."
    )
    form_name = _(u"Configure element")


class FMEActionEditFormView(ContentRuleFormWrapper):
    """ edit view"""

    form = FMEActionForm
