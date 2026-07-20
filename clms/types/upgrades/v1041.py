# -*- coding: utf-8 -*-
"""Run upgrade"""

from plone import api

from . import logger


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info("Running upgrade (Python): v1041")

    setup = api.portal.get_tool("portal_setup")
    setup.runImportStepFromProfile("clms.types.upgrades:1041", "catalog")

    for brain in api.content.find(portal_type="TechnicalLibrary"):
        obj = brain.getObject()
        obj.reindexObject()

    logger.info("Done")
