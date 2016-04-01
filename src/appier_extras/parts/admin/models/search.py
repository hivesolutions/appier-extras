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

class Search(base.Base):

    token = appier.field(
        index = True,
        default = True
    )

    target_id = appier.field(
        index = True
    )

    target_cls = appier.field(
        index = True
    )

    target_title = appier.field()

    target_description = appier.field()

    @classmethod
    def validate(cls):
        return super(Search, cls).validate() + [
            appier.not_null("token"),
            appier.not_empty("token"),

            appier.not_null("target_id"),

            appier.not_null("target_cls"),
            appier.not_empty("target_cls"),

            appier.not_null("target_title"),
            appier.not_empty("target_title")
        ]

    @classmethod
    def list_names(cls):
        return ["id", "token", "target_id", "target_cls"]

    @classmethod
    def order_name(self):
        return ["id", -1]

    @classmethod
    def is_indexed(cls):
        return False

    @classmethod
    def create_index(
        cls,
        token,
        target_id,
        target_cls,
        target_title,
        target_description = None
    ):
        token = cls._ensure_unicode(token)
        target_title = cls._ensure_unicode(target_title)
        target_description = cls._ensure_unicode(target_description)
        index = cls(
            token = token,
            target_id = target_id,
            target_cls = target_cls.__name__,
            target_title = target_title,
            target_description = target_description
        )
        index.save()

    @classmethod
    def find_indexes(cls, target_id, target_cls, *args, **kwargs):
        target_cls = target_cls.__name__
        return cls.find(
            target_id = target_id,
            target_cls = target_cls,
            *args, **kwargs
        )

    @classmethod
    def delete_indexes(cls, target_id, target_cls, *args, **kwargs):
        indexes = cls.find_indexes(target_id, target_cls, build = False)
        for index in indexes: index.delete(*args, **kwargs)

    @classmethod
    def _build(cls, model, map):
        super(Search, cls)._build(model, map)
        target_cls = model["target_cls"]
        target_id = model["target_id"]
        model["url"] = appier.get_app().url_for(
            "admin.show_entity",
            model = target_cls.lower(),
            _id = target_id
        )
        return model

    @classmethod
    def _ensure_unicode(self, value):
        if value == None: return value
        if appier.legacy.is_unicode(value): return value
        return appier.legacy.UNICODE(value)
