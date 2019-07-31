#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import json
import zipfile

import appier

from appier_extras import base

class ExportPart(appier.Part):
    """
    Modular part class that provides an infra-structure for the individual
    export of models using a JSON exporting format.

    This parts uses a monkey patching approach so that the model classes
    are changed adding the new export links.
    """

    def __init__(self, *args, **kwargs):
        appier.Part.__init__(self, *args, **kwargs)

    def version(self):
        return base.VERSION

    def load(self):
        appier.Part.load(self)
        self._monkey_patch()

    def routes(self):
        return [
            (("GET",), "/export/<str:model>.json", self.model_json, None, True),
            (("GET",), "/export/<str:model>.zip", self.model_zip, None, True),
            (("GET",), "/export/<str:model>/<str:_id>.json", self.entity_json, None, True)
        ]

    @classmethod
    @appier.link(name = "JSON (Export)", context = True)
    def json_global(cls, view = None, context = None, absolute = False):
        return appier.get_app().url_for(
            "export.model_json",
            model = cls._under(),
            view = view,
            context = context,
            absolute = absolute
        )

    @classmethod
    @appier.link(name = "ZIP (Export)", context = True)
    def zip_global(cls, view = None, context = None, absolute = False):
        return appier.get_app().url_for(
            "export.model_zip",
            model = cls._under(),
            view = view,
            context = context,
            absolute = absolute
        )

    @classmethod
    @appier.operation(
        name = "Import JSON (Export)",
        parameters = (
            ("JSON File", "file", "file"),
            ("Empty source", "empty", bool, False)
        )
    )
    def import_json(cls, file, empty):
        def callback(model_d):
            if "_id" in model_d: del model_d["_id"]
            model = cls(model_d)
            model.save(validate = False, verify = False)

        if empty: cls.delete_c()
        cls._json_import(file, callback)

    @classmethod
    @appier.operation(
        name = "Import ZIP (Export)",
        parameters = (
                ("ZIP File", "file", "file"),
                ("Empty source", "empty", bool, False)
        )
    )
    def import_zip(cls, file, empty):
        if empty: cls.delete_c()

        with zipfile.ZipFile(file, "r") as open_zip:
            for name in open_zip.namelist():
                content = open_zip.read(name)
                cls.import_json(content, False)

    @appier.ensure(token = "admin", context = "admin")
    def model_json(self, model):
        model_c = self.owner.get_model(model)
        object = appier.get_object(
            alias = True,
            find = True,
            limit = 0
        )
        models = self.owner.admin_part._find_view(
            model_c,
            map = True,
            rules = False,
            **object
        )
        return models

    @appier.ensure(token = "admin", context = "admin")
    def model_zip(self, model):
        encoding = self.field("encoding", default = "utf-8")

        model_c = self.owner.get_model(model)
        object = appier.get_object(
            alias = True,
            find = True,
            limit = 0
        )
        models = self.owner.admin_part._find_view(
            model_c,
            map = True,
            rules = False,
            **object
        )

        prefix = "%s-%s" % (self.owner.name, model)

        # creates the in memory file that is going to be used for the storage
        # of the ZIP file that is going to be created
        zip_io = appier.legacy.BytesIO()

        try:
            # creates the ZIP file using the in memory file and then dumps the
            # JSON based data into the associated directory, notice that a proper
            # encoding operation may be required to have a bytes object
            models_s = json.dumps(models)
            if not appier.legacy.is_bytes(models_s): models_s = models_s.encode(encoding)
            zip_file = zipfile.ZipFile(zip_io, mode = "w", allowZip64 = True)
            try: zip_file.writestr("%s.json" % prefix, models_s)
            finally: zip_file.close()

            # seeks the in memory file back to the initial position
            # and then reads the complete set of contents from it
            zip_io.seek(0)
            data = zip_io.read()
        finally:
            zip_io.close()

        return data

    @appier.ensure(token = "admin", context = "admin")
    def entity_json(self, model, _id):
        model_c = self.owner.get_model(model)
        entity = model_c.get(
             map = True,
             rules = False,
            _id = self.get_adapter().object_id(_id)
        )
        return entity

    @appier.link(name = "JSON")
    def json(self):
        return appier.get_app().url_for(
            "export.entity_json",
            model = self.__class__._under(),
            _id = self._id
        )

    def _monkey_patch(
        self,
        models = None,
        base_cls = None,
        class_methods = None,
        instance_methods = None
    ):
        # verifies that a set of model classes have been provided to the method
        # and if that's not the case assumes that the complete set of model classes
        # registers in the current application should be patched
        models = models or list(self.owner.models_l)

        # runs the default operation on the base class so that if no value is provided
        # the default (parent) Appier class is used as the root of the monkey patch
        base_cls = base_cls or appier.Model

        # runs the defaulting on the class methods, these methods are considered the
        # recommended ones to be used in the initial monkey patching
        class_methods = class_methods or (
            ExportPart.json_global,
            ExportPart.zip_global,
            ExportPart.import_json,
            ExportPart.import_zip
        )

        # defaults the instance methods so that the required ones are used for the
        # monkey patching operation (as expected)
        instance_methods = instance_methods or (
            ExportPart.json,
        )

        # iterates over the complete set of class methods to add to the base
        # model class, then instantiates them and set the as attributes
        for class_method in class_methods:
            bound_method = classmethod(class_method.__func__)
            setattr(base_cls, class_method.__name__, bound_method)

        # iterates over the "special" instance methods to be added and changes
        # them to comply with the new instance intrinsics
        for instance_method in instance_methods:
            setattr(base_cls, instance_method.__name__, instance_method)

        # iterates over the complete set of model classes that are going to
        # be patched by adding the class and instance methods
        for model in models:
            # in case the model is not a sub class of the base class for
            # the current operation (nothing to be done) continues the loop
            if not issubclass(model, base_cls): continue

            # iterates over the "special" instance methods to be added and schedules
            # them to be bounded once the model instance is created, this is done
            # by adding them to the extra methods sequence of the model class
            for instance_method in instance_methods:
                model._extra_methods.append(
                    (
                        instance_method.__name__,
                        instance_method.__func__ if hasattr(instance_method, "__func__") else instance_method
                    )
                )

            # invalidates the methods cache in the model class, so that the
            # next retrieval already includes the newly added methods
            if "_methods" in model.__dict__: del model.__dict__["_methods"]
