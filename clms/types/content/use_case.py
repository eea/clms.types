# -*- coding: utf-8 -*-
"""
UseCase content-type definition
"""
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import Invalid, implementer, invariant
from collective import dexteritytextindexer
from clms.types import _
from clms.types.content.utils import valid_email


class IUseCase(model.Schema):
    """Marker interface for UseCase"""

    # default fieldset
    dexteritytextindexer.searchable("title")
    title = schema.TextLine(
        title=_(u"label_title", default=u"Title"),
        description=_("Provide a descriptive use case title."),
        required=True,
    )

    dexteritytextindexer.searchable("text")
    text = RichText(
        title=_(u"label_description", default=u"Summary"),
        description=_(
            "Provide a short and complete abstract of the use case:"
            " description, purpose, outcome, reference years, spatial coverage"
            " or location… Provide extra links to documents, videos and"
            " websites, if necessary."
        ),
        required=True,
        readonly=False,
    )

    dexteritytextindexer.searchable("submittingProducionYear")
    submittingProducionYear = schema.TextLine(
        title=_(u"Submitting production year of Use Case"),
        description=_(
            "Provide the year or a year interval in which the use case was"
            " produced, for example: 2019 or 2019-2022"
        ),
        required=True,
    )

    dexteritytextindexer.searchable("responsibleOrganization")
    responsibleOrganization = schema.TextLine(
        title=_(u"Responsible organization"),
        description=_(
            "Provide the name of the organisation that conducted the use case."
        ),
        required=True,
    )
    dexteritytextindexer.searchable("contactName")
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

    dexteritytextindexer.searchable("topics")
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
    dexteritytextindexer.searchable("outcome")
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

    # Removed: we are using collective.taxonomy based listing now.
    # geographicCoverage = schema.List(
    #     title=_(u"Spatial coverage"),
    #     description=_(
    #         "Choose at least one value from the drop down list with the"
    #         " location represented by the data."
    #     ),
    #     required=True,
    #     value_type=schema.Choice(
    #         title=_(
    #             u"Spatial coverage",
    #         ),
    #         vocabulary=u"clms.types.UseCaseSpatialCoverageVocabulary",
    #         required=True,
    #         readonly=False,
    #     ),
    #     readonly=False,
    # )

    external_url = schema.TextLine(
        title=_(
            u"External URL",
        ),
        description=_(
            u"Fill this field with the external URL (if any) of this use-case"
            u" so we can link our portal with the external.",
        ),
        default=u"",
        required=False,
        readonly=False,
    )

    products = schema.List(
        title=_(
            u"CLMS associated products (Copernicus Land Monitoring Service"
            u" products used)",
        ),
        description=_(
            u"Choose at least one value from the drop down list for the"
            u" Copernicus land monitoring service products used to produce the"
            u" use case.",
        ),
        value_type=schema.Choice(
            title=_(
                u"CLMS products used",
            ),
            vocabulary=u"clms.types.ProductsVocabulary",
            required=True,
            readonly=False,
        ),
        required=False,
        readonly=False,
    )

    datasets = schema.List(
        title=_(
            u"CLMS associated datasets",
        ),
        description=_(
            u"Choose at least one value from the drop down list for the"
            u" Copernicus land monitoring service datasets used to produce the"
            u" use case.",
        ),
        value_type=schema.Choice(
            title=_(
                u"CLMS datasets used",
            ),
            vocabulary=u"clms.types.DataSetsVocabulary",
            required=True,
            readonly=False,
        ),
        required=False,
        readonly=False,
    )

    @invariant
    def validate_products_and_datasets(data):
        """validate that at least one product or dataset is filled"""
        if not (data.datasets or data.products):
            raise Invalid(
                _("You need to provide at least one product or dataset")
            )

    @invariant
    def validate_email(data):
        """validate email"""
        if data.contactEmail and not valid_email(data.contactEmail):
            raise Invalid(_("The provided email address is not valid"))


@implementer(IUseCase)
class UseCase(Container):
    """UseCase content-type class"""
