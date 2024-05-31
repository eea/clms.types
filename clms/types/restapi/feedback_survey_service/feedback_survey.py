"""
REST API endpoint to get the feedback_survey configuration data
"""

from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from clms.types.interfaces import IClmsTypesLayer
from plone.memoize.view import memoize
from plone import api


@implementer(IExpandableElement)
@adapter(IDexterityContent, IClmsTypesLayer)
class FeedbackSurveyService(object):
    """Feedback survey configuration"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    # @memoize
    def get_survey_config(self):
        """return survey configuration"""
        is_active = api.portal.get_registry_record(
            "clms.types.feedback_survey.is_active", default=False
        )
        text = api.portal.get_registry_record(
            "clms.types.feedback_survey.text", default=""
        )
        link = api.portal.get_registry_record(
            "clms.types.feedback_survey.link", default=""
        )
        return {
            "is_active": is_active,
            "text": text,
            "link": link,
        }

    def __call__(self, expand=False):
        return {"feedback_survey": self.get_survey_config()}


class FeedbackSurveyServiceGet(Service):
    """Feedback survey config"""

    def reply(self):
        """Feedback survey"""
        return FeedbackSurveyService(self.context, self.request)()
