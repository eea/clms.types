# -*- coding: utf-8 -*-
"""Run upgrade"""
from . import logger
from plone import api


def remove_unneeded_behaviors():
    """remove unneeded behaviors"""
    pt = api.portal.get_tool("portal_types")
    fti = pt.getTypeInfo("FAQ")
    behaviors_list = list(fti.behaviors)
    behaviors_list.remove("volto.blocks")
    fti.behaviors = tuple(behaviors_list)


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info("Running upgrade (Python): v1023")
    remove_unneeded_behaviors()
    logger.info("Done")
