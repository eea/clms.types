# -*- coding: utf-8 -*-
"""
UseCase content-type definition
"""
from typing import Tuple

from plone import api
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import Interface, implementer, provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from clms.types import _


@provider(IVocabularyFactory)
def products_vocabulary_factory():
    products = api.content.find(portal_type='Product')
    productsList = [(p.getObject().id, p.getObject().title) for p in products]
    terms = [SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
             for pair in productsList]
    products_vocabulary = SimpleVocabulary(terms)
    return products_vocabulary


products_vocabulary = products_vocabulary_factory()


class IUseCaseMarker(Interface):
    pass


class IUseCase(model.Schema):
    """ Marker interface for UseCase
    """

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('use_case.xml')

    products = schema.List(
        title=_(
            u'CLMS products used',
        ),
        description=_(
            u'Multiple selection allowed',
        ),
        value_type=schema.Choice(
            title=_(
                u'CLMS products used',
            ),
            vocabulary=products_vocabulary,
            required=True,
            readonly=False,
        ),
        required=True,
        readonly=False,
    )

    responsibleOrganization = schema.TextLine(
        title=_(u"Responsible organization"),
        required=True,
    )

    contactName = schema.TextLine(
        title=_(u"Contact person name"),
        required=False,
    )

    contactEmail = schema.TextLine(
        title=_(u"Contact person email"),
        required=False,
    )

    topics = schema.List(
        title=_(
            u'Use case topics',
        ),
        description=_(
            u'Multiple selection allowed',
        ),
        value_type=schema.Choice(
            title=_(
                u'Use case topics',
            ),
            vocabulary=u'clms.types.TopicsVocabulary',
            required=True,
            readonly=False,
        ),
        required=True,
        readonly=False,
    )

    outcome = schema.TextLine(
        title=_(u"User case outcome"),
        required=True,
    )

    links = schema.List(
        title=_(
            u'Links to use case',
        ),
        description=_(
            u'',
        ),
        value_type=schema.URI(
            title=u'',
        ),
        required=True,
        readonly=False,
    )

    image = namedfile.NamedBlobImage(
        title=_(u"image"),
        required=False,
    )


@implementer(IUseCase)
@adapter(IUseCaseMarker)
class UseCase(Container):
    """ UseCase content-type class """

    def __init__(self, context):
        self.context = context

    @property
    def products(self):
        if hasattr(self.context, "products"):
            return self.context.products
        return None

    @products.setter
    def products(self, value):
        self.context.products = value

    @property
    def responsibleOrganization(self):
        if hasattr(self.context, "responsibleOrganization"):
            return self.context.responsibleOrganization
        return None

    @responsibleOrganization.setter
    def responsibleOrganization(self, value):
        self.context.responsibleOrganization = value

    @property
    def contactName(self):
        if hasattr(self.context, "contactName"):
            return self.context.contactName
        return None

    @contactName.setter
    def contactName(self, value):
        self.context.contactName = value

    @property
    def contactEmail(self):
        if hasattr(self.context, "contactEmail"):
            return self.context.contactEmail
        return None

    @contactEmail.setter
    def contactEmail(self, value):
        self.context.contactEmail = value

    @property
    def topics(self):
        if hasattr(self.context, "topics"):
            return self.context.topics
        return None

    @topics.setter
    def topics(self, value):
        self.context.topics = value

    @property
    def outcome(self):
        if hasattr(self.context, "outcome"):
            return self.context.outcome
        return None

    @outcome.setter
    def outcome(self, value):
        self.context.outcome = value

    @property
    def links(self):
        if hasattr(self.context, "links"):
            return self.context.links
        return None

    @links.setter
    def links(self, value):
        self.context.links = value

    @property
    def image(self):
        if hasattr(self.context, "image"):
            return self.context.image
        return None

    @image.setter
    def image(self, value):
        self.context.image = value
