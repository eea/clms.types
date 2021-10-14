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
    """ Specific adapter for datasets """

    def render_metadata(self):
        """ render all metadata for datasets """
        metadata = super().render_metadata()

        metadata["SearchableText"] = " ".join(
            [
                # pylint: ignore=W503
                self.context.dataResourceAbstract
                and self.context.dataResourceAbstract.output
                or "",
                self.context.accessAndUseLimitationPublic
                and self.context.accessAndUseLimitationPublic.output
                or "",
                self.context.accessAndUseConstraints
                and self.context.accessAndUseConstraints.output
                or "",
                self.context.qualitySpatialResolution
                and self.context.qualitySpatialResolution.output
                or "",
                self.context.responsibleParty
                and self.context.responsibleParty.output
                or "",
                self.context.responsiblePartyRole
                and self.context.responsiblePartyRole.output
                or "",
                self.context.conformitySpecification
                and self.context.conformitySpecification.output
                or "",
                self.context.qualityLineage
                and self.context.qualityLineage.output
                or "",
                self.context.dataServices
                and self.context.dataServices.output
                or "",
                self.context.point_of_contact
                and self.context.point_of_contact.output
                or "",
                self.context.distribution_format
                and self.context.distribution_format.output
                or "",
            ]
        )

        metadata["language"] = ILanguage(self.context).get_language()

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
        # Formats
        metadata["distribution_format"] = self.context.distribution_format

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
