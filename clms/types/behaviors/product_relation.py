"""
product_relation behavior
"""
# -*- coding: utf-8 -*-

from clms.types import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr, getToolByName
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider


class IProductRelationMarker(Interface):
    """marker interface"""


@provider(IFormFieldProvider)
class IProductRelation(model.Schema):
    """interface definition"""

    products = schema.List(
        title=_(
            u"CLMS associated products",
        ),
        description=_(
            u"Multiple selection allowed",
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


@implementer(IProductRelation)
@adapter(IProductRelationMarker)
class ProductRelation:
    """behavior implementation"""

    def __init__(self, context):
        self.context = context

    @property
    def products(self):
        """getter"""
        if safe_hasattr(self.context, "products"):
            catalog = getToolByName(self.context, 'portal_catalog')
            valid_products = [
                uid for uid in self.context.products if len(
                    catalog(UID=uid)) > 0]
            return valid_products
        return None

    @products.setter
    def products(self, value):
        """setter"""
        self.context.products = value
