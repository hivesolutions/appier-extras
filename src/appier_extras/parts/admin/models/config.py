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

from appier_extras.parts.admin.models import base

class Config(base.Base):

    _CONFIG = {}
    """ The reference to the last dictionary of
    configuration that has been loaded into memory
    this may be used to calculate the deltas, for
    proper removal (garbage collection) """

    key = appier.field(
        index = "all",
        default = True
    )

    value = appier.field(
        index = "all"
    )

    @classmethod
    def setup(cls):
        super(Config, cls).setup()
        cls._flush()
        appier.get_bus().bind("config/reload", cls._flush)

    @classmethod
    def validate(cls):
        return super(Config, cls).validate() + [
            appier.not_null("key"),
            appier.not_empty("key"),
            appier.not_duplicate("key", cls._name()),

            appier.not_null("value"),
            appier.not_empty("value")
        ]

    @classmethod
    def list_names(cls):
        return ["key", "value"]

    @classmethod
    def config_d(cls):
        configs = cls.find_e()
        return dict([(config.key, config.value) for config in configs])

    @classmethod
    def _flush(cls):
        # retrieves the dictionary of configurations currently
        # enabled in the data source
        config_d = cls.config_d()

        # iterates over the complete set of configuration
        # key in the previous configuration, to try to determine
        # the ones that have been removed
        for key in cls._CONFIG:
            if key in config_d: continue
            appier.conf_r(key)

        # iterates over the complete set of key value pairs
        # in the configuration dictionary to set these configuration
        for key, value in appier.legacy.iteritems(config_d):
            appier.conf_s(key, value)

        # updates the current configuration dictionary with
        # the one that has just been retrieved
        cls._CONFIG = config_d

    def post_create(self):
        base.Base.post_create(self)
        self.owner.trigger_bus("config/reload")

    def post_update(self):
        base.Base.post_update(self)
        self.owner.trigger_bus("config/reload")

    def post_delete(self):
        base.Base.post_delete(self)
        self.owner.trigger_bus("config/reload")
