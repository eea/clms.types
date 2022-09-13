# -*- coding: utf-8 -*-
"""Run upgrade"""
from plone import api

from . import logger


def migrate_to_new_spatial_coverage():
    """ migrate all spatialcoverage fields to the new one
        which is based on collective.taxonomy
    """
    brains = api.content.find(portal_type='UseCase')
    for brain in brains:
        item = brain.getObject()
        item.taxonomy_use_case_spatial_coverage = item.geographicCoverage
        logger.info('Migrated item: %s', brain.getPath())
    logger.info('Migrated all usecases to use taxonomy')


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info("Running upgrade (Python): v1017")
    migrate_to_new_spatial_coverage()

    logger.info("Done")
