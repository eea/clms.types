# -*- coding: utf-8 -*-
"""Searchable text indexers"""
from clms.types.content.data_set import IDataSet
from clms.types.content.technical_library import ITechnicalLibrary
from plone.app.dexterity.textindexer import interfaces
from plone.app.dexterity.textindexer.converters import \
    NamedfileFieldConverter as Base
from plone.namedfile.interfaces import INamedFileField
from Products.CMFPlone.utils import safe_text
from z3c.form.interfaces import IWidget
from zope.component import adapter
from zope.interface import implementer

TITLE_IN_SEARCHABLE_TEXT_WEIGHT = 100


@implementer(interfaces.IDexterityTextIndexFieldConverter)
@adapter(ITechnicalLibrary, INamedFileField, IWidget)
class NamedfileFieldConverter(Base):
    """Custom namedfilefielconverter to index the file name"""

    def convert(self):
        """convert method, call the super method and append the filename"""

        data = super().convert()
        if self.widget.filename:
            data += " "
            data += safe_text(self.widget.filename)

        return data


@implementer(interfaces.IDynamicTextIndexExtender)
@adapter(IDataSet)
class DataSetSearchableTextDynamicTextIndexExtender:
    """an extender for DataSet searchable text to extend
    the searchable text with additional text.
    In our case with additional values of the title
    to make the title more important
    """

    def __init__(self, context):
        """initialization"""
        self.context = context

    def __call__(self):
        """run the adapter"""
        return " ".join(
            [self.context.Title()] * TITLE_IN_SEARCHABLE_TEXT_WEIGHT
        )


@implementer(interfaces.IDynamicTextIndexExtender)
@adapter(ITechnicalLibrary)
class TechnicalLibrarySearchableTextDynamicTextIndexExtender:
    """an extender for TechnicalLibraru searchable text to extend
    the searchable text with additional text.
    In our case with additional values of the title
    to make the title more important
    """

    def __init__(self, context):
        """initialization"""
        self.context = context

    def __call__(self):
        """run the adapter"""
        return " ".join(
            [self.context.Title()] * TITLE_IN_SEARCHABLE_TEXT_WEIGHT
        )
