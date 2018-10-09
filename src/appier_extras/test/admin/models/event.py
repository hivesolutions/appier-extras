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

import appier_extras

class EventTest(unittest.TestCase):

    def test_format(self):
        result = appier_extras.admin.Event.format(
            dict(
                name = "{person[name]}",
                person = dict(name = "john")
            )
        )
        self.assertEqual(
            result,
            dict(
                name = "john",
                person = dict(name = "john")
            )
        )

        result = appier_extras.admin.Event.format(
            dict(
                name = "{person[name]}",
                age = "{person[age]}",
                person = dict(name = "john")
            )
        )
        self.assertEqual(
            result,
            dict(
                name = "john",
                age = "",
                person = dict(name = "john")
            )
        )

        result = appier_extras.admin.Event.format(
            dict(
                name = "{person[name]}",
                age = "{person[age]}",
                person = dict(name = "john", age = 21)
            )
        )
        self.assertEqual(
            result,
            dict(
                name = "john",
                age = "21",
                person = dict(name = "john", age = 21)
            )
        )
