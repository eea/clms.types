# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.browserlayer import utils

from clms.types.interfaces import IClmsTypesLayer
from clms.types.testing import CLMS_TYPES_INTEGRATION_TESTING

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that clms.types is properly installed."""

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if clms.types is installed."""
        self.assertTrue(self.installer.is_product_installed("clms.types"))

    def test_browserlayer(self):
        """Test that IClmsTypesLayer is registered."""
        self.assertIn(IClmsTypesLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    """ test that clms.types is properly uninstalled """

    layer = CLMS_TYPES_INTEGRATION_TESTING

    def setUp(self):
        """ setup"""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("clms.types")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if clms.types is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("clms.types"))

    def test_browserlayer_removed(self):
        """Test that IClmsTypesLayer is removed."""
        self.assertNotIn(IClmsTypesLayer, utils.registered_layers())
