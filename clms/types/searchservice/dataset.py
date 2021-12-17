# -*- coding: utf-8 -*-
"""
@metadata endpoint extension for DataSets
"""
from clms.types.content.data_set import IDataSet
from eea.api.coremetadata.api.services.metadata.adapters.dexterity import (
    BaseDexterityCoreMetadataAdapter,
)
from eea.api.coremetadata.api.services.metadata.adapters.interfaces import (
    ICoreMetadata,
)
from Products.CMFPlone.interfaces import ILanguage
from zope.component import adapter
from zope.interface import implementer


@adapter(IDataSet)
@implementer(ICoreMetadata)
class DatasetMetadataAdapter(BaseDexterityCoreMetadataAdapter):
    """Specific adapter for datasets"""

    def render_metadata(self):
        """render all metadata for datasets"""
        metadata = super().render_metadata()
        dataResourceAbstract = (
            self.context.dataResourceAbstract.output
            if self.context.dataResourceAbstract
            else ""
        )
        accessAndUseConstraints = (
            self.context.accessAndUseConstraints.output
            if self.context.accessAndUseConstraints
            else ""
        )
        responsibleParty = (
            self.context.responsibleParty.output
            if self.context.responsibleParty
            else ""
        )
        responsiblePartyRole = (
            self.context.responsiblePartyRole.output
            if self.context.responsiblePartyRole
            else ""
        )
        conformitySpecification = (
            self.context.conformitySpecification.output
            if self.context.conformitySpecification
            else ""
        )
        qualityLineage = (
            self.context.qualityLineage.output
            if self.context.qualityLineage
            else ""
        )
        dataServices = (
            self.context.dataServices.output
            if self.context.dataServices
            else ""
        )
        point_of_contact = (
            self.context.point_of_contact.output
            if self.context.point_of_contact
            else ""
        )

        metadata["SearchableText"] = " ".join(
            [
                dataResourceAbstract,
                accessAndUseConstraints,
                self.context.qualitySpatialResolution_line or "",
                responsibleParty,
                responsiblePartyRole,
                conformitySpecification,
                qualityLineage,
                dataServices,
                point_of_contact,
            ]
        )

        metadata["language"] = ILanguage(self.context).get_language()

        # Limitation of public access: accessAndUseLimitationPublic
        metadata[
            "limitation_of_public_access"
        ] = self.context.accessAndUseLimitationPublic_line

        # Type of resources
        metadata["resource_type"] = self.context.dataResourceType
        # GEMET Keyword
        metadata[
            "classification_topic_category"
        ] = self.context.classificationTopicCategory
        # INSPIRE THEMEs
        metadata["inspire_themes"] = self.context.inspireThemes
        # Keywords
        # They come from Plone field 'tags'

        # Years
        metadata["temporal_coverage"] = self.context.temporalCoverage

        # This is a RichText
        # # Formats
        metadata["distribution_format"] = self.context.distribution_format_list

        # Representation types
        # ???

        # Update Frequency
        metadata["update_frequency"] = self.context.update_frequency
        # Status
        metadata["conformity_pass"] = self.context.conformityPass
        # Scale
        # ???
        # Resolution
        # ???
        # Regions
        # ???
        metadata[
            "geographicBoundingBox"
        ] = self.context.geographicBoundingBox.get("items", [])

        return metadata
