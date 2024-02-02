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

import base64
import unittest

import appier

import appier_extras


class ImageTest(unittest.TestCase):
    def test_resize_image(self):
        try:
            import PIL.Image
        except ImportError:
            self.skipTest("PIL not installed")

        image_data_b64 = b"iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAAAAABVicqIAAAAP0lEQVRo3u3NMQ0AAAgDMOZfNFPBQdIaaHbuRSKRSCQSiUQikUgkEolEIpFIJBKJRCKRSCQSiUQikUgkkv9JAZqQZAF1iHVBAAAAAElFTkSuQmCC"
        image_data = base64.b64decode(image_data_b64)

        image = PIL.Image.open(appier.legacy.BytesIO(image_data))
        self.assertEqual(image.size, (100, 100))
        self.assertEqual(image.format, "PNG")

        get_data, etag = appier_extras.resize_image(image_data, width=50, height=50)
        output_data = get_data()
        output_image = PIL.Image.open(appier.legacy.BytesIO(output_data))
        self.assertEqual(output_image.size, (50, 50))
        self.assertEqual(output_image.format, "PNG")
        self.assertEqual(etag, None)

        get_data, etag = appier_extras.resize_image(image_data, height=50)
        output_data = get_data()
        output_image = PIL.Image.open(appier.legacy.BytesIO(output_data))
        self.assertEqual(output_image.size, (50, 50))
        self.assertEqual(output_image.format, "PNG")
        self.assertEqual(etag, None)

        get_data, etag = appier_extras.resize_image(image_data, format="JPEG")
        output_data = get_data()
        output_image = PIL.Image.open(appier.legacy.BytesIO(output_data))
        self.assertEqual(output_image.size, (100, 100))
        self.assertEqual(output_image.format, "JPEG")
        self.assertEqual(etag, None)

        get_data, etag = appier_extras.resize_image(
            image_data, width=50, height=50, format="JPEG"
        )
        output_data = get_data()
        output_image = PIL.Image.open(appier.legacy.BytesIO(output_data))
        self.assertEqual(output_image.size, (50, 50))
        self.assertEqual(output_image.format, "JPEG")
        self.assertEqual(etag, None)
