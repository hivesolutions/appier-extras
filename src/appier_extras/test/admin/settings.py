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

class SettingsTest(unittest.TestCase):

    def setUp(self):
        self.app = appier.App(
            parts = (appier_extras.admin.AdminPart,),
            session_c = appier.MemorySession
        )

    def tearDown(self):
        self.app.unload()
        adapter = appier.get_adapter()
        adapter.drop_db()

    def test_extra(self):
        appier_extras.admin.Settings.set_extra_s("hello", "world")
        result = appier_extras.admin.Settings.get_extra("hello")

        self.assertEqual(result, "world")

        appier_extras.admin.Settings.del_extra_s("hello")
        result = appier_extras.admin.Settings.get_extra("hello")

        self.assertEqual(result, None)

        result = appier_extras.admin.Settings.get_extra("hello", "other")

        self.assertEqual(result, "other")

    def test_meta(self):
        settings = appier_extras.admin.Settings()
        settings.save()

        self.assertEqual(settings.meta, {})

        settings = settings.reload()
        settings.update_meta_s(dict(hello = "world"))

        self.assertEqual(settings.meta, dict(hello = "world"))

        settings = settings.reload()
        settings.update_meta_s(world = "hello")

        self.assertEqual(settings.meta, dict(hello = "world", world = "hello"))

        account = settings.reload()

        self.assertEqual(account.meta, dict(hello = "world", world = "hello"))
