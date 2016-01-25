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

from appier_extras.parts.admin.models import base

class Config(base.Base):

    key = appier.field(
        index = True,
        default = True
    )

    value = appier.field(
        index = True
    )

    @classmethod
    def setup(cls):
        super(Config, cls).setup()
        cls._flush()

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
    def _flush(cls):
        configs = cls.find()
        for config in configs: appier.conf_s(config.key, config.value)

    def post_create(self):
        appier.Model.post_create(self)
        appier.conf_s(self.key, self.value)

    def post_update(self):
        appier.Model.post_update(self)
        appier.conf_s(self.key, self.value)

    def post_delete(self):
        appier.Model.post_delete(self)
        appier.conf_s(self.key, None)
