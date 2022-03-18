# -*- coding: utf-8 -*-
"""Run upgrade"""

from plone import api

from . import logger

PROFILE_ID = "clms.addon:default"


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info("Running upgrade (Python): Add new content type")
    setup = api.portal.get_tool("portal_setup")
    setup.runImportStepFromProfile(PROFILE_ID, "typeinfo")
    setup.runImportStepFromProfile(PROFILE_ID, "rolemap")
    logger.info("Done")
