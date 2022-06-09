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

    # title = schema.TextLine(
    #     title=_(u"Use Case Title"),
    #     required=True
    # )

    # summary = schema.TextLine(
    #     title=_(u"Use Case Summary"),
    #     required=False
    # )

    submittingProducionYear = schema.TextLine(
        title=_(u"Submitting producion year of Use Case"), required=False
    )

    responsibleOrganization = schema.TextLine(
        title=_(u"Responsible organization"),
        required=False,
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

    # documentLinks = schema.List(
    #     title=_(
    #         u"Links to use case documents",
    #     ),
    #     description=_(
    #         u"",
    #     ),
    #     value_type=schema.URI(
    #         title=u"",
    #     ),
    #     required=False,
    #     readonly=False,
    # )

    # videoLinks = schema.List(
    #     title=_(
    #         u"Links to use case videos",
    #     ),
    #     description=_(
    #         u"",
    #     ),
    #     value_type=schema.URI(
    #         title=u"",
    #     ),
    #     required=False,
    #     readonly=False,
    # )

    # websiteLinks = schema.List(
    #     title=_(
    #         u"Links to use case websites",
    #     ),
    #     description=_(
    #         u"",
    #     ),
    #     value_type=schema.URI(
    #         title=u"",
    #     ),
    #     required=False,
    #     readonly=False,
    # )

    image = namedfile.NamedBlobImage(
        title=_(u"image"),
        required=False,
    )

    geographicCoverage = schema.TextLine(
        title=_(u"Spatial coverage"),
        required=True,
    )

    # clms_products_used = schema.TextLine(
    #     title=_(u"Copernicus Land Monitoring Service products used"),
    #     required=True,
    # )


    bbox = schema.TextLine(
        title=_(u"Use Case BoundingBox"),
        required=False,
    )

    # upload_use_case_documents = schema.TextLine(
    #     title=_(u"Use Case document upload"),
    #     required=False,
    # )

    # upload_use_case_images = schema.TextLine(
    #     title=_(u"Use Case image upload"),
    #     required=False,
    # )

    # upload_use_case_videos = schema.TextLine(
    #     title=_(u"Use Case video upload"),
    #     required=False,
    # )

    # origin_name = schema.TextLine(
    #     title=_(u"Use Case origin name"),
    #     required=False,
    # )


@implementer(IUseCase)
class UseCase(Container):
    """UseCase content-type class"""
