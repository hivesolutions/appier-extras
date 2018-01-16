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

class CSFRPartTest(unittest.TestCase):

    def setUp(self):
        self.app = appier.App(
            parts = (appier_extras.CSFRPart,),
            session_c = appier.MemorySession
        )
        self.app.csfr_limit = 0

    def tearDown(self):
        self.app.unload()

    def test_csfr(self):
        token = self.app.csfr_part._gen_token(scope = "test")
        result = appier_extras.csfr_ensure(self.app, token, scope = "test")

        self.assertEqual(result, token)

        self.assertRaises(
            appier.AppierException,
            lambda: appier_extras.csfr_ensure(self.app, "hello world", scope = "test")
        )

        token = self.app.csfr_part._gen_token(scope = "test")
        self.app.csfr_part._gen_token(scope = "test")
        self.assertRaises(
            appier.AppierException,
            lambda: appier_extras.csfr_ensure(self.app, token, scope = "test")
        )
