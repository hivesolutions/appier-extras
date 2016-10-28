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

import appier

from . import handler

class SematextPart(appier.Part):
    """
    Modular part class that provides the system to handle Sematext
    logging requests automatically on Appier.

    This part uses the Sematext API client to run all the remote
    calls accordingly.

    :see: http://sematext.com
    """

    def load(self):
        appier.Part.load(self)

        self._api = None
        self.add_handler()

    def add_handler(self, set_default = True):
        log = appier.conf("SEMATEXT_LOG", False, cast = bool)
        buffer_size = appier.conf("SEMATEXT_BUFFER_SIZE", 128, cast = int)
        timeout = appier.conf("SEMATEXT_TIMEOUT", 30, cast = int)
        if not log: return
        api = self._get_api()
        handler_sematext = handler.SematextHandler(
            owner = self,
            api = api,
            buffer_size = buffer_size,
            timeout = timeout
        )
        handler_sematext.setLevel(self.owner.level)
        handler_sematext.setFormatter(self.owner.formatter)
        self.owner.handlers.append(handler_sematext)
        self.logger.addHandler(handler_sematext)
        if not set_default: return
        logger = logging.getLogger()
        logger.addHandler(handler_sematext)

    def _get_api(self):
        if self._api: return self._api
        try: sematext = appier.import_pip("sematext", package = "sematext_api")
        except: return None
        self._api = sematext.Api()
        return self._api
