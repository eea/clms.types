""" Base test cases
"""
import plone.restapi
from plone.app.testing import (
    TEST_USER_ID,
    FunctionalTesting,
    PloneSandboxLayer,
    applyProfile,
    setRoles,
)
from plone.testing import z2
from Products.CMFPlone import setuphandlers

import clms.types


class EEAFixture(PloneSandboxLayer):
    """EEA Testing Policy"""

    def setUpZope(self, app, configurationContext):
        """Setup Zope"""

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=clms.types)
        z2.installProduct(app, "plone.restapi")
        z2.installProduct(app, "clms.types")

    def setUpPloneSite(self, portal):
        """Setup Plone"""
        applyProfile(portal, "clms.types:default")

        # Default workflow
        wftool = portal["portal_workflow"]
        wftool.setDefaultChain("simple_publication_workflow")

        # Login as manager
        setRoles(portal, TEST_USER_ID, ["Manager"])

        # Add default Plone content
        try:
            applyProfile(portal, "plone.app.contenttypes:plone-content")
        except KeyError:
            # BBB Plone 4
            setuphandlers.setupPortalContent(portal)

        # Create testing environment
        portal.invokeFactory("Folder", "sandbox", title="Sandbox")

    def tearDownZope(self, app):
        """Uninstall Zope"""
        z2.uninstallProduct(app, "clms.types")


EEAFIXTURE = EEAFixture()
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EEAFIXTURE,), name="EEAtypes:Functional"
)
