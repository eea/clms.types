# -*- coding: utf-8 -*-
"""
WorkOpportunity content-type definition
"""
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IWorkOpportunity(model.Schema):
    """Marker interface and Dexterity Python Schema for WorkOpportunity"""


@implementer(IWorkOpportunity)
class WorkOpportunity(Container):
    """WorkOpportunity content type class"""
