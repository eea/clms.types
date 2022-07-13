# -*- coding: utf-8 -*-
from Products.CMFPlone.RegistrationTool import EmailAddressInvalid
from Products.CMFPlone.RegistrationTool import checkEmailAddress
from z3c.form import validator
from zope import schema

from clms.types import _


def valid_email(value):
    if value is not None:
        try:
            checkEmailAddress(value)
        except EmailAddressInvalid:
            return False
    return True


class WrongEmail(schema.ValidationError):
    __doc__ = _("""The entered email is not valid""")


class EmailValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        super(EmailValidator, self).validate(value)
        if valid_email(value):
            return True
        raise WrongEmail
