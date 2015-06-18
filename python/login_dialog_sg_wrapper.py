# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
QT Login dialog for authenticating to a Shotgun server.

--------------------------------------------------------------------------------
NOTE! This module is part of the authentication library internals and should
not be called directly. Interfaces and implementation of this module may change
at any point.
--------------------------------------------------------------------------------
"""

from .login_dialog_sg import LoginDialog


class LoginDialogSgWrapper(LoginDialog):
    """
    Wraps the core's login dialog so that it is compatible with tk-framework-login.
    """
    def __init__(self, login, parent=None, **kwargs):
        """
        Translates the arguments from the tk-framework-login frame into the ones from the 
        """
        self._login = login
        hostname, login, password = login._get_saved_values()
        LoginDialog.__init__(
            self,
            is_session_renewal=False,
            hostname=hostname,
            login=login,
            fixed_host=False,
            http_proxy=login._http_proxy
        )

    def _authenticate(self, error_label, site, login, password, auth_code=None):
        """
        Authenticates the user using the passed in credentials.

        :param error_label: Label to display any error raised from the authentication.
        :param site: Site to connect to.
        :param login: Login to use for that site.
        :param password: Password to use with the login.
        :param auth_code: Optional two factor authentication code.

        :raises MissingTwoFactorAuthenticationFault: Raised if auth_code was None but was required
            by the server.
        """
        try:
            # set the wait cursor
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            QtGui.QApplication.processEvents()

            # try and authenticate
            self._new_session_token = session_cache.generate_session_token(
                site, login, password, self._http_proxy, auth_code
            )
        except AuthenticationError, e:
            # authentication did not succeed
            self._set_error_message(error_label, e[0])
        else:
            self.accept()
        finally:
            # restore the cursor
            QtGui.QApplication.restoreOverrideCursor()
            # dialog is done
            QtGui.QApplication.processEvents()
