# -*- coding: utf-8 -*-
"""
TechnicalLibrary content-type definition
"""
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from clms.types import _


class ITechnicalLibrary(model.Schema):
    """Marker interface and Dexterity Python Schema for TechnicalLibrary"""

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('product.xml')
    file = NamedBlobFile(title=_(u"File"), required=True)

    products = schema.List(
        title=_(
            u"CLMS associated products",
        ),
        description=_(
            u"Multiple selection allowed",
        ),
        value_type=schema.Choice(
            title=_(
                u"CLMS products used",
            ),
            vocabulary=u"clms.types.ProductsVocabulary",
            required=True,
            readonly=False,
        ),
        required=True,
        readonly=False,
    )


@implementer(ITechnicalLibrary)
class TechnicalLibrary(Container):
    """TechnicalLibrary content-type class"""
