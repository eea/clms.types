"""
product_updates_publication behavior
"""
# -*- coding: utf-8 -*-

from clms.types import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider
from plone.autoform import directives
from plone.app.z3cform.widget import DatetimeFieldWidget
from zope.interface import invariant
from plone.app.dexterity.behaviors.metadata import (
    EffectiveAfterExpires,
    DCFieldProperty,
    MetadataBase,
)
from z3c.form.interfaces import IAddForm, IEditForm


class IProductUpdatesPublicationMarker(Interface):
    """marker interface"""


@provider(IFormFieldProvider)
class IProductUpdatesPublication(model.Schema):
    # dates fieldset
    model.fieldset(
        "dates",
        label=_("label_schema_dates", default="Dates"),
        fields=["effective", "expires"],
    )

    effective = schema.Datetime(
        title=_("label_effective_date", "Publishing Date"),
        description=_(
            "help_effective_date",
            default="If this date is in the future, the content will "
            "not show up in listings and searches until this date.",
        ),
        required=True,
    )
    directives.widget("effective", DatetimeFieldWidget)

    expires = schema.Datetime(
        title=_("label_expiration_date", "Expiration Date"),
        description=_(
            "help_expiration_date",
            default="When this date is reached, the content will no "
            "longer be visible in listings and searches.",
        ),
        required=False,
    )
    directives.widget("expires", DatetimeFieldWidget)

    @invariant
    def validate_start_end(data):
        if data.effective and data.expires and data.effective > data.expires:
            raise EffectiveAfterExpires(
                _(
                    "error_expiration_must_be_after_effective_date",
                    default="Expiration date must be after publishing date.",
                )
            )

    directives.omitted("effective", "expires")
    directives.no_omit(IEditForm, "effective", "expires")
    directives.no_omit(IAddForm, "effective", "expires")


@implementer(IProductUpdatesPublication)
@adapter(IProductUpdatesPublicationMarker)
class ProductUpdatesPublication(MetadataBase):
    effective = DCFieldProperty(
        IProductUpdatesPublication["effective"], get_name="effective_date"
    )
    expires = DCFieldProperty(
        IProductUpdatesPublication["expires"], get_name="expiration_date"
    )
