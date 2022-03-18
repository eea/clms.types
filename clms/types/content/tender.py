# -*- coding: utf-8 -*-
"""
WorkOpportunity content-type definition
"""
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class ITender(model.Schema):
    """Marker interface and Dexterity Python Schema for WorkOpportunity"""


@implementer(ITender)
class Tender(Container):
    """Tender content type class"""
