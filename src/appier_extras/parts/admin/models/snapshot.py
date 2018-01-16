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

class Snapshot(base.Base):

    target_id = appier.field(
        type = int,
        index = "all",
        description = "Target ID"
    )
    """ The unique identifier of the entity to be used
    to identify the entity globally (should be unique) """

    target_cls = appier.field(
        index = "hashed",
        description = "Target Class"
    )
    """ The name of the class for the entity (as a string) """

    model_data = appier.field(
        type = dict
    )
    """ The payload information on the entity/model
    data that is going to be used to restore the
    entity back to the original state (if requested) """

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
    def order_name(cls):
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

    def pre_save(self):
        base.Base.pre_save(self)
        self.model_data = self.model_data_b

    @appier.operation(name = "Restore")
    def restore_s(self, save = True, validate = False):
        model_data = dict(self.model_data_s)
        target_cls = appier.get_model(self.target_cls)
        target_cls.types(model_data)
        model = target_cls.old(model = model_data, safe = False)
        if not save: return model
        exists = not target_cls.get(id = self.target_id, raise_e = False) == None
        if save: model.save(
            validate = validate,
            is_new = not exists,
            increment_a = False,
            immutables_a = False
        )
        return model

    @property
    def model_data_s(self):
        """
        Safe version of the model data that should ensure that the
        primary object identifier of the model is properly encoded
        as an object identifier.

        :rtype: Dictionary
        :return: The safe version of the model data, with proper
        object identifiers set.
        """

        cls = self.__class__
        if not "_id" in self.model_data: return self.model_data
        adapter = cls._adapter()
        model_data = dict(self.model_data)
        model_data["_id"] = adapter.object_id(model_data["_id"])
        return model_data

    @property
    def model_data_b(self):
        """
        Bulk version of the model data that should be ready for
        safe data source storing.

        The primary goal is to properly encode the object id of
        the model in a safe "dictionary way".

        :rtype: Dictionary
        :return: The bulk version of the model data, with proper
        object identifiers encoded in "dictionary way".
        """

        cls = self.__class__
        if not "_id" in self.model_data: return self.model_data
        model_data = dict(self.model_data)
        model_data["_id"] = str(model_data["_id"])
        return model_data
