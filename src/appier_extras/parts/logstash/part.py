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

import logging

import appier

from appier_extras import base

from . import handler


class LogstashPart(appier.Part):
    """
    Modular part class that provides the system to handle Logstash
    logging requests automatically on Appier.

    This part uses the Logstash API client to run all the remote
    calls accordingly.

    :see: http://www.elastic.co/products/logstash
    """

    def __init__(self, *args, **kwargs):
        appier.Part.__init__(self, *args, **kwargs)
        self.log = kwargs.get("log", False)
        self.buffer_size = kwargs.get("buffer_size", 128)
        self.timeout = kwargs.get("timeout", 30)
        self.log = appier.conf("LOGSTASH_LOG", self.log, cast=bool)
        self.buffer_size = appier.conf(
            "LOGSTASH_BUFFER_SIZE", self.buffer_size, cast=int
        )
        self.timeout = appier.conf("LOGSTASH_TIMEOUT", self.timeout, cast=int)

    def version(self):
        return base.VERSION

    def info(self):
        info = appier.Part.info(self)
        info.update(log=self.log, buffer_size=self.buffer_size, timeout=self.timeout)
        return info

    def load(self):
        appier.Part.load(self)

        self._api = None
        self.add_handler()

    def add_handler(self, set_default=True):
        if not self.log:
            return
        api = self._get_api()
        handler_logstash = handler.LogstashHandler(
            owner=self, api=api, buffer_size=self.buffer_size, timeout=self.timeout
        )
        handler_logstash.setLevel(self.owner.level)
        handler_logstash.setFormatter(self.owner.formatter)
        self.owner.handlers.append(handler_logstash)
        self.logger.addHandler(handler_logstash)
        if not set_default:
            return
        logger = logging.getLogger()
        logger.addHandler(handler_logstash)

    def _get_api(self):
        if self._api:
            return self._api
        try:
            logstash = appier.import_pip("logstash", package="logstash_api")
        except Exception:
            logstash = None
        if not logstash:
            return None
        self._api = logstash.API()
        return self._api
