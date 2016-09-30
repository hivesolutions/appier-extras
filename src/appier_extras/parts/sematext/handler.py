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

import logging
import datetime

class SematextHandler(logging.Handler):

    def __init__(self, level = logging.NOTSET, api = None, buffer_size = 128):
        logging.Handler.__init__(self, level = level)
        self.api = api
        self.buffer_size = buffer_size
        self.buffer = []

    def emit(self, record):
        # formats the current record according to the defined
        # logging rules so that we can used the resulting message
        # for any logging purposes
        message = self.format(record)

        # retrieves the current date time value as an utc value
        # and then formats it according to the provided format string
        now = datetime.datetime.utcnow()
        now_s = now.strftime("%Y-%m-%dT%H:%M:%S")

        # creates the log record structure that is going to be sent
        # to the sematext infra-structure, this should represent a
        # proper structure ready to be debugged
        log = {
            "@timestamp" : now_s,
            "message" : message
        }

        # adds the new log item to the buffer so that it's properly
        # store for sending and then in case the should flush condition
        # is met the flush operation is performed, running the remote
        # calling operations that should block the infra-structure
        self.buffer.append(log)
        should_flush = len(self.buffer) >= self.buffer_size
        if should_flush: self.flush()

    def flush(self):
        logging.Handler.flush(self)
        self.api.log_bulk("default", self.buffer)
        del self.buffer[:]
