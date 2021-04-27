# -*- coding: utf-8 -*-
"""
DataSet content-type definition
"""
from clms.types import _
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IDataSet(model.Schema):
    """Marker interface and Dexterity Python Schema for DataSet"""

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('product.xml')

    accessAndUseConstraints = RichText(
        title=_(u"accessAndUseConstraints"), required=False
    )

    accessAndUseLimitationPublic = RichText(
        title=_(u"accessAndUseLimitationPublic"), required=False
    )

    # classificationTopicCategory = schema.List(
    #     title=_(u'classificationTopicCategory'),
    #     required=False
    # )

    conformitySpecification = RichText(
        title=_(u"conformitySpecification"), required=False
    )

    coordinateReferenceSystem = schema.TextLine(
        title=_(u"coordinateReferenceSystem"),
        required=False,
    )

    coverImage = namedfile.NamedBlobImage(
        title=_(u"coverImage"),
        required=False,
    )

    image = namedfile.NamedBlobImage(
        title=_(u"image"),
        required=False,
    )

    dataCustodians = RichText(title=_(u"dataCustodians"), required=False)

    dataResourceAbstract = RichText(
        title=_(u"dataResourceAbstract"), required=False
    )

    dataResourceLocator = schema.URI(
        title=_(u"dataResourceLocator"), required=False
    )

    dataResourceTitle = schema.TextLine(
        title=_(u"dataResourceTitle"),
        required=False,
    )

    # directives.widget(level=RadioFieldWidget)
    # dataResourceType = schema.Choice(
    #     title=_(u'dataResourceType'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    dataSources = RichText(title=_(u"dataSources"), required=False)

    descriptionDetailedMetadata = RichText(
        title=_(u"descriptionDetailedMetadata"), required=False
    )

    download = RichText(title=_(u"download"), required=False)

    embed = schema.SourceText(title=_(u"embed"), required=True)

    # directives.widget(level=RadioFieldWidget)
    # fileCategories = schema.Choice(
    #     title=_(u'fileCategories'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    geographicAccuracy = RichText(
        title=_(u"geographicAccuracy"), required=False
    )

    # geographicBoundingBox = schema.List(
    #     title=_(u'geographicBoundingBox'),
    #     required=False
    # )

    # geographicCoverage = schema.List(
    #     title=_(u'geographicCoverage'),
    #     required=False
    # )

    # geographicCoverageGT = schema.List(
    #     title=_(u'geographicCoverageGT'),
    #     required=False
    # )

    owners = RichText(title=_(u"owners"), required=False)

    qualityLineage = RichText(title=_(u"qualityLineage"), required=False)

    qualitySpatialResolution = RichText(
        title=_(u"qualitySpatialResolution"), required=False
    )

    responsiblePartyRole = RichText(
        title=_(u"responsiblePartyRole"), required=False
    )

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


@implementer(IDataSet)
class DataSet(Container):
    """ DataSet content-type class """
