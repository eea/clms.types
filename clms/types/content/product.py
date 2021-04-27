# -*- coding: utf-8 -*-
from clms.types import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IProduct(model.Schema):
    """Marker interface and Dexterity Python Schema for Product"""

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('product.xml')

    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    # image = namedfile.NamedBlobImage(
    #     title=_(u'image'),
    #     required=False,
    # )

    # text = RichText(
    #     title=_(u'Text'),
    #     required=False
    # )

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(IProduct)
class Product(Container):
    """"""
