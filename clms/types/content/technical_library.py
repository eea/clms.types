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

    document_product = schema.TextLine(
        title=_(
            u'document_product (used for import from old site',
        ),
        description=_(
            u'',
        ),
        default=u'',
        required=False,
        readonly=False,
    )
    document_type = schema.TextLine(
        title=_(
            u'document_type (used for import from old site',
        ),
        description=_(
            u'',
        ),
        default=u'',
        required=False,
        readonly=False,
    )
    document_title = schema.TextLine(
        title=_(
            u'document_title (used for import from old site',
        ),
        description=_(
            u'',
        ),
        default=u'',
        required=False,
        readonly=False,
    )
    document_url = schema.TextLine(
        title=_(
            u'document_url (used for import from old site',
        ),
        description=_(
            u'',
        ),
        default=u'',
        required=False,
        readonly=False,
    )
    document_file = schema.TextLine(
        title=_(
            u'document_file (used for import from old site',
        ),
        description=_(
            u'',
        ),
        default=u'',
        required=False,
        readonly=False,
    )

# document_product
# document_type
# document_title
# document_url
# document_file


@implementer(ITechnicalLibrary)
class TechnicalLibrary(Container):
    """TechnicalLibrary content-type class"""
