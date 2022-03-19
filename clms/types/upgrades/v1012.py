# -*- coding: utf-8 -*-
"""Run upgrade"""

from plone import api

from . import logger

PROFILE_ID = "clms.addon:default"


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info("Running upgrade (Python): New indexes and catalog fields")
    setup = api.portal.get_tool("portal_setup")
    setup.runImportStepFromProfile(PROFILE_ID, "catalog")
    setup.runImportStepFromProfile(PROFILE_ID, "plone.app.registry")
    logger.info("Done")
