""" some utils"""
# -*- coding: utf-8 -*-
from Products.CMFPlone.RegistrationTool import (
    EmailAddressInvalid,
    checkEmailAddress,
)


def valid_email(value):
    """return whether the value is a valid email or not"""
    if value is not None:
        try:
            checkEmailAddress(value)
        except EmailAddressInvalid:
            return False
    return True
