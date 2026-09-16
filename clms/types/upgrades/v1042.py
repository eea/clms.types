# -*- coding: utf-8 -*-
"""Run upgrade"""

from plone import api

from . import logger


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info("Running upgrade (Python): v1042")

    for brain in api.content.find(portal_type="DataSet"):
        obj = brain.getObject()
        obj.characteristics_data_type = "continuous"
        obj.reindexObject()

    logger.info("Done")
