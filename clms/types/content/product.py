# -*- coding: utf-8 -*-
"""
Product content-type definition
"""
from clms.types import _
from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from plone.schema.jsonfield import JSONField
from plone.supermodel import model
from zope.interface import implementer
from zope import schema
from plone.restapi.behaviors import BLOCKS_SCHEMA, LAYOUT_SCHEMA, IBlocks
from .product_layout import product_layout_blocks, product_layout_items


class IProduct(model.Schema):
    """Marker interface and Dexterity Python Schema for Product"""

    showhow_in_mapviewer_link = schema.Bool(
        title=_(
            'Show "Show in mapviewer" link',
        ),
        description=_(
            'If selected a "Show in mapviewer" link will appear in the product page',
        ),
        required=False,
        readonly=False,
    )

    model.fieldset(
        "layout", label=_("Layout"), fields=["blocks", "blocks_layout"]
    )

    blocks = JSONField(
        title=_("Blocks"),
        description=_("The JSON representation of the object blocks."),
        schema=BLOCKS_SCHEMA,
        default=product_layout_blocks,
        required=False,
    )

    blocks_layout = JSONField(
        title=_("Blocks Layout"),
        description=_("The JSON representation of the object blocks layout."),
        schema=LAYOUT_SCHEMA,
        default={"items": product_layout_items},
        required=False,
    )

    model.fieldset(
        "order_technical_docs",
        label=_("Order technical documents"),
        fields=[
            "technical_documents_order",
        ],
    )

    textindexer.searchable("technical_documents_order")
    technical_documents_order = JSONField(
        title=_("Order technical documents"),
        description=_("Drag and drop the documents to order them"),
        required=False,
        widget="order_docs_widget",
        default={"items": []},
        missing_value={"items": []},
    )


@implementer(IProduct)
class Product(Container):
    """Product content type class"""
