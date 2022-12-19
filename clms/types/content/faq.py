# -*- coding: utf-8 -*-
"""
WorkOpportunity content-type definition
"""
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IFAQ(model.Schema):
    """Marker interface and Dexterity Python Schema for FAQ"""


@implementer(IFAQ)
class FAQ(Container):
    """FAQ content type class"""
