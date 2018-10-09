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

class OAuthTokenTest(unittest.TestCase):

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

        oauth_client = appier_extras.admin.OAuthClient()
        oauth_client.name = "name"
        oauth_client.redirect_uri = "http://localhost/oauth"
        oauth_client.save()

        self.assertNotEqual(oauth_client.id, None)
        self.assertNotEqual(oauth_client.client_id, None)
        self.assertNotEqual(oauth_client.client_secret, None)
        self.assertEqual(oauth_client.name, "name")
        self.assertEqual(oauth_client.redirect_uri, "http://localhost/oauth")

        oauth_token = oauth_client.build_token_s("username", scope = ["admin", "user"])

        self.assertNotEqual(oauth_token.id, None)
        self.assertNotEqual(oauth_token.access_token, None)
        self.assertNotEqual(oauth_token.authorization_code, None)
        self.assertNotEqual(oauth_token.authorization_code_date, None)
        self.assertEqual(oauth_token.client.id, oauth_client.id)
        self.assertEqual(oauth_token.username, "username")
        self.assertEqual(oauth_token.scope, ["admin", "user"])
        self.assertEqual(oauth_token.tokens, ["user"])

        tokens = oauth_client.get_tokens()

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].username, "username")

        oauth_client.invalidate_s()

        tokens = oauth_client.get_tokens()

        self.assertEqual(len(tokens), 0)

    def test_reuse(self):
        account = appier_extras.admin.Account()
        account.username = "username"
        account.email = "username@domain.com"
        account.password = "password"
        account.password_confirm = "password"
        account.save()

        oauth_client = appier_extras.admin.OAuthClient()
        oauth_client.name = "name"
        oauth_client.redirect_uri = "http://localhost/oauth"
        oauth_client.save()

        self.assertNotEqual(oauth_client.id, None)
        self.assertNotEqual(oauth_client.client_id, None)
        self.assertNotEqual(oauth_client.client_secret, None)
        self.assertEqual(oauth_client.name, "name")
        self.assertEqual(oauth_client.redirect_uri, "http://localhost/oauth")

        oauth_token = oauth_client.build_token_s("username", scope = ["admin", "user"])

        self.assertNotEqual(oauth_token.id, None)
        self.assertNotEqual(oauth_token.access_token, None)
        self.assertNotEqual(oauth_token.authorization_code, None)
        self.assertNotEqual(oauth_token.authorization_code_date, None)
        self.assertEqual(oauth_token.client.id, oauth_client.id)
        self.assertEqual(oauth_token.username, "username")
        self.assertEqual(oauth_token.scope, ["admin", "user"])
        self.assertEqual(oauth_token.tokens, ["user"])

        result, tokens, oauth_token = appier_extras.admin.OAuthToken.reuse_s(
            "http://localhost/oauth",
            ["admin", "user"],
            oauth_client,
            account = account,
            owner = self.app
        )

        self.assertNotEqual(result, False)
        self.assertNotEqual(tokens, None)
        self.assertNotEqual(oauth_token, None)
        self.assertNotEqual(oauth_token.id, None)
        self.assertNotEqual(oauth_token.access_token, None)
        self.assertNotEqual(oauth_token.authorization_code, None)
        self.assertNotEqual(oauth_token.authorization_code_date, None)
        self.assertEqual(result, True)
        self.assertEqual(tokens, ["user"])
        self.assertEqual(oauth_token.client.id, oauth_client.id)
        self.assertEqual(oauth_token.username, "username")
        self.assertEqual(oauth_token.scope, ["admin", "user"])
        self.assertEqual(oauth_token.tokens, ["user"])
