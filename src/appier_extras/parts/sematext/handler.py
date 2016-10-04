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

import os
import socket
import logging
import datetime
import threading

class SematextHandler(logging.Handler):

    def __init__(
        self,
        level = logging.NOTSET,
        owner = None,
        api = None,
        buffer_size = 128,
        timeout = 30
    ):
        logging.Handler.__init__(self, level = level)
        self.owner = owner
        self.api = api
        self.buffer_size = buffer_size
        self.buffer = []
        self._schedule(timeout = timeout)

    def emit(self, record):
        # verifies if the api structure is defined and set and if
        # that's not the case returns immediately
        if not self.api: return

        # retrieves the current date time value as an utc value
        # and then formats it according to the provided format string
        now = datetime.datetime.utcnow()
        now_s = now.strftime("%Y-%m-%dT%H:%M:%S")

        # creates the log record structure that is going to be sent
        # to the sematext infra-structure, this should represent a
        # proper structure ready to be debugged
        log = {
            "@timestamp" : now_s,
            "logger" : record.name,
            "message" : record.message,
            "level" : record.levelname,
            "path" : record.pathname,
            "lineno" : record.lineno,
            "host" : socket.gethostname(),
            "tid" : threading.current_thread().ident,
            "pid" : os.getpid() if hasattr(os, "getpid") else -1,
        }

        # adds the new log item to the buffer so that it's properly
        # store for sending and then in case the should flush condition
        # is met the flush operation is performed, running the remote
        # calling operations that should block the infra-structure
        self.buffer.append(log)
        should_flush = len(self.buffer) >= self.buffer_size
        if should_flush: self.flush()

    def flush(self, force = False):
        logging.Handler.flush(self)

        # verifies if the api structure is defined and set and if
        # that's not the case returns immediately
        if not self.api: return

        # retrieves some references from the current instance that
        # are going to be used in the flush operation
        app = self.owner.owner
        buffer = self.buffer

        # verifies if the buffer is empty and if that's the case and
        # the force flag is not set, returns immediately
        if not buffer and not force: return

        # creates the lambda function that is going to be used for the
        # bulk flushing operation of the buffer, this is going to be
        # called on a delayed (async fashion) so that no blocking occurs
        # in the current logical flow
        call_log = lambda: self.api.log_bulk("default", buffer)

        # schedules the call log operation and then empties the buffer
        # so that it's no longer going to be used (flushed)
        app.delay(call_log)
        self.buffer = []

    def _schedule(self, timeout = 30):
        app = self.owner.owner

        def tick():
            self.flush()
            app.schedule(tick, timeout = timeout)

        app.schedule(tick, timeout = timeout)
