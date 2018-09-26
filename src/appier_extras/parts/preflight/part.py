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

class PreflightPart(appier.Part):

    def __init__(self, *args, **kwargs):
        appier.Part.__init__(self, *args, **kwargs)
        self.data = appier.conf("PREFLIGHT_DATA", "")
        self.data_b = appier.legacy.bytes(self.data, force = True)

    def version(self):
        return base.VERSION

    def load(self):
        appier.Part.load(self)

        self.owner.bind("before_request", self._handler)

    def unload(self):
        appier.Part.unload(self)

        self.owner.bind("before_request", self._handler)

    def _handler(self):
        if not self.owner.request.method == "OPTIONS": return
        if self.owner.request.handled: return
        allow_headers = self.request.get_header("Access-Control-Request-Headers", None)
        if allow_headers: self.request.set_header("Access-Control-Allow-Headers", allow_headers)
        self.owner.request.handle(self.data_b)
