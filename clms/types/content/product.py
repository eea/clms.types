# -*- coding: utf-8 -*-
"""
Product content-type definition
"""
from clms.types import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IProduct(model.Schema):
    """Marker interface and Dexterity Python Schema for Product"""


@implementer(IProduct)
class Product(Container):
    """Product content type class"""
