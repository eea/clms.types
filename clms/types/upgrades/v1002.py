# -*- coding: utf-8 -*-
"""Run upgrade"""

from . import logger
from plone import api
from plone.restapi.types.utils import add_field
from plone.restapi.types.utils import add_fieldset
from zope.globalrequest import getRequest

import json

data = {
    "fieldsets": [],
    "properties": {},
}


LAYOUT_FIELDSET = {
    "id": "layout",
    "title": "Layout",
    "fields": ["blocks", "blocks_layout"],
}

BLOCK_FIELDS = [
    {
        "id": "blocks",
        "title": "Blocks",
        "type": "dict",
        "widget": "json",
        "factory": "JSONField",
    },
    {
        "id": "blocks_layout",
        "title": "Blocks Layout",
        "type": "dict",
        "widget": "json",
        "factory": "JSONField",
    },
]

from zope.component import queryMultiAdapter


def set_blocks_fieldset_and_fields_to_lrfs(context):

    context = api.portal.get()
    request = getRequest()

    dtypes = queryMultiAdapter((context, request), name="dexterity-types")
    ctype = dtypes.publishTraverse(request, "LRF")

    for field in BLOCK_FIELDS:
        try:
            add_field(ctype, request, field)
        except:
            logger.info("Field already exists in LRF: {}".format(field["id"]))

    add_fieldset(ctype, request, LAYOUT_FIELDSET)


def set_default_values_to_lrfs(context):
    brains = api.content.find(portal_type="LRF")
    for brain in brains:
        lrf = brain.getObject()
        if not lrf.blocks or not isinstance(lrf.blocks, dict):
            logger.info("Setting blocks attribute value for {}".format(lrf.id))
            lrf.blocks = {}

        if not lrf.blocks_layout or not isinstance(lrf.blocks_layout, dict):
            lrf.blocks_layout = {"items": []}
            logger.info(
                "Setting blocks_layout attribute value for {}".format(lrf.id)
            )


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info(
        "Running upgrade (Python): "
        "Reinstall profile to be sure to set the LRF schema"
    )
    set_blocks_fieldset_and_fields_to_lrfs(setup_tool)
    set_default_values_to_lrfs(setup_tool)
    logger.info("Done")
