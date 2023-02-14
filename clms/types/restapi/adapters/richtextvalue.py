""" ploen.restapi converter for RichTextValue objects"""
# -*- coding: utf-8 -*-
from plone.app.textfield.interfaces import IRichTextValue
from plone.restapi.interfaces import IJsonCompatible
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.interface import implementer


@adapter(IRichTextValue)
@implementer(IJsonCompatible)
def richtext_converter(value):
    """default richtext converter"""
    return json_compatible(value.output)
