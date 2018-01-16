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

import appier

from appier_extras import base

class DiagPart(appier.Part):
    """
    Modular part class that provides an infra-structure of diagnostics
    that allow more and better debugging of an Application.
    """

    def version(self):
        return base.VERSION

    def load(self):
        appier.Part.load(self)

        appier.App.add_custom("before_request", self.before_request)
        appier.App.add_custom("after_request", self.after_request)

    def before_request(self):
        pass

    def after_request(self):
        print(self._combined_log())

    def _common_log(self, user = "root"):
        template = "%s - %s [%s] \"%s %s %s\" %d %s"
        return template % (
            self.request.address,
            user,
            self.request.get_sdate(),
            self.request.method,
            self.request.path,
            self.request.protocol,
            self.request.code,
            str(self.request.result_l or "-")
        )

    def _combined_log(self, user = "root"):
        template = "%s - %s [%s] \"%s %s %s\" %d %s \"%s\" \"%s\""
        return template % (
            self.request.address,
            user,
            self.request.get_sdate(),
            self.request.method,
            self.request.path,
            self.request.protocol,
            self.request.code,
            str(self.request.result_l or "-"),
            self.request.get_header("Referer") or "",
            self.request.get_header("User-Agent") or ""
        )
