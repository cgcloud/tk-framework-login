# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

################################################################################
# Shotgun Login Implementation

# package shotgun_api3 until toolkit upgrades to a version that
# allows for user based logins
from .shotgun_api3 import Shotgun
from .login import Login, LoginError
import logging

class ShotgunLogin(Login):

    SETTINGS_APPLICATION = "Shotgun Logging"
    SETTINGS_ORGANIZATION = "Shotgun Software"
    SETTINGS_APPLICATION_NAME = "com.shotgunsoftware.shotgunlogin"

    # Logging
    __logger = logging.getLogger("tk-framework-login.shotgunlogin")

    @classmethod
    def _site_connect(cls, site, login, password):
        """
        Authenticate the given values in Shotgun.

        Return a valid authenticated connection or raise an Exception
        """
        # package shotgun_api3 until toolkit upgrades to a version that
        # allows for user based logins

        # try to connect to Shotgun
        try:
            # connect and force an exchange so the authentication is validated
            connection = Shotgun(site, login=login, password=password)
            connection.find_one("HumanUser", [])
        except Exception, e:
            raise LoginError("Could not connect to server", str(e))

        try:
            result = connection.authenticate_human_user(login, password)
            if result is None:
                raise LoginError("Could not log in to server", "Login not valid.")
            return result
        except Exception, e:
            raise LoginError("Could not log in to server", str(e))
