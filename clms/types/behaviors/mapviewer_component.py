"""
mapviewer_component behavior
"""
# -*- coding: utf-8 -*-

from clms.types import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider


class IMapviewerComponentMarker(Interface):
    """ marker interface"""


@provider(IFormFieldProvider)
class IMapviewerComponent(model.Schema):
    """ interface definition """

    component_title = schema.TextLine(
        title=_(
            u"Component Title",
        ),
        description=_(
            u"This field is used to group datasets under a single "
            u"component in the mapviewer",
        ),
        default=u"Default",
        required=False,
        readonly=False,
    )


@implementer(IMapviewerComponent)
@adapter(IMapviewerComponentMarker)
class MapviewerComponent:
    """ behavior implementation """
    def __init__(self, context):
        self.context = context

    @property
    def component_title(self):
        """ getter """
        if safe_hasattr(self.context, "component_title"):
            return self.context.component_title
        return None

    @component_title.setter
    def component_title(self, value):
        """ setter """
        self.context.component_title = value
