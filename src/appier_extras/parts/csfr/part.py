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

import appier

class CSFRPart(appier.Part):
    """
    Modular part class that provides the required infra-structure
    for the control of CSFR attacks.

    Should be used with proper knowledge of the inner workings of
    the captcha mechanism to avoid any security problems.

    @see: http://en.wikipedia.org/wiki/Cross-site_request_forgery
    """

    def load(self):
        appier.Part.load(self)

        self.owner.context["csfr"] = self.csfr

    def csfr(self, scope = None, name = "csfr_token"):
        token = self._gen_token(scope = scope)
        return self.owner.escape_jinja(
            "<input type=\"hidden\" name=\"%s\" value=\"%s\"/>" %\
            (name, token)
        )

    def _gen_token(self, scope = None):
        csfr_m = self.session.get("csfr", {})
        tokens = csfr_m.get(scope, {})
        token = appier.gen_token()
        tokens[token] = True
        csfr_m[scope] = tokens
        self.session["csfr"] = csfr_m
        return token
