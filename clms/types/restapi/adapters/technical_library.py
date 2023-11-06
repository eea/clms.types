"""
Custom adapter to decide where to link when selecting
a TechnicalLibrary item as a link target.

It should behave as a normal link to a File except when
the 'ondemand' attribute is set to True.

In such case, the link should point to the content itself
"""
# -*- coding: utf-8 -*-
from clms.types.content.technical_library import ITechnicalLibrary
from plone.namedfile.interfaces import INamedFileField
from plone.restapi.serializer.dxfields import PrimaryFileFieldTarget
from zope.component import adapter
from zope.interface import Interface


@adapter(INamedFileField, ITechnicalLibrary, Interface)
class TechnicalLibraryPrimaryFileFieldTarget(PrimaryFileFieldTarget):
    """ Custom adapter for TechnicalLibrary items, to decide when to show
        the primary field link
    """
    def use_primary_field_target(self):
        """ alter condition"""
        super_value = super().use_primary_field_target()
        if super_value:
            if hasattr(self.context, 'ondemand') and self.context.ondemand:
                return False
            return True
        return False
