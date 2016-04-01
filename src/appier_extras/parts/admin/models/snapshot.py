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

class Snapshot(base.Base):

    target_id = appier.field(
        type = int,
        index = True
    )

    target_cls = appier.field(
        index = True
    )

    model_data = appier.field(
        type = dict
    )

    @classmethod
    def validate(cls):
        return super(Snapshot, cls).validate() + [
            appier.not_null("target_id"),

            appier.not_null("target_cls"),
            appier.not_empty("target_cls"),

            appier.not_null("model_data")
        ]

    @classmethod
    def list_names(cls):
        return ["id", "created", "target_id", "target_cls"]

    @classmethod
    def order_name(self):
        return ["id", -1]

    @classmethod
    def is_indexed(cls):
        return False

    @classmethod
    def create_snapshot(
        cls,
        target_id,
        target_cls,
        model_data
    ):
        snapshot = cls(
            target_id = target_id,
            target_cls = target_cls.__name__,
            model_data = model_data
        )
        snapshot.save()

    @appier.operation(name = "Restore")
    def restore_s(self, save = True, validate = False):
        target_cls = appier.get_model(self.target_cls)
        target_cls.types(self.model_data)
        model = target_cls.old(model = self.model_data, safe = False)
        if not save: return model
        exists = not target_cls.get(id = self.target_id, raise_e = False) == None
        if save: model.save(
            validate = validate,
            is_new = not exists,
            increment_a = False,
            immutables_a = False
        )
        return model
