#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Hive Appier Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Appier Framework.
#
# Hive Appier Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Appier Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Appier Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import json
import appier
import unittest

import appier_extras


class AccountTwoFactorTest(unittest.TestCase):
    def setUp(self):
        if not appier.legacy.PYTHON_3:
            self.skipTest("Python 3 is required")
        self.app = appier.App(
            parts=(appier_extras.admin.AdminPart,), session_c=appier.MemorySession
        )
        self._patch_fido2_server()

    def tearDown(self):
        self.app.unload()
        adapter = appier.get_adapter()
        adapter.drop_db()
        self._rollback_fido2_server()

    def test_otp_generate_and_login(self):
        account = self._create_account()
        account.generate_otp_s()
        account = account.reload(rules=False)

        self.assertEqual(account.otp_enabled, True)
        self.assertNotEqual(account.otp_secret, None)

        otp_token = account.generate_otp_token()
        account_logged = appier_extras.admin.Account.login_otp("username", otp_token)
        self.assertEqual(account_logged.id, account.id)

    def test_otp_invalid_token(self):
        account = self._create_account()
        account.generate_otp_s()

        with self.assertRaises(appier.OperationalError):
            appier_extras.admin.Account.login_otp("username", "000000")

    def test_otp_two_factor_method_property(self):
        account = self._create_account()
        self.assertEqual(account.two_factor_method, None)

        account.generate_otp_s()
        account = account.reload()
        self.assertEqual(account.two_factor_method, "otp")

    def test_fido2_register_and_login(self):
        account = self._create_account()
        account.add_credential_s("credential-id", "credential-data")
        account = account.reload(rules=False)

        self.assertEqual(account.fido2_enabled, True)
        self.assertEqual(
            appier_extras.admin.Account._fido2_server._authenticated, False
        )

        state_json, _ = appier_extras.admin.Account.login_begin_fido2("username")
        self.assertEqual(json.loads(state_json), "fido2-state")
        self.assertEqual(
            appier_extras.admin.Account._fido2_server._authenticated, False
        )

        account_logged = appier_extras.admin.Account.login_fido2(
            "username", state_json, dict(id="credential-id")
        )
        self.assertEqual(account_logged.id, account.id)
        self.assertEqual(appier_extras.admin.Account._fido2_server._authenticated, True)

    def test_fido2_invalid_state(self):
        account = self._create_account()
        account.add_credential_s("credential-id", "credential-data")

        with self.assertRaises(appier.OperationalError):
            appier_extras.admin.Account.login_fido2("username", None, {})

    def test_fido2_two_factor_method_property(self):
        account = self._create_account()
        self.assertEqual(account.two_factor_method, None)

        account.add_credential_s("credential-id", "credential-data")
        account = account.reload()
        self.assertEqual(account.two_factor_method, "fido2")

    def _create_account(self):
        account = appier_extras.admin.Account()
        account.username = "username"
        account.email = "username@domain.com"
        account.password = "password"
        account.password_confirm = "password"
        account.save()
        return account

    def _patch_fido2_server(self):
        # creates a stub for the FIDO2 server
        # allowing test operations to work as expected
        class _StubFido2Server(object):
            _authenticated = False

            def authenticate_begin(self, credentials):
                return {}, "fido2-state"

            def authenticate_complete(self, state, credentials, response_data):
                self._authenticated = True
                return None

        # sets the stub for the FIDO2 server allowing test operations
        # to work as expected
        appier_extras.admin.Account._fido2_server = _StubFido2Server()

        # patches the `credentials_data_n` property to avoid complex attestation parsing
        # allowing test operations to work as expected
        self._orig_credentials_data_n = appier_extras.admin.Account.credentials_data_n
        appier_extras.admin.Account.credentials_data_n = property(lambda self: [])

    def _rollback_fido2_server(self):
        # restores the original `_fido2_server` property
        # allowing future operations to work as expected
        if hasattr(appier_extras.admin.Account, "_fido2_server"):
            delattr(appier_extras.admin.Account, "_fido2_server")

        # restores the original `credentials_data_n` property
        # allowing future operations to work as expected
        if hasattr(self, "_orig_credentials_data_n"):
            appier_extras.admin.Account.credentials_data_n = (
                self._orig_credentials_data_n
            )
