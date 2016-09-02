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

class OpbeatPart(appier.Part):
    """
    Modular part class that provides the system to handle Opbeat
    API request automatically on Appier.

    This part used the Opbeat API client to run all the remote
    calls accordingly.

    :see: http://opbeat.com
    """

    def load(self):
        appier.Part.load(self)

        self._api = None

        self.owner.bind("exception", self.exception)

    def exception(self, exception, is_soft = False):
        self.delay(
            self.log_exception,
            args = [exception],
            kwargs = dict(is_soft = is_soft)
        )

    def log_exception(self, exception, is_soft = False):
        api = self._get_api()

        message = hasattr(exception, "message") and\
            exception.message or str(exception)

        payload = dict(
            message = message,
            http = dict(
                url = self.url_for("location", absolute = True),
                method = self.request.method,
                data = self.request.get_data(),
                query_string = self.request.query,
                cookies = self.request.get_header("Cookie"),
                headers = self.request.in_headers,
                remote_host = self.request.get_address(),
                http_host = "absolute.uri",
                user_agent = self.request.get_header("User-Agent"),
                secure = self.request.scheme == "https"
            )
        )

        api.error(payload)

    def _get_api(self):
        import opbeat
        if self._api: return self._api
        self._api = opbeat.Api()
        return self._api
