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

import logging

import appier

from appier_extras import base

from . import handler

class LogglyPart(appier.Part):
    """
    Modular part class that provides the system to handle Loggly
    logging requests automatically on Appier.

    This part uses the Loggly API client to run all the remote
    calls accordingly.

    :see: http://loggly.com
    """

    def __init__(self, *args, **kwargs):
        appier.Part.__init__(self, *args, **kwargs)
        self.log = kwargs.get("log", False)
        self.buffer_size = kwargs.get("buffer_size", 128)
        self.timeout = kwargs.get("timeout", 30)
        self.log = appier.conf("LOGGLY_LOG", self.log, cast = bool)
        self.buffer_size = appier.conf(
            "LOGGLY_BUFFER_SIZE",
            self.buffer_size,
            cast = int
        )
        self.timeout = appier.conf(
            "LOGGLY_TIMEOUT",
            self.timeout,
            cast = int
        )

    def version(self):
        return base.VERSION

    def load(self):
        appier.Part.load(self)

        self._api = None
        self.add_handler()

    def add_handler(self, set_default = True):
        if not self.log: return
        api = self._get_api()
        handler_loggly = handler.LogglyHandler(
            owner = self,
            api = api,
            buffer_size = self.buffer_size,
            timeout = self.timeout
        )
        handler_loggly.setLevel(self.owner.level)
        handler_loggly.setFormatter(self.owner.formatter)
        self.owner.handlers.append(handler_loggly)
        self.logger.addHandler(handler_loggly)
        if not set_default: return
        logger = logging.getLogger()
        logger.addHandler(handler_loggly)

    def _get_api(self):
        if self._api: return self._api
        try: loggly = appier.import_pip("loggly", package = "loggly_api_python")
        except: loggly = None
        if not loggly: return None
        self._api = loggly.API()
        return self._api
