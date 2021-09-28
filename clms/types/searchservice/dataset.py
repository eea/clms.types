# -*- coding: utf-8 -*-
from eea.api.coremetadata.api.services.metadata.adapters.dexterity import (
    BaseDexterityCoreMetadataAdapter,
)
from eea.api.coremetadata.api.services.metadata.adapters.interfaces import (
    ICoreMetadata,
)
from clms.types.content.data_set import IDataSet

from zope.component import adapter
from zope.interface import implementer


@adapter(IDataSet)
@implementer(ICoreMetadata)
class DatasetMetadataAdapter(BaseDexterityCoreMetadataAdapter):
    def render_metadata(self):
        metadata = super().render_metadata()

        metadata["SearchableText"] = " ".join(
            [
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

        metadata["topic"] = self.context.classificationTopicCategory

        return metadata
