# -*- coding: utf-8 -*-
"""Run upgrade"""
from plone import api
from plone.app.textfield import RichTextValue

from . import logger


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info("Running upgrade (Python): v1020")
    migrate_summary_for_usecases()
    logger.info("Done")


def migrate_summary_for_usecases():
    """upgrade old UseCases to move their content to the new
    richtext field
    """
    brains = api.content.find(portal_type="UseCase")
    for brain in brains:
        obj = brain.getObject()
        obj.text = RichTextValue(
            f"<p>{obj.description}</p>", "text/html", "text/html"
        )
        logger.info("Migrated description to RichText: %s", obj.getId())
