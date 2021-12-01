"""
dataset_relation behavior
"""
# -*- coding: utf-8 -*-

from clms.types import _
from plone import schema
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
        if safe_hasattr(self.context, "datasets"):
            return self.context.datasets
        return None

    @datasets.setter
    def datasets(self, value):
        """setter"""
        self.context.datasets = value
