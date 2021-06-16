# -*- coding: utf-8 -*-
"""
DataSet content-type definition
"""
from plone.app.textfield import RichText
from clms.types import _
from plone.autoform.directives import widget
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import implementer, Interface

import json
from plone.schema.jsonfield import JSONField

MIXEDFIELD_SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {}}}},
    }
)


class IDataSet(model.Schema):
    """Marker interface and Dexterity Python Schema for DataSet"""

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('product.xml')

    accessAndUseConstraints = RichText(
        title=_(u"Access And Use Constraints"), required=False
    )

    accessAndUseLimitationPublic = RichText(
        title=_(u"Access And Use Limitation Public"), required=False
    )

    classificationTopicCategory = schema.List(
        title=_(
            u"Classification Topic Category",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"",
        ),
        required=False,
        readonly=False,
    )

    conformitySpecification = RichText(
        title=_(u"Conformity Specification"), required=False
    )

    conformityPass = RichText(title=_(u"conformityPass"), required=False)

    coordinateReferenceSystem = schema.TextLine(
        title=_(u"Coordinate Reference System"),
        required=False,
    )

    # coverImage = namedfile.NamedBlobImage(
    #     title=_(u"coverImage"),
    #     required=False,
    # )

    image = namedfile.NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )

    # dataCustodians = RichText(title=_(u"dataCustodians"), required=False)

    # dataResourceAbstract = RichText(
    #     title=_(u"dataResourceAbstract"), required=False
    # )

    dataResourceLocator = schema.URI(
        title=_(u"Data Resource Locator"), required=False
    )

    # dataResourceTitle = schema.TextLine(
    #     title=_(u"dataResourceTitle"),
    #     required=False,
    # )

    # Make sure to import: plone.app.textfield
    dataServices = RichText(
        title=_(
            u"Dataservices",
        ),
        required=False,
        readonly=False,
    )

    dataResourceType = schema.TextLine(
        title=_(
            u"Data Resource Type",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    # dataSources = RichText(title=_(u"dataSources"), required=False)

    # descriptionDetailedMetadata = RichText(
    #     title=_(u"descriptionDetailedMetadata"), required=False
    # )

    # download = RichText(title=_(u"download"), required=False)

    # embed = schema.SourceText(title=_(u"embed"), required=True)

    # geographicAccuracy = RichText(
    #     title=_(u"geographicAccuracy"), required=False
    # )


    bounding_field = JSONField(
        title=u'Bounding box dataGrid field',
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="bounding_widget",
        default={"items": []},
        missing_value={"items": []},
        )

    geographicCoverage = schema.List(
        title=_(
            u"Geographic Coverage",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"",
        ),
        required=False,
        readonly=False,
    )

    geographicCoverageGT = schema.List(
        title=_(
            u"Geographic Coverage GT",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"",
        ),
        required=False,
        readonly=False,
    )

    # owners = RichText(title=_(u"owners"), required=False)

    qualityLineage = RichText(title=_(u"Quality Lineage"), required=False)

    qualitySpatialResolution = RichText(
        title=_(u"Quality Spatial Resolution"), required=False
    )

    responsibleParty = RichText(title=_(u"Responsible Party"), required=False)

    responsiblePartyRole = RichText(
        title=_(u"Responsible Party Role"), required=False
    )

    identifier = schema.TextLine(
        title=_(
            u"Identifier",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    # Make sure to import: plone.app.textfield
    point_of_contact = RichText(
        title=_(
            u"Point of contact",
        ),
        required=False,
        readonly=False,
    )

    update_frequency = schema.TextLine(
        title=_(
            u"Update Frequency",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    # Make sure to import: plone.app.textfield
    distribution_format = RichText(
        title=_(
            u"Distribution format",
        ),
        required=False,
        readonly=False,
    )

    hierarchy_level = schema.TextLine(
        title=_(
            u"Hierarchy level",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    geonetwork_identifier = schema.TextLine(
        title=_(
            u"GeoNetwork id",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )


"""
IDENTIFICATION INFO
    Resource title: title
    Date of publication: effective
    Revision date: modified
    Resource abstract: description
    Keywords: subject
    Coverage: geographicCoverage
    Geotags : geographicCoverageGT
    Limitation of public access: accessAndUseLimitationPublic
    Conditions applying to access and use: accessAndUseConstraints
    Spatial resolution: qualitySpatialResolution
    Topic of category: classificationTopicCategory
    Bounding Box: geographicBoundingBox
    Temporal extent

HIERARCHY LEVEL
    Resource type: dataResourceType

CONTACT
    Responsible party: responsibleParty
    Responsible party role: responsiblePartyRole

REFERENCE SYSTEM INFO
    Coordinate Reference System: coordinateReferenceSystem

DATA QUALITY INFO
    Specification: conformitySpecification
    Pass: conformityPass
    Lineage: qualityLineage

DISTRIBUTION INFO
    Resource Locator: dataResourceLocator
    Services: dataServices

Non-visible metadata for the user
    Identifier: identifier
    Metadata language: AUTOMATIC
    Character Set: AUTOMATIC
    Date stamp: AUTOMATIC
    Metadata standard name: AUTOMATIC
    Metadata standard version: AUTOMATIC
    Point of contact: point_of_contact
    Maintenance and update frequency: update_frequence
    Distribution format: distribution_format
    Hierarchy level: hierarchy_level
"""


# model.fieldset(
#     "default",
#     label=_("Identification info"),
#     fields=["title", "IPublication.effective"],
# )


@implementer(IDataSet)
class DataSet(Container):
    """ DataSet content-type class """
