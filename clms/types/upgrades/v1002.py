# -*- coding: utf-8 -*-

from . import logger


from .base import reload_gs_profile

# from plone import api


def upgrade(setup_tool=None):
    """"""
    logger.info(
        "Running upgrade (Python): Reinstall profile to be sure to set the LRF schema"
    )
    reload_gs_profile(setup_tool)
    logger.info("Done")
