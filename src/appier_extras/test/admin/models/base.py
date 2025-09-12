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

    def test__csv_import(self):
        lines, headers = [], []
        appier_extras.admin.Base._csv_import(
            b"name,age\nAlice,30\nBob,25\n",
            lambda line, **kwargs: lines.append(tuple(line)),
            callback_header=lambda header: headers.append(tuple(header)),
            mime_type="text/csv",
        )
        self.assertEqual(headers, [(appier.legacy.u("name"), appier.legacy.u("age"))])
        self.assertEqual(
            lines,
            [
                (appier.legacy.u("Alice"), appier.legacy.u("30")),
                (appier.legacy.u("Bob"), appier.legacy.u("25")),
            ],
        )

        lines, headers = [], []
        appier_extras.admin.Base._csv_import(
            appier.legacy.u("name,age\n爱丽丝,30\nBob,25\n").encode("utf-8"),
            lambda line, **kwargs: lines.append(tuple(line)),
            callback_header=lambda header: headers.append(tuple(header)),
            mime_type="text/csv",
            encoding="utf-8",
        )
        self.assertEqual(headers, [(appier.legacy.u("name"), appier.legacy.u("age"))])
        self.assertEqual(
            lines,
            [
                (appier.legacy.u("爱丽丝"), appier.legacy.u("30")),
                (appier.legacy.u("Bob"), appier.legacy.u("25")),
            ],
        )

        lines, headers = [], []
        appier_extras.admin.Base._csv_import(
            appier.legacy.u("name,age\nJoão,30\nBob,25\n").encode("cp1252"),
            lambda line, **kwargs: lines.append(tuple(line)),
            callback_header=lambda header: headers.append(tuple(header)),
            mime_type="text/csv",
            encoding="cp1252",
        )
        self.assertEqual(headers, [(appier.legacy.u("name"), appier.legacy.u("age"))])
        self.assertEqual(
            lines,
            [
                (appier.legacy.u("João"), appier.legacy.u("30")),
                (appier.legacy.u("Bob"), appier.legacy.u("25")),
            ],
        )

        lines, headers = [], []
        appier_extras.admin.Base._csv_import(
            appier.legacy.u("name,age\nJoão,30\nBob,25\n").encode("cp1252"),
            lambda line, **kwargs: lines.append(tuple(line)),
            callback_header=lambda header: headers.append(tuple(header)),
            mime_type="text/csv",
            encoding="auto",
        )
        self.assertEqual(headers, [(appier.legacy.u("name"), appier.legacy.u("age"))])
        self.assertEqual(
            lines,
            [
                (appier.legacy.u("João"), appier.legacy.u("30")),
                (appier.legacy.u("Bob"), appier.legacy.u("25")),
            ],
        )

        lines, headers = [], []
        appier_extras.admin.Base._csv_import(
            appier.legacy.u("name;age\nJoão;30\nBob;25\n").encode("cp1252"),
            lambda line, **kwargs: lines.append(tuple(line)),
            callback_header=lambda header: headers.append(tuple(header)),
            mime_type="text/csv",
            header="auto",
            delimiter="auto",
            encoding="auto",
        )
        self.assertEqual(headers, [(appier.legacy.u("name"), appier.legacy.u("age"))])
        self.assertEqual(
            lines,
            [
                (appier.legacy.u("João"), appier.legacy.u("30")),
                (appier.legacy.u("Bob"), appier.legacy.u("25")),
            ],
        )

        lines, headers = [], []
        appier_extras.admin.Base._csv_import(
            appier.legacy.u("João;30\nBob;25\n").encode("cp1252"),
            lambda line, **kwargs: lines.append(tuple(line)),
            callback_header=lambda header: headers.append(tuple(header)),
            mime_type="text/csv",
            header="auto",
            delimiter="auto",
            encoding="auto",
        )
        self.assertEqual(headers, [()])
        self.assertEqual(
            lines,
            [
                (appier.legacy.u("João"), appier.legacy.u("30")),
                (appier.legacy.u("Bob"), appier.legacy.u("25")),
            ],
        )
