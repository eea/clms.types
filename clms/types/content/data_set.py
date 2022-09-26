# -*- coding: utf-8 -*-
"""
DataSet content-type definition
"""
import json

from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.schema.jsonfield import JSONField
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from collective import dexteritytextindexer
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

    model.fieldset(
        "metadata",
        label=_(u"Metadata"),
        fields=[
            # "validation",
            "dataResourceTitle",
            "resourceEffective",
            "resourceModified",
            # "dataResourceAbstract",
            "keywords",
            "geographicCoverage",
            "accessAndUseLimitationPublic_line",
            "accessAndUseConstraints",
            "qualitySpatialResolution_line",
            "classificationTopicCategory",
            "geographicBoundingBox",
            "temporalCoverage",
            "temporalExtentStart",
            "temporalExtentEnd",
            "gemet",
            "gemetInspireThemes",
            # "inspireThemes",
            # HIERARCHY LEVEL
            "dataResourceType",
            # CONTACT
            "responsiblePartyWithRole",
            # "responsibleParty",
            # "responsiblePartyRole",
            # REFERENCE SYSTEM INFO
            "coordinateReferenceSystemList",
            # "coordinateReferenceSystem",
            # DATA QUALITY INFO
            "conformitySpecification",
            "conformityPass",
            "qualityLineage",
            # DISTRIBUTION INFO
            "distributionInfo",
            # "dataResourceLocator",
            # "dataServices",
            # Non-visible metadata for the user
            "identifier",
            "point_of_contact_data",
            # "point_of_contact",
            "update_frequency",
            "distribution_format_list",
            "hierarchy_level",
            "metadata_language",
            "character_set",
            "date_stamp",
            "metadata_standard_name",
            "metadata_standard_version",
            "spatial_representation_type",
            # identifiers for the importation
            # "geonetwork_identifiers",
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
    dexteritytextindexer.searchable('validation')
    validation = RichText(title=_(u"Validation status"), required=False)

    dexteritytextindexer.searchable('dataResourceTitle')
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

    dexteritytextindexer.searchable('resourceEffective')
    resourceEffective = schema.Date(
        title=_(
            u"Date of publication",
        ),
        description=_(
            u"",
        ),
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('resourceModified')
    resourceModified = schema.Date(
        title=_(
            u"Revision date",
        ),
        description=_(
            u"",
        ),
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('dataResourceAbstract')
    dataResourceAbstract = RichText(
        title=_(u"Resource abstract"), required=False
    )

    dexteritytextindexer.searchable('keywords')
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

    dexteritytextindexer.searchable('accessAndUseLimitationPublic_line')
    accessAndUseLimitationPublic_line = schema.TextLine(
        title=_(u"Limitation of public access"), required=False
    )

    dexteritytextindexer.searchable('accessAndUseConstraints')
    accessAndUseConstraints = RichText(
        title=_(u"Conditions applying to access and use"), required=False
    )

    dexteritytextindexer.searchable('qualitySpatialResolution_line')
    qualitySpatialResolution_line = schema.TextLine(
        title=_(u"Spatial Resolution"), required=False
    )

    dexteritytextindexer.searchable('classificationTopicCategory')
    classificationTopicCategory = schema.List(
        title=_(
            u"Topic of Category",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=_(
                u"Use case topics",
            ),
            required=False,
            readonly=False,
        ),
        required=False,
        readonly=False,
    )

    geographicBoundingBox = JSONField(
        title=_(u"Bounding Box"),
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="bounding_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    dexteritytextindexer.searchable('temporalCoverage')
    temporalCoverage = schema.List(
        title=_(
            u"Temporal Extent",
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

    dexteritytextindexer.searchable('temporalExtentStart')
    temporalExtentStart = schema.TextLine(
        title=_(
            u"Temporal Extent Start",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('temporalExtentEnd')
    temporalExtentEnd = schema.TextLine(
        title=_(
            u"Temporal Extent End",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('gemet')
    gemet = schema.List(
        title=_(
            u"GEMET",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"THEME",
        ),
        required=False,
    )

    dexteritytextindexer.searchable('gemetInspireThemes')
    gemetInspireThemes = schema.List(
        title=_(
            u"GEMET INSPIRE Themes",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"INSPIRE THEME",
        ),
        required=False,
    )

    # HIERARCHY LEVEL
    #     Resource type: dataResourceType
    dexteritytextindexer.searchable('dataResourceType')
    dataResourceType = schema.TextLine(
        title=_(
            u"Resource Type",
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
    dexteritytextindexer.searchable('responsiblePartyWithRole')
    responsiblePartyWithRole = JSONField(
        title=u"Responsible Party with Role ",
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="contact_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    # responsibleParty = RichText(
    #     title=_(u"Responsible Party (DEPRECATED)"), required=False
    # )

    # responsiblePartyRole = RichText(
    #     title=_(u"Responsible Party Role (DEPRECATED)"), required=False
    # )

    # REFERENCE SYSTEM INFO
    #     Coordinate Reference System: coordinateReferenceSystem
    dexteritytextindexer.searchable('coordinateReferenceSystemList')
    coordinateReferenceSystemList = schema.List(
        title=_(u"Coordinate Reference System"),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"Reference",
        ),
        required=False,
    )

    # coordinateReferenceSystem = schema.TextLine(
    #     title=_(u"Coordinate Reference System (DEPRECATED)"),
    #     required=False,
    # )

    # DATA QUALITY INFO
    #     Specification: conformitySpecification
    #     Pass: conformityPass (conformityDegree)
    #     Lineage: qualityLineage
    dexteritytextindexer.searchable('conformitySpecification')
    conformitySpecification = RichText(
        title=_(u"Specification"), required=False
    )

    dexteritytextindexer.searchable('conformityPass')
    conformityPass = schema.Choice(
        title=_(u"Pass"),
        description=_(
            u"(true - if conformant, false - if not "
            "conformant, or Null - if not evaluated)",
        ),
        vocabulary=u"clms.types.ConformityPassVocabulary",
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('qualityLineage')
    qualityLineage = RichText(title=_(u"Lineage"), required=False)

    # DISTRIBUTION INFO
    #     Distribution Info: distributionInfo
    #     Resource Locator: dataResourceLocator (DEPRECATED)
    #     Services: dataServices (DEPRECATED)

    dexteritytextindexer.searchable('distributionInfo')
    distributionInfo = JSONField(
        title=u"Dataservices and each Resource Locator",
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="distribution_info_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    # dataResourceLocator = schema.URI(
    #     title=_(u"Data Resource Locator (DEPRECATED)"), required=False
    # )

    # dataServices = RichText(
    #     title=_(
    #         u"Dataservices (DEPRECATED)",
    #     ),
    #     required=False,
    #     readonly=False,
    # )

    # Non-visible metadata for the user
    #     Identifier: identifier
    #     Point of contact: point_of_contact
    #     Maintenance and update frequency: update_frequence
    #     Distribution format: distribution_format
    #     Hierarchy level: hierarchy_level
    #     Metadata language: metadata_language
    #     Character Set: character_set
    #     Date stamp: date_stamp
    #     Metadata standard name: metadata_standard_name
    #     Metadata standard version: metadata_standard_version

    dexteritytextindexer.searchable('identifier')
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

    # point_of_contact = RichText(
    #     title=_(
    #         u"Point of contact (DEPRECATED)",
    #     ),
    #     required=False,
    #     readonly=False,
    # )
    dexteritytextindexer.searchable('update_frequency')
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

    dexteritytextindexer.searchable('distribution_format_list')
    distribution_format_list = schema.List(
        title=_(
            u"Distribution format",
        ),
        value_type=schema.TextLine(
            title=u"Format",
        ),
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('hierarchy_level')
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

    dexteritytextindexer.searchable('metadata_language')
    metadata_language = schema.TextLine(
        title=_(
            u"Metadata Language",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('character_set')
    character_set = schema.TextLine(
        title=_(
            u"Character Set",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('date_stamp')
    date_stamp = schema.TextLine(
        title=_(
            u"Date Stamp",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('metadata_standard_name')
    metadata_standard_name = schema.TextLine(
        title=_(
            u"Metadata Standard Name",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('metadata_standard_version')
    metadata_standard_version = schema.TextLine(
        title=_(
            u"Metadata Standard Version",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('spatial_representation_type')
    spatial_representation_type = schema.List(
        title=_(
            u"Spatial representation type",
        ),
        value_type=schema.TextLine(
            title=u"Representation type",
        ),
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('citation')
    citation = RichText(title=_(u"Dataset citation"), required=False)

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
            "mapviewer_viewservice",
            "mapviewer_default_active",
            "mapviewer_layers",
            "mapviewer_istimeseries",
            "mapviewer_timeseriesservice",
            "mapviewer_handlinglevel",
        ],
    )

    dexteritytextindexer.searchable('mapviewer_viewservice')
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

    dexteritytextindexer.searchable('mapviewer_timeseriesservice')
    mapviewer_timeseriesservice = schema.TextLine(
        title=_(
            u"Time series and information service URL",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    dexteritytextindexer.searchable('mapviewer_handlinglevel')
    mapviewer_handlinglevel = schema.Bool(
        title=_(
            u"Handling level",
        ),
        description=_(""),
        required=False,
        default=False,
        readonly=False,
    )

    model.fieldset(
        "downloads",
        label=_(u"Downloads"),
        fields=[
            "downloadable_dataset",
            "downloadable_full_dataset",
            "downloadable_files",
            "dataset_download_information",
            # "dataset_full_path",
            # "dataset_full_format",
            # "dataset_full_source",
            # "wekeo_choices",
        ],
    )

    downloadable_dataset = schema.Bool(
        title=_(
            "Check if this dataset is downloadable",
        ),
        description=_(
            "If selected, a button will be shown in the dataset page to "
            "go to the download page of this dataset"
        ),
        required=False,
        default=True,
        readonly=False,
    )

    downloadable_full_dataset = schema.Bool(
        title=_(
            "Check if this dataset can be downloaded as a full dataset ",
        ),
        description=_(
            "If selected, an icon will be shown next to this dataset the map "
            " viewer to be able to download the full dataset"
        ),
        required=False,
        default=True,
        readonly=False,
    )

    dataset_download_information = JSONField(
        title=_("Dataset download information"),
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="dataset_download_information_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    # dataset_full_path = schema.TextLine(
    #     title=_(
    #         u"(DEPRECATED) Enter the path to the full dataset download file",
    #     ),
    #     description=_(
    #         u"This is used when requesting the download from the map viewer",
    #     ),
    #     default=u"",
    #     required=False,
    #     readonly=False,
    # )

    # dataset_full_format = schema.Choice(
    #     title=_(
    #         u"(DEPRECATED) Enter the format of the full dataset file",
    #     ),
    #     description=_(
    #         u"",
    #     ),
    #     vocabulary="clms.types.FullDatasetFormatsVocabulary",
    #     required=False,
    #     readonly=False,
    # )

    # dataset_full_source = schema.Choice(
    #     title=_(
    #         u"(DEPRECATED) Enter the source of the full dataset file",
    #     ),
    #     description=_(
    #         u"",
    #     ),
    #     vocabulary=u"clms.types.FullDatasetSourcesVocabulary",
    #     required=False,
    #     readonly=False,
    # )

    # wekeo_choices = schema.Text(
    #     title=_(
    #         "(DEPRECATED) WEKEO choices",
    #     ),
    #     description=_(""),
    #     default=u"",
    #     required=False,
    #     readonly=False,
    # )

    downloadable_files = JSONField(
        title=_("Downloadable files"),
        description=_("Add one line per file"),
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget="downloadable_files_widget",
        default={"items": []},
        missing_value={"items": []},
    )

    dexteritytextindexer.searchable('download_page_information')
    download_page_information = RichText(
        title=_("Download tab extra information"),
        description=_("This text will be shown in the download tab"),
        required=False,
    )


@implementer(IDataSet)
class DataSet(Container):
    """DataSet content-type class"""
