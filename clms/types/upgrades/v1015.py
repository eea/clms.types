# -*- coding: utf-8 -*-
"""Run upgrade"""


from . import logger


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info(
        "Running upgrade (Python): New control panel and registry item"
    )
    logger.info("Done")
