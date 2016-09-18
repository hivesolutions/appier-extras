#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import functools

import appier

def csfr_protect(scope = None):

    def decorator(function):

        @functools.wraps(function)
        def interceptor(self, *args, **kwargs):
            token = self.field("csfr_token", None)
            csfr_ensure(self, token, scope = scope)
            return appier.call_safe(function, self, *args, **kwargs)
        return interceptor

    return decorator

def csfr_ensure(self, token, scope = None):
    csfr_m = self.session.get("csfr", {})
    tokens, _tokens_l = csfr_m.get(scope, ({}, []))
    result = tokens.pop(token, None)
    if result: return token
    raise appier.AppierException(
        message = "Invalid CSFR protect token",
        code = 403
    )
