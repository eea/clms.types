# -*- coding: utf-8 -*-
from plone.app.upgrade.utils import loadMigrationProfile

PROFILE_ID = "profile-clms.types:default"


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        "profile-clms.types:default",
    )
