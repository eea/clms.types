# -*- coding: utf-8 -*-

from . import logger

def upgrade(setup_tool=None):
    """"""
    logger.info(
        "Running upgrade (Python): Reinstall profile to be sure to set the LRF schema"
    )
    logger.info("Done")
