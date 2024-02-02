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

import appier


def resize_image(
    data, etag=None, width=None, height=None, format=None, quality=None, resample=None
):
    def get_data():
        import PIL.Image

        input_stream = appier.legacy.BytesIO(data)
        output_stream = appier.legacy.BytesIO()

        image = PIL.Image.open(input_stream)

        try:
            target_width = width
            target_height = height
            target_format = format if format else image.format

            image_width, image_height = image.size
            if width:
                ratio = float(image_width) / float(width)
            elif height:
                ratio = float(image_height) / float(height)
            else:
                ratio = 1.0

            if not target_width:
                target_width = int(image_width * ratio)
            if not target_height:
                target_height = int(image_height * ratio)

            _resample = (
                (
                    PIL.Image.ANTIALIAS  # type: ignore
                    if hasattr(PIL.Image, "ANTIALIAS")
                    else (PIL.Image.LANCZOS if hasattr(PIL.Image, "LANCZOS") else None)  # type: ignore
                )
                if resample == None
                else resample
            )

            image.thumbnail((target_width, target_height), _resample)
            if quality:
                image.save(output_stream, target_format, quality=quality)
            else:
                image.save(output_stream, target_format)

            output_data = output_stream.getvalue()
        finally:
            input_stream.close()
            output_stream.close()
            image.close()

        return output_data

    etag = "%s-w%s-h%s" % (etag, str(width), str(height)) if etag else etag

    return (get_data, etag)
