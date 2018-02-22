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

import sys
import traceback

import appier

from appier_extras import base

class OpbeatPart(appier.Part):
    """
    Modular part class that provides the system to handle Opbeat
    API requests automatically on Appier.

    This part uses the Opbeat API client to run all the remote
    calls accordingly.

    :see: http://opbeat.com
    """

    def __init__(self, *args, **kwargs):
        appier.Part.__init__(self, *args, **kwargs)
        self.log = kwargs.get("log", False)
        self.log = appier.conf("OPBEAT_LOG", self.log, cast = bool)

    def version(self):
        return base.VERSION

    def load(self):
        appier.Part.load(self)

        self._api = None

        self.owner.bind("exception", self.exception)

        if self.log: appier.ensure_pip(
            "opbeat",
            package = "opbeat_api",
            delayed = True
        )

    def unload(self):
        appier.Part.unload(self)

        self.owner.unbind("exception", self.exception)

    def exception(self, exception, is_soft = False):
        if not self.log: return
        self.log_exception(exception, is_soft = is_soft)

    def log_exception(
        self,
        exception,
        level = "error",
        is_soft = False,
        strict = False
    ):
        if not strict and is_soft: return

        api = self._get_api()
        if not api: return

        _exc_type, _exc_value, exc_traceback = sys.exc_info()
        stacktrace = traceback.extract_tb(exc_traceback)

        message = hasattr(exception, "message") and\
            exception.message or str(exception)

        lines = traceback.format_exc().splitlines()
        lines = appier.App._lines(lines)

        payload = dict(
            message = message,
            level = level,
            exception = dict(
                type = exception.__class__.__name__,
                value = message,
                module = str(exception.__class__.__module__)
            ),
            http = dict(
                url = self.url_for("location", absolute = True),
                method = self.request.method,
                data = self.request.get_encoded(),
                query_string = self.request.query,
                cookies = self.request.get_header("Cookie"),
                headers = self.request.in_headers,
                remote_host = self.request.get_address(),
                http_host = "absolute.uri",
                user_agent = self.request.get_header("User-Agent"),
                secure = self.request.scheme == "https"
            ),
            stacktrace = dict(
                frames = [
                    dict(
                        abs_path = value[0],
                        filename = value[0],
                        lineno = value[1],
                        function = value[2],
                        context_line = value[3],
                    ) for value in stacktrace
                ]
            )
        )

        self.delay(api.error, args = [payload])

    def _get_api(self):
        if self._api: return self._api
        try: import opbeat
        except: return None
        self._api = opbeat.API()
        return self._api
