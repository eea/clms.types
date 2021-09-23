# -*- coding: utf-8 -*-
"""Run upgrade"""

from . import logger


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info(
        "Running upgrade (Python): "
        "Reinstall profile to be sure to set the LRF schema"
    )
    logger.info("Done")
