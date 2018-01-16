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

class NetTest(unittest.TestCase):

    def test_size_round_unit(self):
        result = appier_extras.size_round_unit(209715200, space = True)
        self.assertEqual(result, "200 MB")

        result = appier_extras.size_round_unit(20480, space = True)
        self.assertEqual(result, "20 KB")

        result = appier_extras.size_round_unit(2048, reduce = False, space = True)
        self.assertEqual(result, "2.00 KB")

        result = appier_extras.size_round_unit(2500, space = True)
        self.assertEqual(result, "2.44 KB")

        result = appier_extras.size_round_unit(2500, reduce = False, space = True)
        self.assertEqual(result, "2.44 KB")

        result = appier_extras.size_round_unit(1)
        self.assertEqual(result, "1B")

        result = appier_extras.size_round_unit(2048, minimum = 2049, reduce = False)
        self.assertEqual(result, "2048B")

        result = appier_extras.size_round_unit(2049, places = 4, reduce = False)
        self.assertEqual(result, "2.001KB")

        result = appier_extras.size_round_unit(2048, places = 0, reduce = False)
        self.assertEqual(result, "2KB")

        result = appier_extras.size_round_unit(2049, places = 0, reduce = False)
        self.assertEqual(result, "2KB")
