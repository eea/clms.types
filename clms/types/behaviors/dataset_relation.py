"""
dataset_relation behavior
"""
# -*- coding: utf-8 -*-

from clms.types import _
from plone import schema
from plone import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider


class IDataSetRelationMarker(Interface):
    """marker interface"""


@provider(IFormFieldProvider)
class IDataSetRelation(model.Schema):
    """interface definition"""

    datasets = schema.List(
        title=_(
            u"CLMS associated datasets",
        ),
        description=_(
            u"Multiple selection allowed",
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


@implementer(IDataSetRelation)
@adapter(IDataSetRelationMarker)
class DataSetRelation:
    """behavior implementation"""

    def __init__(self, context):
        self.context = context

    @property
    def datasets(self):
        """getter"""
        catalog = api.portal.get_tool('portal_catalog')

        if safe_hasattr(self.context, "datasets"):
            associated_datasets = self.context.datasets
            valid_datasets = []
            for dataset_id in associated_datasets:
                if len(catalog(UID=dataset_id)) > 0:
                    valid_datasets.append(dataset_id)
            # Return only existing datasets. Else when a dataset is deleted,
            # this item is not editable anymore.
            return valid_datasets
        return None

    @datasets.setter
    def datasets(self, value):
        """setter"""
        self.context.datasets = value
