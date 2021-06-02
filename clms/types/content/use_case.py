# -*- coding: utf-8 -*-
"""
UseCase content-type definition
"""
from typing import Tuple
from clms.types import _

from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IUseCase(model.Schema):
    """ Marker interface for UseCase
    """

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('use_case.xml')

    responsibleOrganization = schema.TextLine(
        title=_(u"Responsible organization"),
        required=True,
    )

    contactName = schema.TextLine(
        title=_(u"Contact person name"),
        required=False,
    )

    contactEmail = schema.TextLine(
        title=_(u"Contact person email"),
        required=False,
    )
    # Make sure to import: plone.app.vocabularies as vocabs
    # topics = schema.Choice(
    #     title=_(
    #         u'Use case topics',
    #     ),
    #     vocabulary=u'vocabs.PortalTypes',
    #     default=u'',
    #     required=True,
    #     readonly=False,
    # )

    name = schema.List(
        title=_(
            u'Links to use case',
        ),
        description=_(
            u'',
        ),
        value_type=schema.URI(
            title=u'',
        ),
        required=True,
        readonly=False,
    )

    image = namedfile.NamedBlobImage(
        title=_(u"image"),
        required=False,
    )

@implementer(IUseCase)
class UseCase(Container):
    """ UseCase content-type class """
