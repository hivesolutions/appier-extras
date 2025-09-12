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

import json
import base64
import unittest

import appier

import appier_extras


class SerializationTest(unittest.TestCase):
    def test_bytes_encoder(self):
        bytes_value = b"hello world"

        data_json = json.dumps(dict(data=bytes_value), cls=appier_extras.BytesEncoder)

        encoded_expect = base64.b64encode(bytes_value).decode("utf-8")
        loaded = json.loads(data_json)

        if appier.legacy.PYTHON_3:
            self.assertIn(encoded_expect, data_json)
            self.assertEqual(loaded["data"], encoded_expect)
        else:
            self.assertIn("hello world", data_json)
            self.assertEqual(loaded["data"], "hello world")

    def test_bytes_decoder(self):
        if not appier.legacy.PYTHON_3:
            self.skipTest("Python 3 is required")

        bytes_value = b"foo bar"
        encoded_value = base64.b64encode(bytes_value).decode("utf-8")

        data = dict(data=encoded_value)
        result = appier_extras.bytes_decoder(data)

        self.assertIs(result, data)
        self.assertEqual(result["data"], bytes_value)
