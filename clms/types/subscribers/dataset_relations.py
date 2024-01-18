"""
An event subsriber to set both-direction relations in datasets
"""
# -*- coding: utf-8 -*-
from logging import getLogger

from plone import api

log = getLogger(__name__)


def dataset_edit_handler(object, event):
    """ handler executed when a dataset is edited"""
    for description in event.descriptions:
        if 'IDataSet.datasets' in description.attributes:
            log.info('Changed')
            # only execute if related datasets field
            # have been modified

            # First reset all existing relations
            dataset_brains = api.content.find(
                associated_datasets=object.UID(),
                portal_type='DataSet'
            )
            for dataset_brain in dataset_brains:
                dataset_object = dataset_brain.getObject()
                try:
                    dataset_object.datasets.remove(object.UID())
                    log.info(
                        'Dataset relation removed in %s',
                        dataset_object.absolute_url()
                    )
                except ValueError:
                    # The item is not there
                    log.info('Dataset not related')
                dataset_object.reindexObject()

        # Finally do the setting again
        for dataset_uid in object.datasets:
            dataset = api.content.get(UID=dataset_uid)
            if dataset.datasets is None:
                dataset.datasets = []
            if object.UID() not in dataset.datasets:
                dataset.datasets.append(object.UID())
                log.info(
                    'Added related dataset. Current object %s, '
                    'related dataset %s',
                    object.absolute_url(),
                    dataset.absolute_url()
                )
                dataset.reindexObject()





