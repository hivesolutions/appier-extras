#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2018 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import unittest

import appier
import appier_extras

class AccountTest(unittest.TestCase):

    def setUp(self):
        self.app = appier.App(
            parts = (appier_extras.admin.AdminPart,),
            session_c = appier.MemorySession
        )

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

    def test_confirm(self):
        account = appier_extras.admin.Account()
        account.username = "username"
        account.email = "username@domain.com"
        account.password = "password"
        account.password_confirm = "password"
        account.save()

        self.assertEqual(account.enabled, True)
        self.assertNotEqual(account.confirmation_token, None)

        account = account.get(username = "username", rules = False)
        account.enabled = False
        account.save()

        appier_extras.admin.Account.confirm(account.confirmation_token)
        account = account.reload(rules = False)

        self.assertEqual(account.enabled, True)
        self.assertEqual(account.confirmation_token, None)
        self.assertEqual(account.password, account.encrypt("password"))

    def test_reset(self):
        account = appier_extras.admin.Account()
        account.username = "username"
        account.email = "username@domain.com"
        account.password = "password"
        account.password_confirm = "password"
        account.save()

        self.assertEqual(account.enabled, True)
        self.assertEqual(account.reset_token, None)
        self.assertNotEqual(account.confirmation_token, None)

        account = account.get(username = "username", rules = False)
        account.enabled = False
        account.save()

        self.assertEqual(account.enabled, False)
        self.assertEqual(account.reset_token, None)
        self.assertNotEqual(account.confirmation_token, None)

        reset_token = account.recover_s()
        account = account.reload(rules = False)

        self.assertEqual(account.enabled, False)
        self.assertNotEqual(account.reset_token, None)
        self.assertEqual(account.reset_token, reset_token)
        self.assertNotEqual(account.confirmation_token, None)

        appier_extras.admin.Account.reset(
            reset_token,
            "passwordnew",
            "passwordnew"
        )
        account = account.reload(rules = False)

        self.assertEqual(account.enabled, True)
        self.assertEqual(account.reset_token, None)
        self.assertEqual(account.confirmation_token, None)
        self.assertEqual(account.password, account.encrypt("passwordnew"))

        account.enabled = False
        account.save()

        reset_token = account.recover_s()
        account = account.reload(rules = False)
        appier_extras.admin.Account.reset(
            reset_token,
            "passwordnew",
            "passwordnew",
            confirm = False
        )
        account = account.reload(rules = False)

        self.assertEqual(account.enabled, False)
        self.assertEqual(account.reset_token, None)
        self.assertEqual(account.confirmation_token, None)
        self.assertEqual(account.password, account.encrypt("passwordnew"))

    def test_role(self):
        account = appier_extras.admin.Account()
        account.username = "username"
        account.email = "username@domain.com"
        account.password = "password"
        account.password_confirm = "password"
        account.save()

        tokens = account.tokens()

        self.assertEqual(account.type, appier_extras.admin.Account.USER_TYPE)
        self.assertEqual(tokens, ["base", "user"])

        role = appier_extras.admin.Role()
        role.name = "admin"
        role.tokens = ["*"]
        role.save()

        self.assertEqual(role.name, "admin")
        self.assertEqual(role.tokens, ["*"])

        account = account.reload()
        account.add_role_s("admin")
        tokens = account.tokens()

        self.assertEqual(account.type, appier_extras.admin.Account.ROLE_TYPE)
        self.assertEqual(len(account.roles), 1)
        self.assertEqual(tokens, ["*"])

        account.add_role_s("admin")
        tokens = account.tokens()

        self.assertEqual(account.type, appier_extras.admin.Account.ROLE_TYPE)
        self.assertEqual(len(account.roles), 1)
        self.assertEqual(tokens, ["*"])

        role = appier_extras.admin.Role()
        role.name = "user"
        role.tokens = ["base", "user"]
        role.save()

        self.assertEqual(role.name, "user")
        self.assertEqual(role.tokens, ["base", "user"])

        account = account.reload()
        account.add_role_s("user")
        tokens = account.tokens()

        self.assertEqual(account.type, appier_extras.admin.Account.ROLE_TYPE)
        self.assertEqual(len(account.roles), 2)
        self.assertEqual(tokens, ["*"])

        account.remove_role_s("admin")
        tokens = account.tokens()

        self.assertEqual(account.type, appier_extras.admin.Account.ROLE_TYPE)
        self.assertEqual(len(account.roles), 1)
        self.assertEqual(tokens, ["base", "user"])

        role = appier_extras.admin.Role()
        role.name = "advanced"
        role.tokens = ["base", "advanced"]
        role.save()

        account.add_role_s("advanced")
        tokens = account.tokens()

        self.assertEqual(account.type, appier_extras.admin.Account.ROLE_TYPE)
        self.assertEqual(len(account.roles), 2)
        self.assertEqual(tokens, ["advanced", "base", "user"])
