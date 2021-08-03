# -*- coding: utf-8 -*-
"""
UseCase content-type definition
"""

from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from clms.types import _


class IUseCase(model.Schema):
    """Marker interface for UseCase"""

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('use_case.xml')

    products = schema.List(
        title=_(
            u"CLMS products used",
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

    topics = schema.List(
        title=_(
            u"Use case topics",
        ),
        description=_(
            u"Multiple selection allowed",
        ),
        value_type=schema.Choice(
            title=_(
                u"Use case topics",
            ),
            vocabulary=u"clms.types.TopicsVocabulary",
            required=True,
            readonly=False,
        ),
        required=True,
        readonly=False,
    )

    outcome = schema.TextLine(
        title=_(u"User case outcome"),
        required=True,
    )

    links = schema.List(
        title=_(
            u"Links to use case",
        ),
        description=_(
            u"",
        ),
        value_type=schema.URI(
            title=u"",
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
