#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
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
        role = appier_extras.admin.Role()
        role.name = "name"
        role.tokens = ["user"]
        role.save()

        self.assertNotEqual(role.id, None)
        self.assertEqual(role.name, "name")
        self.assertEqual(role.tokens, ["user"])
        self.assertEqual(role.tokens_a, set(["user"]))
        self.assertEqual(role.meta_a, {})

    def test_children(self):
        role = appier_extras.admin.Role()
        role.name = "name"
        role.tokens = ["user"]
        role.save()

        self.assertNotEqual(role.id, None)
        self.assertEqual(role.name, "name")
        self.assertEqual(role.tokens, ["user"])
        self.assertEqual(role.meta, {})
        self.assertEqual(role.tokens_a, set(["user"]))
        self.assertEqual(role.meta_a, {})

        child_role = appier_extras.admin.Role()
        child_role.name = "child_name"
        child_role.tokens = ["admin"]
        child_role.meta = {"parent" : "father"}
        child_role.save()

        self.assertNotEqual(child_role.id, None)
        self.assertEqual(child_role.name, "child_name")
        self.assertEqual(child_role.tokens, ["admin"])
        self.assertEqual(child_role.meta, {"parent" : "father"})
        self.assertEqual(child_role.tokens_a, set(["admin"]))
        self.assertEqual(child_role.meta_a, {"parent" : "father"})

        role.add_child_s(child_role.name)

        role = role.reload()

        self.assertNotEqual(role.id, None)
        self.assertEqual(role.name, "name")
        self.assertEqual(role.tokens, ["user"])
        self.assertEqual(role.meta, {})
        self.assertEqual(role.tokens_a, set(["user", "admin"]))
        self.assertEqual(role.meta_a, {"parent" : "father"})
