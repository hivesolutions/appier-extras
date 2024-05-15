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

import appier


class BytesEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that makes sure that bytes
    are properly encoded as Base64 strings.
    """

    def default(self, obj):
        if isinstance(obj, appier.legacy.BYTES):
            return base64.b64encode(obj).decode("utf-8")
        return json.JSONEncoder.default(self, obj)


def bytes_decoder(map):
    for key, value in map.items():
        if isinstance(value, str):
            try:
                decoded_value = base64.b64decode(value)
                map[key] = decoded_value
            except (ValueError, TypeError):
                pass
    return map
