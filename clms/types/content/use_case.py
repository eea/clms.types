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
        description=_(
            "Provide the name of the organisation that conducted the use case."
        ),
        required=True,
    )

    contactName = schema.TextLine(
        title=_(u"Contact person name"),
        description=_("Provide the use case focal point name."),
        required=False,
    )

    contactEmail = schema.TextLine(
        title=_(u"Contact person email"),
        description=_("Provide the use case focal point email."),
        required=False,
    )

    topics = schema.List(
        title=_(
            u"Use case topics",
        ),
        description=_(
            u"Choose at least one topic from the drop-down list. You can"
            u" consult more about the classification here:"
            # pylint: disable=line-too-long
            u" https://inspire.ec.europa.eu/glossary/MetadataElement-TopicCategory",  # noqa
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
        description=_(
            "Specify the use case result: Monitoring system/Web"
            " Application/Viewer/Modelling service, Bulletin, Publication,"
            " Study, Indicator(s), etc. "
        ),
        required=False,
    )

    image = namedfile.NamedBlobImage(
        title=_(u"Image"),
        description=_("Provide a representative picture of the use case."),
        required=False,
    )

    geographicCoverage = schema.List(
        title=_(u"Spatial coverage"),
        description=_(
            "Choose at least one value from the drop down list with the"
            " location represented by the data."
        ),
        required=True,
        value_type=schema.Choice(
            title=_(
                u"Spatial coverage",
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
