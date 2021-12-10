# -*- coding: utf-8 -*-
"""
DataSet content-type definition
"""
import json

from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.schema.jsonfield import JSONField
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from clms.types import _

MIXEDFIELD_SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {"type": "object", "properties": {}},
            }
        },
    }
)


class IDataSet(model.Schema):
    """Marker interface and Dexterity Python Schema for DataSet"""

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('product.xml')
    coverImage = namedfile.NamedBlobImage(
        title=_(u"coverImage"),
        required=False,
    )

    inspireThemes = schema.List(
        title=_(
            u"Inspire Themes",
        ),
        description=_(
            u"",
        ),
        value_type=schema.Choice(
            title=_(
                u"Inspire theme",
            ),
            vocabulary=u"clms.types.InspireThemesVocabulary",
            required=False,
            readonly=False,
        ),
        required=False,
        readonly=False,
    )

    model.fieldset(
        "metadata",
        label=_(u"Metadata"),
        fields=[
            "dataResourceTitle",
            "resourceEffective",
            "resourceModified",
            "dataResourceAbstract",
            "keywords",
            "geographicCoverage",
            "accessAndUseLimitationPublic",
            "accessAndUseConstraints",
            "qualitySpatialResolution",
            "classificationTopicCategory",
            "geographicBoundingBox",
            "temporalCoverage",
            "dataResourceType",
            "responsiblePartyWithRole",
            "responsibleParty",
            "responsiblePartyRole",
            "coordinateReferenceSystem",
            "conformitySpecification",
            "conformityPass",
            "qualityLineage",
            "distributionInfo",
            "dataResourceLocator",
            "dataServices",
            "identifier",
            "point_of_contact_data",
            "point_of_contact",
            "update_frequency",
            "distribution_format",
            "hierarchy_level",
            "geonetwork_identifiers",
        ],
    )

    # IDENTIFICATION INFO
    #     Resource title: dataResourceTitle
    #     Date of publication: resourceEffective
    #     Revision date: resourceModified
    #     Resource abstract: dataResourceAbstract
    #     Keywords: keywords
    #     Coverage: geographicCoverage
    #     Geotags : geographicCoverage
    #     Limitation of public access: accessAndUseLimitationPublic
    #     Conditions applying to access and use: accessAndUseConstraints
    #     Spatial resolution: qualitySpatialResolution
    #     Topic of category: classificationTopicCategory
    #     Bounding Box: geographicBoundingBox
    #     Temporal extent: temporalCoverage

    dataResourceTitle = schema.TextLine(
        title=_(
            u"Resource title",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    resourceEffective = schema.Date(
        title=_(
            u"Effective date",
        ),
        description=_(
            u"",
        ),
        # defaultFactory=get_default_name,
        required=False,
        readonly=False,
    )

    resourceModified = schema.Date(
        title=_(
            u"Modified date",
        ),
        description=_(
            u"",
        ),
        # defaultFactory=get_default_name,
        required=False,
        readonly=False,
    )

    dataResourceAbstract = RichText(
        title=_(u"Resource abstract"), required=False
    )

    keywords = schema.List(
        title=_(
            u"Keywords",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"Keyword",
        ),
        required=False,
        readonly=False,
    )

    geographicCoverage = JSONField(
        title=_(u"geographicCoverage"),
        required=False,
        widget="geolocation",
        default={},
    )

    # geographicCoverage = schema.List(
    #     title=_(u"Geographic Coverage",),
    #     description=_(u"",),
    #     value_type=schema.TextLine(title=u"",),
    #     required=False,
    #     readonly=False,
    # )

    # geographicCoverageGT = schema.List(
    #     title=_(u"Geographic Coverage GT",),
    #     description=_(u"",),
    #     value_type=schema.TextLine(title=u"",),
    #     required=False,
    #     readonly=False,
    # )

    accessAndUseLimitationPublic = schema.TextLine(
        title=_(u"Access And Use Limitation Public"), required=False
    )

    accessAndUseConstraints = RichText(
        title=_(u"Access And Use Constraints"), required=False
    )

    qualitySpatialResolution = RichText(
        title=_(u"Quality Spatial Resolution"), required=False
    )

    classificationTopicCategory = schema.List(
        title=_(
            u"Classification Topic Category",
        ),
        description=_(
            u"",
        ),
        value_type=schema.Choice(
            title=_(
                u"Use case topics",
            ),
            vocabulary=u"clms.types.CategoryTopicsVocabulary",
            required=False,
            readonly=False,
        ),
        required=False,
        readonly=False,
    )

    geographicBoundingBox = JSONField(
        title=u"Bounding box dataGrid field",
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="bounding_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    temporalCoverage = schema.List(
        title=_(
            u"Temporal Coverage",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"Year",
        ),
        required=False,
        readonly=False,
    )

    # HIERARCHY LEVEL
    #     Resource type: dataResourceType
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

    # CONTACT
    #     Responsible party with Role: responsiblePartyWithRole
    #     Responsible party: responsibleParty (DEPRECATED)
    #     Responsible party role: responsiblePartyRole (DEPRECATED)

    responsiblePartyWithRole = JSONField(
        title=u"Responsible Party with Role ",
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="contact_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    responsibleParty = RichText(
        title=_(u"Responsible Party (DEPRECATED)"), required=False
    )

    responsiblePartyRole = RichText(
        title=_(u"Responsible Party Role (DEPRECATED)"), required=False
    )

    # REFERENCE SYSTEM INFO
    #     Coordinate Reference System: coordinateReferenceSystem
    coordinateReferenceSystem = schema.List(
        title=_(u"Coordinate Reference System"),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"Reference",
        ),
        required=False,
    )

    # DATA QUALITY INFO
    #     Specification: conformitySpecification
    #     Pass: conformityPass (conformityDegree)
    #     Lineage: qualityLineage
    conformitySpecification = RichText(
        title=_(u"Conformity Specification"), required=False
    )

    conformityPass = schema.Choice(
        title=_(u"conformityPass"),
        description=_(
            u"(true - if conformant, false - if not "
            "conformant, or Null - if not evaluated)",
        ),
        vocabulary=u"clms.types.ConformityPassVocabulary",
        required=False,
        readonly=False,
    )

    qualityLineage = RichText(title=_(u"Quality Lineage"), required=False)

    # DISTRIBUTION INFO
    #     Distribution Info: distributionInfo
    #     Resource Locator: dataResourceLocator (DEPRECATED)
    #     Services: dataServices (DEPRECATED)

    distributionInfo = JSONField(
        title=u"Dataservices and each Resource Locator",
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="distribution_info_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    dataResourceLocator = schema.URI(
        title=_(u"Data Resource Locator (DEPRECATED)"), required=False
    )

    dataServices = RichText(
        title=_(
            u"Dataservices (DEPRECATED)",
        ),
        required=False,
        readonly=False,
    )

    # Non-visible metadata for the user
    #     Identifier: identifier
    #     Point of contact: point_of_contact
    #     Maintenance and update frequency: update_frequence
    #     Distribution format: distribution_format
    #     Hierarchy level: hierarchy_level
    #     Metadata language: AUTOMATIC
    #     Character Set: AUTOMATIC
    #     Date stamp: AUTOMATIC
    #     Metadata standard name: AUTOMATIC
    #     Metadata standard version: AUTOMATIC

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

    point_of_contact_data = JSONField(
        title=u"Point of contact Data",
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="contact_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    point_of_contact = RichText(
        title=_(
            u"Point of contact (DEPRECATED)",
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

    distribution_format = schema.TextLine(
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

    # geonetwork_identifier = schema.TextLine(
    #     title=_(
    #         u"GeoNetwork id",
    #     ),
    #     description=_(
    #         u"",
    #     ),
    #     default=u"",
    #     required=False,
    #     readonly=False,
    # )

    geonetwork_identifiers = JSONField(
        title=_("Geonetwork identifier list"),
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="geonetwork_identifiers_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    model.fieldset(
        "mapviewer",
        label=_(u"Mapviewer"),
        fields=[
            # "mapviewer_component",
            "mapviewer_viewservice",
            "mapviewer_default_active",
            "mapviewer_downloadservice",
            "mapviewer_layers",
            "mapviewer_downloadtype",
            "mapviewer_istimeseries",
            "mapviewer_timeseriesservice",
        ],
    )

    # mapviewer_component = schema.TextLine(
    #     title=_(
    #         u"Component Title",
    #     ),
    #     description=_(
    #         u"This field is used to group datasets under a singel component",
    #     ),
    #     default=u"Default",
    #     required=False,
    #     readonly=False,
    # )

    mapviewer_viewservice = schema.TextLine(
        title=_(
            u"View service",
        ),
        description=_(
            u"Enter the service url (WMS)",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    mapviewer_default_active = schema.Bool(
        title=_(
            u"Default active?",
        ),
        description=_(u"Enter whether is dataset should be active by default"),
        required=False,
        default=False,
        readonly=False,
    )

    mapviewer_layers = JSONField(
        title=_("Layers available in the map viewer"),
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="layer_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    mapviewer_downloadservice = schema.TextLine(
        title=_(
            u"Download service",
        ),
        description=_(
            u"This field is used to identify where the download files "
            "should come from",
        ),
        default=u"EEA",
        required=False,
        readonly=False,
    )

    mapviewer_downloadtype = schema.TextLine(
        title=_(
            u"Download type",
        ),
        description=_(
            u"This field is used to identify how the download should "
            u"be handled",
        ),
        default=u"ESRI REST service",
        required=False,
        readonly=False,
    )

    mapviewer_istimeseries = schema.Bool(
        title=_(
            u"Is time series?",
        ),
        description=_(
            u"Mark this field if this dataset contains time series "
            u" information and fill the next field with the time "
            u"series service url"
        ),
        required=False,
        default=False,
        readonly=False,
    )

    mapviewer_timeseriesservice = schema.TextLine(
        title=_(
            u"Time series service URL",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    model.fieldset(
        "downloads",
        label=_(u"Downloads"),
        fields=[
            "downloadable_files",
            "dataset_full_path",
        ],
    )

    downloadable_files = JSONField(
        title=_("Downloadable files"),
        description=_("Add one line per file"),
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="downloadable_files_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    dataset_full_path = schema.TextLine(
        title=_(
            u"Enter the path to the full dataset download file",
        ),
        description=_(
            u"This is used when requesting the download from the map viewer",
        ),
        default=u"",
        required=False,
        readonly=False,
    )


# Unused fields

# dataCustodians = RichText(title=_(u"dataCustodians"), required=False)

# dataSources = RichText(title=_(u"dataSources"), required=False)

# descriptionDetailedMetadata = RichText(
#     title=_(u"descriptionDetailedMetadata"), required=False
# )

# download = RichText(title=_(u"download"), required=False)

# embed = schema.SourceText(title=_(u"embed"), required=False)

# geographicAccuracy = RichText(
#     title=_(u"geographicAccuracy"), required=False
# )

# owners = RichText(title=_(u"owners"), required=False)


# model.fieldset(
#     "default",
#     label=_("Identification info"),
#     fields=["title", "IPublication.effective"],
# )


@implementer(IDataSet)
class DataSet(Container):
    """DataSet content-type class"""
