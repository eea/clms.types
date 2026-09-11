# -*- coding: utf-8 -*-
"""Run upgrade"""

from plone import api

from . import logger


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info("Running upgrade (Python): v1042")

    for brain in api.content.find(portal_type="DataSet"):
        obj = brain.getObject()
        if not getattr(obj, "characteristics_data_type", None):
            obj.characteristics_data_type = "discrete"
            obj.reindexObject()

    logger.info("Done")
