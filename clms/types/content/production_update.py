# -*- coding: utf-8 -*-
"""
ProductionUpdate content-type definition
"""
from plone import api
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from clms.types import _


class IProductionUpdate(model.Schema):
    """Marker interface for ProductionUpdate"""


    status = schema.Choice(
        title=_(
            'Status',
        ),
        vocabulary="clms.types.ProductionUpdateStatusVocabulary",
        default=None,
        # defaultFactory=get_default_status,
        required=True,
        readonly=False,
    )


@implementer(IProductionUpdate)
class ProductionUpdate(Container):
    """UseCase content-type class"""

