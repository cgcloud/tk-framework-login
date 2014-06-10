# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from urlparse import urlparse

# package shotgun_api3 until toolkit upgrades to a version that
# allows for user based logins
from .shotgun_api3 import Shotgun

from .login import Login
from .login import LoginError

from .qt_abstraction import QtCore


################################################################################
# Shotgun Login Implementation
class ShotgunLogin(Login):
    def get_login(self, site=None, dialog_message=None, force_dialog=False):
        """ Returns the HumanUser for the current login.  Acts like login otherwise. """
        results = self.login(site, dialog_message, force_dialog)
        return results["login"]

    def get_connection(self, site=None, dialog_message=None, force_dialog=False):
        """ Returns the connection for the current login.  Acts like login otherwise. """
        results = self.login(site, dialog_message, force_dialog)
        return results["connection"]

    def _get_keyring_values(self, site, login):
        """
        Override the base class implementation to always use a specific keyring
        but encode the site in the login.
        """
        keyring = "com.shotgunsoftware.tk-framework-shotgunlogin"
        parse = urlparse(site)
        login = "%s@%s" % (login, parse.netloc)
        return (keyring, login)

    def _get_settings(self, group=None):
        """
        Override the base class implementation to always use a specific
        organization and application for the QSettings.
        """
        settings = QtCore.QSettings("Shotgun Software", "Shotgun Login Framework")

        if group is not None:
            settings.beginGroup(group)
        return settings

    def _site_connect(self, site, login, password):
        """
        Authenticate the given values in Shotgun.

        :param site: The site to login to
        :param login: The login to use
        :param password: The password to use

        :returns: A tuple of (connection, login) if successful, where connection
            is a valid Shotgun connection to site, logged in as login, and login
            is a HumanUser dictionary of the Entity on the Shotgun site representing
            this login.

        :raises: LoginError on failure.
        """
        # try to connect to Shotgun
        try:
            # connect and force an exchange so the authentication is validated
            connection = Shotgun(site, login=login, password=password)
            connection.find_one("HumanUser", [])
        except Exception, e:
            raise LoginError("Could not connect to server", str(e))

        try:
            user = connection.authenticate_human_user(login, password)
            if user is None:
                raise LoginError("Could not log in to server", "Login not valid.")
            return {"connection": connection, "login": user}
        except Exception, e:
            raise LoginError("Could not log in to server", str(e))
