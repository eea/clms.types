# -*- coding: utf-8 -*-
"""
TechnicalLibrary content-type definition
"""
from clms.types import _
from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from plone.supermodel.directives import primary
from zope import schema
from zope.interface import implementer


class ITechnicalLibrary(model.Schema):
    """Marker interface and Dexterity Python Schema for TechnicalLibrary"""

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('product.xml')
    primary("file")
    textindexer.searchable("file")
    file = NamedBlobFile(title=_(u"File"), required=True)

    publication_date = schema.Date(
        title=_(
            u"Enter the publication date of this document",
        ),
        description=_(
            u"",
        ),
        # defaultFactory=get_default_,
        required=False,
        readonly=False,
    )

    version = schema.TextLine(
        title=_(
            u"Enter the version of this document",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )


@implementer(ITechnicalLibrary)
class TechnicalLibrary(Container):
    """TechnicalLibrary content-type class"""
