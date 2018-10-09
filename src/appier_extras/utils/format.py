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

import string

import appier

class SafeFormatter(string.Formatter):

    def __init__(self, fallback = ""):
        self.fallback = fallback

    def get_field(self, field_name, args, kwargs):
        if appier.legacy.PYTHON_3:
            import _string
            first, rest = _string.formatter_field_name_split(field_name)
        else:
            first, rest = field_name._formatter_field_name_split()

        try:
            obj = self.get_value(first, args, kwargs)
        except:
            return self.fallback, first

        for is_attr, key in rest:
            if is_attr:
                try:
                    obj = getattr(obj, key)
                except:
                    obj = self.fallback
                    break
            else:
                try:
                    obj = obj[key]
                except:
                    obj = self.fallback
                    break

        return obj, first
