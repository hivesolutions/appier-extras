#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import unittest

import appier
import appier_extras


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = appier.App(
            parts=(appier_extras.admin.AdminPart,), session_c=appier.MemorySession
        )

    def tearDown(self):
        self.app.unload()
        adapter = appier.get_adapter()
        adapter.drop_db()

    def test_basic(self):
        base = appier_extras.admin.Base()
        base.save(verify=False)

        self.assertNotEqual(base.created, None)
        self.assertNotEqual(base.modified, None)

    def test_ensure_view(self):
        result = appier_extras.admin.Base.ensure_views(
            dict(name="Joseph", age=21), views=[dict(name="Joseph")]
        )
        self.assertEqual(result, None)

        self.assertRaises(
            appier.SecurityError,
            lambda: appier_extras.admin.Base.ensure_views(
                dict(name="Anthony", age=21), views=[dict(name="Joseph")]
            ),
        )

        self.assertRaises(
            appier.SecurityError,
            lambda: appier_extras.admin.Base.ensure_views(
                dict(age=21), views=[dict(name="Joseph")]
            ),
        )

        result = appier_extras.admin.Base.ensure_views(
            dict(age=21), views=[dict(name="Joseph")], ensure_set=False
        )
        self.assertEqual(result, None)

    def test_add_secret_s(self):
        settings = appier_extras.admin.Settings()
        settings.save()

        settings.add_secret_s("hello", "world", strategy="plain")
        settings = settings.reload(rules=False)
        self.assertNotEqual(settings.secrets, {})

        settings = settings.reload()
        result = settings.decode_secret("hello")
        self.assertEqual(result, "world")

        settings.add_secret_s("hello", "world", strategy="base64")
        settings = settings.reload(rules=False)
        self.assertNotEqual(settings.secrets, {})

        settings = settings.reload()
        result = settings.decode_secret("hello")
        self.assertEqual(result, "world")
