# -*- coding: utf-8 -*-
"""
WorkOpportunity content-type definition
"""
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IDataSetAccordion(model.Schema):
    """Marker interface and Dexterity Python Schema for DatasetAccordion"""


@implementer(IDataSetAccordion)
class DataSetAccordion(Container):
    """DatasetAccordion content type class"""
