# -*- coding: utf-8 -*-
"""
DataSet content-type definition
"""
import json

from clms.types import _
from plone.app.dexterity import textindexer
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.schema.jsonfield import JSONField
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from plone.app.z3cform.widget import SingleCheckBoxBoolFieldWidget
from plone.autoform import directives

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
        "characteristics",
        label=_("Dataset characteristics"),
        fields=[
            "characteristics_type",
            "characteristics_spatial_coverage",
            "characteristics_spatial_resolution",
            "characteristics_spatial_representation_type",
            "characteristics_temporal_extent",
            "characteristics_temporal_usability",
            "characteristics_update_frequency",
            "characteristics_timeliness",
            "characteristics_platform",
            "characteristics_sensor",
            "characteristics_thematic_accuracy",
            "characteristics_position_accuracy",
            "characteristics_release_major_version",
        ],
    )
    textindexer.searchable("characteristics_type")
    characteristics_type = schema.Choice(
        title=_(
            u"Type",
        ),
        description=_(
            u"Type of observations",
        ),
        values=[
            "Satellite observations",
            "Satellite products",
            "In situ observations",
        ],
        # defaultFactory=get_default_name,
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_spatial_coverage")
    characteristics_spatial_coverage = schema.TextLine(
        title=_(
            u"Spatial coverage",
        ),
        description=_(
            u"The area of interest represented in the dataset",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_spatial_resolution")
    characteristics_spatial_resolution = schema.TextLine(
        title=_(
            u"Spatial resolution",
        ),
        description=_(
            u"Level of detail of the data set. Enter resolution distance with"
            u" units",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_spatial_representation_type")
    characteristics_spatial_representation_type = schema.Choice(
        title=_(
            u"Spatial representation type",
        ),
        description=_(
            u"Method used for spatial representation of geographical"
            u" information",
        ),
        values=["Grid", "Vector", "Vector and Grid"],
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_temporal_extent")
    characteristics_temporal_extent = schema.TextLine(
        title=_(
            u"Temporal extent",
        ),
        description=_(
            "Time period covered by the content of the dataset (data"
            " collection period). Use YYYY for a specific year. Use YYYY -"
            " YYYY for a defined time period. Use YYYY - now for open-ended"
            " datasets ",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_temporal_usability")
    characteristics_temporal_usability = schema.Choice(
        title=_(
            "Temporal usability",
        ),
        description=_(
            "Temporal appliance related to the dataset update frequency:"
            "Archive-only data (no updates)"
            "Current = archive with regular updates"
            "Future = forecasts",
        ),
        values=[
            "Archive-only (no updates)",
            "Archive with regular updates",
            "Forecasts",
        ],
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_update_frequency")
    characteristics_update_frequency = schema.Choice(
        title=_(
            u"Update frequency",
        ),
        description=_(
            u"Frequency with which modifications and deletions are made to the"
            u" data after it is first produced",
        ),
        values=[
            "Annually",
            "AsNeeded",
            "Biannually",
            "Continual",
            "Daily",
            "Fortnightly",
            "Irregular",
            "Monthly",
            "NotPlanned",
            "Quaterly",
            "Unknown",
            "Weekly",
            "3-yearly",
            "6-yearly",
        ],
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_timeliness")
    characteristics_timeliness = schema.TextLine(
        title=_(
            u"Timeliness",
        ),
        description=_(
            u"How fast each update is made available to the user counting from"
            u" the moment of the availability of the input data.",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_platform")
    characteristics_platform = schema.TextLine(
        title=_(
            u"Platform",
        ),
        description=_(
            u"Name of satellite family or ground base station",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_sensor")
    characteristics_sensor = schema.TextLine(
        title=_(
            u"Sensor",
        ),
        description=_(
            u"Name of the instrument for detecting energy.",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_thematic_accuracy")
    characteristics_thematic_accuracy = schema.TextLine(
        title=_(
            u"Thematic accuracy",
        ),
        description=_(
            u"Refers to how well the class name on the map correspond to what"
            u" is really on the ground. It can be expressed something like: "
            u"Expected overall accuracy is greater than 85% ",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_position_accuracy")
    characteristics_position_accuracy = schema.TextLine(
        title=_(
            u"Position accuracy",
        ),
        description=_(
            u"Indicator or measure of how a spatial object is accurately"
            u" positioned on the map with respect to its true position.",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    textindexer.searchable("characteristics_release_major_version")
    characteristics_release_major_version = schema.TextLine(
        title=_(
            u"Release / Major version",
        ),
        description=_(
            u"Name given for the release that consists of major new features"
            u" or existing features that might have been deprecated.",
            u"V + number.Example: V2",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    model.fieldset(
        "jrc_data",
        label=_("JRC Data"),
        fields=[
            "jrc_algorithm",
            "jrc_quality",
            "jrc_datalayers",
            # "jrc_show_technical_documents",
            "jrc_show_related_datasets",
        ],
    )

    # Make sure to import: from plone.app.textfield import RichText
    textindexer.searchable("jrc_algorithm")
    jrc_algorithm = RichText(
        title=_(
            "Algorithm",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )

    # Make sure to import: from plone.app.textfield import RichText
    textindexer.searchable("jrc_quality")
    jrc_quality = RichText(
        title=_(
            "Quality",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )

    # Make sure to import: from plone.app.textfield import RichText
    textindexer.searchable("jrc_datalayers")
    jrc_datalayers = RichText(
        title=_(
            "Datalayers",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )

    # Make sure you import:
    # plone.app.z3cform.widget.SingleCheckBoxBoolFieldWidget
    # directives.widget(
    #     jrc_show_technical_documents=SingleCheckBoxBoolFieldWidget
    # )
    # jrc_show_technical_documents = schema.Bool(
    #     title=_(
    #         u"Show technical documents?",
    #     ),
    #     description=_(
    #         u"If checked an accordion with related technical documents will be"
    #         u" shown in the dataset page.",
    #     ),
    #     required=False,
    #     default=False,
    #     readonly=False,
    # )

    # Make sure you import:
    # plone.app.z3cform.widget.SingleCheckBoxBoolFieldWidget
    directives.widget(jrc_show_related_datasets=SingleCheckBoxBoolFieldWidget)
    jrc_show_related_datasets = schema.Bool(
        title=_(
            u"Show related datasets?",
        ),
        description=_(
            u"If checked an accordion with related datasets will be shown in"
            u" the dataset page.",
        ),
        required=False,
        default=False,
        readonly=False,
    )

    model.fieldset(
        "metadata",
        label=_(u"Metadata"),
        fields=[
            # "validation",
            # "dataResourceTitle",
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
    textindexer.searchable("validation")
    validation = RichText(title=_(u"Validation status"), required=False)

    # textindexer.searchable("dataResourceTitle")
    # dataResourceTitle = schema.TextLine(
    #     title=_(
    #         u"Resource title",
    #     ),
    #     description=_(
    #         u"",
    #     ),
    #     default=u"",
    #     required=False,
    #     readonly=False,
    # )

    textindexer.searchable("resourceEffective")
    resourceEffective = schema.Date(
        title=_(
            u"Metadata date stamp",
        ),
        description=_(
            u"",
        ),
        required=False,
        readonly=False,
    )

    textindexer.searchable("resourceModified")
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

    textindexer.searchable("dataResourceAbstract")
    dataResourceAbstract = RichText(
        title=_(u"Resource abstract"), required=False
    )

    textindexer.searchable("keywords")
    keywords = schema.List(
        title=_(
            u"Keywords",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"Keyword",
            required=False,
            readonly=False,
        ),
        required=False,
        readonly=False,
    )

    # geographicCoverage = JSONField(
    #     title=_(u"geographicCoverage"),
    #     required=False,
    #     widget="geolocation",
    #     default={},
    # )

    textindexer.searchable("geographicCoverage")
    geographicCoverage = schema.List(
        title=_(
            u"Geographic coverage",
        ),
        value_type=schema.TextLine(
            title=u"Geographic Coverage",
            required=False,
            readonly=False,
        ),
        required=False,
        readonly=False,
    )

    textindexer.searchable("accessAndUseLimitationPublic_line")
    accessAndUseLimitationPublic_line = schema.TextLine(
        title=_(u"Limitation of public access"), required=False
    )

    textindexer.searchable("accessAndUseConstraints")
    accessAndUseConstraints = RichText(
        title=_(u"Conditions applying to access and use"), required=False
    )

    textindexer.searchable("qualitySpatialResolution_line")
    qualitySpatialResolution_line = schema.TextLine(
        title=_(u"Spatial Resolution"), required=False
    )

    textindexer.searchable("classificationTopicCategory")
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

    textindexer.searchable("temporalCoverage")
    temporalCoverage = schema.List(
        title=_(
            u"Temporal Extent",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"Year",
            required=False,
            readonly=False,
        ),
        required=False,
        readonly=False,
    )

    textindexer.searchable("temporalExtentStart")
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

    textindexer.searchable("temporalExtentEnd")
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

    textindexer.searchable("gemet")
    gemet = schema.List(
        title=_(
            u"GEMET",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"THEME",
            required=False,
            readonly=False,
        ),
        required=False,
    )

    textindexer.searchable("gemetInspireThemes")
    gemetInspireThemes = schema.List(
        title=_(
            u"GEMET INSPIRE Themes",
        ),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"INSPIRE THEME",
            required=False,
            readonly=False,
        ),
        required=False,
    )

    # HIERARCHY LEVEL
    #     Resource type: dataResourceType
    textindexer.searchable("dataResourceType")
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
    textindexer.searchable("responsiblePartyWithRole")
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
    textindexer.searchable("coordinateReferenceSystemList")
    coordinateReferenceSystemList = schema.List(
        title=_(u"Coordinate Reference System"),
        description=_(
            u"",
        ),
        value_type=schema.TextLine(
            title=u"Reference",
            required=False,
            readonly=False,
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
    textindexer.searchable("conformitySpecification")
    conformitySpecification = RichText(
        title=_(u"Specification"), required=False
    )

    textindexer.searchable("conformityPass")
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

    textindexer.searchable("qualityLineage")
    qualityLineage = RichText(title=_(u"Lineage"), required=False)

    # DISTRIBUTION INFO
    #     Distribution Info: distributionInfo
    #     Resource Locator: dataResourceLocator (DEPRECATED)
    #     Services: dataServices (DEPRECATED)

    textindexer.searchable("distributionInfo")
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

    textindexer.searchable("identifier")
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
    textindexer.searchable("update_frequency")
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

    textindexer.searchable("distribution_format_list")
    distribution_format_list = schema.List(
        title=_(
            u"Distribution format",
        ),
        value_type=schema.TextLine(
            title=u"Format",
            required=False,
            readonly=False,
        ),
        required=False,
        readonly=False,
    )

    textindexer.searchable("hierarchy_level")
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

    textindexer.searchable("metadata_language")
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

    textindexer.searchable("character_set")
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

    textindexer.searchable("date_stamp")
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

    textindexer.searchable("metadata_standard_name")
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

    textindexer.searchable("metadata_standard_version")
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

    textindexer.searchable("spatial_representation_type")
    spatial_representation_type = schema.List(
        title=_(
            u"Spatial representation type",
        ),
        value_type=schema.TextLine(
            title=u"Representation type",
            required=False,
            readonly=False,
        ),
        required=False,
        readonly=False,
    )

    textindexer.searchable("citation")
    citation = RichText(
        title=_(u"Dataset citation"),
        required=False,
    )

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

    textindexer.searchable("mapviewer_viewservice")
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

    textindexer.searchable("mapviewer_timeseriesservice")
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

    textindexer.searchable("mapviewer_handlinglevel")
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
            "download_by_area_extra_text",
            "download_full_dataset_text",
            "download_page_information",
            "download_other_ways_access_dataset",
            "dataset_download_information",
            "download_table_area_of_interest_title",
            "show_legend_on_prepackages",
            "show_pop_up_in_mapviewer",
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
            "Check if this dataset can be downloaded from the map viewer",
        ),
        description=_(
            "If selected, an explanation of 'Download by area (and time)'"
            "will be shown in the dataset download page."
        ),
        required=False,
        default=True,
        readonly=False,
    )

    textindexer.searchable("download_by_area_extra_text")
    download_by_area_extra_text = RichText(
        title=_(
            "Extra text for download by area/time",
        ),
        description=_(
            "This text will be shown in the download tab, just below the"
            " button. If empty, nothing will be shown"
        ),
        required=False,
        readonly=False,
    )

    # Make sure to import: from plone.app.textfield import RichText
    textindexer.searchable("download_full_dataset_text")
    download_full_dataset_text = RichText(
        title=_(
            'Text of the "Download full dataset"',
        ),
        description=_(
            "This text will be shown in the download tab. If empty, nothing"
            " will be shown"
        ),
        default=(
            "<p>If you want to download the full dataset, click <a"
            ' href="/en/how-to-guides/how-to-download-spatial-data/'
            'how-to-download-m2m">here</a>'
            " to learn more.</p>"
        ),
        required=False,
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

    download_table_area_of_interest_title = schema.TextLine(
        title=_(
            'Title of the "Area of interest" column in the prepackaged table',
        ),
        description=_(
            'This field allows modifying the title of "Area of interest" '
            "column in the prepackaged files table",
        ),
        default=u"Area of interest",
        required=False,
        readonly=False,
    )

    show_legend_on_prepackages = schema.Bool(
        title=_(
            u"Show associated grid picture for prepackages "
            u"nomenclature reference",
        ),
        description=_(
            "If selected this will show a button that will open a popup "
            "with the image showing the legends of the prepackages files"
        ),
        required=False,
        default=False,
        readonly=False,
    )

    show_pop_up_in_mapviewer = schema.Bool(
        title=_(
            "Mark as downloadable but with no service to visualise",
        ),
        required=False,
        default=False,
        readonly=False,
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

    textindexer.searchable("download_page_information")
    download_page_information = RichText(
        title=_("Download tab extra information"),
        description=_(
            "This text will be shown in the download tab. If empty, nothing"
            " will be shown"
        ),
        required=False,
    )

    textindexer.searchable("download_other_ways_access_dataset")
    download_other_ways_access_dataset = RichText(
        title=_("Text for other ways to access the dataset"),
        description=_(
            "This text will be shown in the download tab. If empty, nothing"
            " will be shown"
        ),
        required=False,
    )


@implementer(IDataSet)
class DataSet(Container):
    """DataSet content-type class"""
