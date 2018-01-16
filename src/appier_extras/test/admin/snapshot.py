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

from . import mock

class SnapshotTest(unittest.TestCase):

    def setUp(self):
        self.app = appier.App(
            parts = (appier_extras.admin.AdminPart,),
            session_c = appier.MemorySession
        )
        self.app._register_models_m(mock, "Mocks")

    def tearDown(self):
        self.app.unload()
        adapter = appier.get_adapter()
        adapter.drop_db()

    def test_basic(self):
        person = mock.AdminPerson()
        person.name = "Name"
        person.save()

        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "Name")

        person = mock.AdminPerson.get(id = 1)

        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "Name")

        person.name = "NameChanged"
        person.save()

        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "NameChanged")
        self.assertEqual(appier_extras.admin.Snapshot.count(), 1)

        person.name = "NameChangedAgain"
        person.save()

        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "NameChangedAgain")
        self.assertEqual(appier_extras.admin.Snapshot.count(), 2)

        person = mock.AdminPerson.restore_snapshot(1)

        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "NameChanged")
        self.assertEqual(appier_extras.admin.Snapshot.count(), 3)

        person = mock.AdminPerson.get(id = 1)

        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "NameChanged")
        self.assertEqual(appier_extras.admin.Snapshot.count(), 3)

        person = mock.AdminPerson.restore_snapshot(1)

        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "NameChangedAgain")
        self.assertEqual(appier_extras.admin.Snapshot.count(), 4)

        person.delete()

        person = mock.AdminPerson.get(id = 1, raise_e = False)

        self.assertEqual(person, None)

        person = mock.AdminPerson.restore_snapshot(1)

        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "NameChangedAgain")

        person = mock.AdminPerson.get(id = 1)

        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "NameChangedAgain")

        person.delete()

        father = mock.AdminPerson()
        father.name = "Father"
        father.save()

        self.assertEqual(father.id, 2)
        self.assertEqual(father.name, "Father")

        father = mock.AdminPerson.get(id = 2)

        self.assertEqual(father.id, 2)
        self.assertEqual(father.name, "Father")

        father.delete()

        person = mock.AdminPerson.restore_snapshot(1)

        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "NameChangedAgain")

        father = mock.AdminPerson.restore_snapshot(2)

        self.assertEqual(father.id, 2)
        self.assertEqual(father.name, "Father")
