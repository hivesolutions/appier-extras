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

    def tearDown(self):
        self.app.unload()
        adapter = appier.get_adapter()
        adapter.drop_db()

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
        self.assertIsNone(account.two_factor_method)

        account.generate_otp_s()
        account = account.reload()
        self.assertEqual(account.two_factor_method, "otp")

    def _create_account(self):
        account = appier_extras.admin.Account()
        account.username = "username"
        account.email = "username@domain.com"
        account.password = "password"
        account.password_confirm = "password"
        account.save()
        return account
