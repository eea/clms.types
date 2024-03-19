# -*- coding: utf-8 -*-
"""
Product content-type definition
"""
from clms.types import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IProduct(model.Schema):
    """Marker interface and Dexterity Python Schema for Product"""

    mapviewer_message = schema.TextLine(
        title=_(
            "Message to be shown next to the product name in the data viewer",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )


@implementer(IProduct)
class Product(Container):
    """Product content type class"""
