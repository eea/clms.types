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

    submittingProducionYear = schema.TextLine(
        title=_(u"Submitting producion year of Use Case"),
        description=_(
            "Provide the year or a year interval in which the use case was"
            " produced, for example: 2019 or 2019-2022"
        ),
        required=True,
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
        required=False,
    )

    image = namedfile.NamedBlobImage(
        title=_(u"image"),
        required=False,
    )

    geographicCoverage = schema.List(
        title=_(u"Spatial coverage"),
        required=True,
        value_type=schema.Choice(
            title=_(
                u"Spatial coverag",
            ),
            vocabulary=u"clms.types.UseCaseSpatialCoverageVocabulary",
            required=True,
            readonly=False,
        ),
        readonly=False,
    )


@implementer(IUseCase)
class UseCase(Container):
    """UseCase content-type class"""
