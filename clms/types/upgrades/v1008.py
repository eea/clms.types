# -*- coding: utf-8 -*-
"""Run upgrade"""

from plone import api

from . import logger


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info("Running upgrade (Python): Add new content type")
    setup = api.portal.get_tool("portal_setup")
    setup.runImportStepFromProfile("clms.types:default", "catalog")
    setup.runImportStepFromProfile("clms.types:default", "plone.app.registry")
    logger.info("Done")
