#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from appier_extras.parts.admin.models import base

class Locale(base.Base):

    locale = appier.field(
        index = "all",
        default = True
    )

    data_j = appier.field(
        type = dict,
        meta = "longmap",
        description = "JSON Data"
    )

    @classmethod
    def setup(cls):
        super(Locale, cls).setup()
        cls._flush()
        appier.get_bus().bind("locale/reload", cls._flush)

    @classmethod
    def validate(cls):
        return super(Locale, cls).validate() + [
            appier.not_null("locale"),
            appier.not_empty("locale"),
            appier.string_eq("locale", 5),
            appier.not_duplicate("locale", cls._name()),

            appier.not_null("data_j"),
            appier.not_empty("data_j")
        ]

    @classmethod
    def list_names(cls):
        return ["locale", "description"]

    @classmethod
    def bundles_d(cls, locale = None):
        bundles = cls.find_e()
        return dict([(bundle.locale, bundle.data_j) for bundle in bundles])

    @classmethod
    def _flush(cls):
        # retrieves the dictionary of bundles currently
        # enabled in the data source
        bundles_d = cls.bundles_d()

        # iterates over the complete set of locale data pairs
        # in the bundles dictionary to set these bundles (locales)
        for locale, data_j in appier.legacy.iteritems(bundles_d):
            appier.get_app()._register_bundle(data_j, locale)

    def post_create(self):
        appier.Model.post_create(self)
        self.owner.trigger_bus("locale/reload")

    def post_update(self):
        appier.Model.post_update(self)
        self.owner.trigger_bus("locale/reload")

    def post_delete(self):
        appier.Model.post_delete(self)
        self.owner.trigger_bus("locale/reload")
