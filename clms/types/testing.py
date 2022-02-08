"""
testing basics
"""
# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    quickInstallProduct,
)
from plone.testing.zope import WSGI_SERVER_FIXTURE

import clms.types


class ClmstypesLayer(PloneSandboxLayer):
    """ base layer"""

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """ setup zope """
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        # pylint: disable=import-outside-toplevel
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=clms.types)

    def setUpPloneSite(self, portal):
        """ setup Plone site"""
        applyProfile(portal, "clms.types:default")


CLMS_TYPES_FIXTURE = ClmstypesLayer()


CLMS_TYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CLMS_TYPES_FIXTURE,),
    name="ClmstypesLayer:IntegrationTesting",
)


CLMS_TYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CLMS_TYPES_FIXTURE,),
    name="ClmstypesLayer:FunctionalTesting",
)


CLMS_TYPES_RESTAPI_TESTING = FunctionalTesting(
    bases=(CLMS_TYPES_FIXTURE, WSGI_SERVER_FIXTURE),
    name="ClmstypesLayer:RestApiTesting",
)


CLMS_TYPES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CLMS_TYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="ClmstypesLayer:AcceptanceTesting",
)
