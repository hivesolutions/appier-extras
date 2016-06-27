#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import unittest

import appier
import appier_extras

from . import mock

class AccountTest(unittest.TestCase):

    def setUp(self):
        self.app = appier.App()
        self.app._register_models_m(mock, "Mocks")

    def tearDown(self):
        self.app.unload()
        adapter = appier.get_adapter()
        adapter.drop_db()

    def test_basic(self):
        account = appier_extras.admin.Account()
        account.username = "username"
        account.email = "username@domain.com"
        account.password = "password"
        account.password_confirm = "password"
        account.save()

        self.assertNotEqual(account.id, None)
        self.assertNotEqual(account.password, "password")
        self.assertEqual(account.username, "username")
        self.assertEqual(account.email, "username@domain.com")
        self.assertEqual(len(account.password), 84)

        account = appier_extras.admin.Account.login("username", "password")

        self.assertNotEqual(account, None)
        self.assertEqual(account.username, "username")
        self.assertEqual(account.email, "username@domain.com")

        account.password = "passwordchanged"
        account.password_confirm = "password"

        self.assertRaises(appier.ValidationError, account.save)

        account.password_confirm = "passwordchanged"
        account.save()

        self.assertRaises(
            appier.OperationalError,
            lambda: appier_extras.admin.Account.login("username", "password")
        )

        account = appier_extras.admin.Account.login("username", "passwordchanged")

        self.assertNotEqual(account, None)
        self.assertEqual(account.username, "username")
        self.assertEqual(account.email, "username@domain.com")

        account.save()

        print(account.username)

        account = appier_extras.admin.Account.login("username", "passwordchanged")

        self.assertNotEqual(account, None)
        self.assertEqual(account.username, "username")
        self.assertEqual(account.email, "username@domain.com")

        account.password = "P"
        account.password_confirm = "P"

        self.assertRaises(appier.ValidationError, account.save)

    def test_insensitive(self):
        account = appier_extras.admin.Account()
        account.username = "Username"
        account.email = "USERNAME@domain.com"
        account.password = "password"
        account.password_confirm = "password"
        account.save()

        self.assertNotEqual(account.id, None)
        self.assertNotEqual(account.password, "password")
        self.assertEqual(account.username, "username")
        self.assertEqual(account.email, "username@domain.com")
        self.assertEqual(len(account.password), 84)

        account = appier_extras.admin.Account.login("USERNAME", "password")

        self.assertNotEqual(account, None)
        self.assertEqual(account.username, "username")
        self.assertEqual(account.email, "username@domain.com")

        self.assertRaises(
            appier.OperationalError,
            lambda: appier_extras.admin.Account.login("username", "PASSWORD")
        )
