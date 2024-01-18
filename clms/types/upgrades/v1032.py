# -*- coding: utf-8 -*-
"""Run upgrade"""
from plone import api

from . import logger


def set_related_datasets():
    """
    set all dataset relations correctly
    all related datasets should be related in both directions
    """
    brains = api.content.find(portal_type="DataSet")
    for brain in brains:
        current_dataset = brain.getObject()
        if current_dataset.datasets is None:
            current_dataset.datasets = []
        for dataset_uid in current_dataset.datasets:
            dataset = api.content.get(UID=dataset_uid)
            if dataset.datasets is None:
                dataset.datasets = []
            if current_dataset.UID() not in dataset.datasets:
                dataset.datasets.append(current_dataset.UID())
                logger.info(
                    "Added related dataset. Current object %s, "
                    "related dataset %s",
                    current_dataset.UID(),
                    dataset_uid,
                )
                dataset.reindexObject()


def upgrade(setup_tool=None):
    """Run upgrade"""
    logger.info("Running upgrade (Python): v1032")
    set_related_datasets()
    logger.info("Done")
