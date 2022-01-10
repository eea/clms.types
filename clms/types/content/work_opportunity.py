# -*- coding: utf-8 -*-
"""
WorkOpportunity content-type definition
"""
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer
from zope import schema

from clms.types import _


class IWorkOpportunity(model.Schema):
    """Marker interface and Dexterity Python Schema for WorkOpportunity"""

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('work_oportunity.xml')

    procurement_no = schema.TextLine(
        title=_(
            u"Reference No",
        ),
        description=_(
            u"",
        ),
        default=u"",
        required=True,
        readonly=False,
    )

    url = schema.URI(title=_(u"Link"), required=False)

    submission_deadline = schema.Datetime(
        title=_(
            u"Submission deadline",
        ),
        description=_(
            u"",
        ),
        # defaultFactory=get_default_name,
        required=False,
        readonly=False,
    )

    # is_open = schema.Bool(
    #     title=_(
    #         u"Are the tenders open?",
    #     ),
    #     description=_(
    #         u"Mark this field if this work opportunity tenders " u"are open."
    #     ),
    #     required=False,
    #     default=False,
    #     readonly=False,
    # )
    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    # image = namedfile.NamedBlobImage(
    #     title=_(u'image'),
    #     required=False,
    # )

    # text = RichText(title=_(u"Text"), required=False)

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(IWorkOpportunity)
class WorkOpportunity(Container):
    """WorkOpportunity content type class"""
