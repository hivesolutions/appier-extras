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
import types
import zipfile
import tempfile

import appier

from appier_extras import base

class ExportPart(appier.Part):
    """
    Modular part class that provides an infra-structure for the individual
    export of models using a JSON exporting format.
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
            (("GET",), "/json/<str:model>.zip", self.zip_model_json, None, True),
            (("GET",), "/json/<str:model>/<str:_id>.zip", self.zip_entity_json, None, True)
        ]

    @appier.ensure(token = "admin", context = "admin")
    def zip_model_json(self, model):
        model_json = self.admin_part.show_model_json(model)

        _zip_handle, zip_path = tempfile.mkstemp()
        zip_file = zipfile.ZipFile(zip_path, mode = "w", allowZip64 = True)

        prefix = "%s_%s" % (self.info_dict()["name"], model)

        try:
            zip_file.writestr("%s.json" % prefix, json.dumps(model_json))
        finally:
            zip_file.close()

        return self.send_path(
            zip_path,
            name = "%s_json.zip" % prefix
        )

    @appier.ensure(token = "admin", context = "admin")
    def zip_entity_json(self, model, _id):
        model_json = self.admin_part.show_entity_json(model, _id)

        _zip_handle, zip_path = tempfile.mkstemp()
        zip_file = zipfile.ZipFile(zip_path, mode = "w", allowZip64 = True)
        prefix = "%s_%s_%s" % (self.info_dict()["name"], model, _id)

        try:
            zip_file.writestr("%s.json" % prefix, json.dumps(model_json))
        finally: zip_file.close()
        return self.send_path(
            zip_path,
            name = "%s_json.zip" % prefix
        )

    @classmethod
    @appier.link(name = "JSON Global")
    def json_collection(cls, model_cls):
        return appier.get_app().url_for(
            "admin.show_model_json",
            model = model_cls._under()
        )

    @classmethod
    @appier.link(name = "JSON Zip Global")
    def json_collection_zip(cls, model_cls):
        return appier.get_app().url_for(
            "export.zip_model_json",
            model = model_cls._under()
        )

    @classmethod
    @appier.operation(
        name = "Import JSON",
        description = "Imports a JSON representing this entity.",
        parameters = (
            ("Contents", "contents", "text"),
            ("Empty source", "empty", bool, False)
        )
    )
    def import_json(cls, contents, empty):
        appier.verify(not contents == None, "Contents must be defined.")

        if empty: cls.delete_c()

        if appier.legacy.is_bytes(contents):
            contents = contents.decode("utf-8")

        models = json.loads(contents)
        if not isinstance(models, list): models = [models]
        for model_d in models:
            del model_d["_id"]
            model = cls(model_d)
            model.save()

    @classmethod
    @appier.operation(
        name = "Import JSON File",
        parameters = (
            ("JSON File", "file", "file"),
            ("Empty source", "empty", bool, False)
        )
    )
    def import_json_file(cls, model_cls, file, empty):
        def callback(model_d):
            model = cls(model_d)
            model.save()

        if empty: model_cls.delete_c()
        model_cls._json_import(file, callback)

    @classmethod
    @appier.operation(
        name = "Import JSON Zip File",
        parameters = (
                ("JSON Zip File", "file", "file"),
                ("Empty source", "empty", bool, False)
        )
    )
    def import_json_zip(cls, model_cls, file, empty):
        if empty: model_cls.delete_c()

        _file_name, _mime_type, data = file
        with zipfile.ZipFile(appier.legacy.BytesIO(data), "r") as open_zip:
            for name in open_zip.namelist():
                content = open_zip.read(name)
                model_cls.import_json(content, False)

    @appier.link(name = "JSON")
    def json(self):
        return appier.get_app().url_for(
            "admin.show_entity_json",
            model = self.__class__.__name__.lower(),
            _id = self._id
        )

    @appier.link(name = "JSON Zip")
    def json_zip(self):
        return appier.get_app().url_for(
            "export.zip_entity_json",
            model = self.__class__.__name__.lower(),
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

        base_cls = base_cls or appier.Model

        class_methods = class_methods or (
            ExportPart.json_collection,
            ExportPart.json_collection_zip,
            ExportPart.import_json,
            ExportPart.import_json_file,
            ExportPart.import_json_zip
        )

        instance_methods = instance_methods or (
            ExportPart.json,
            ExportPart.json_zip
        )

        # adds both the class and the instance method names to the sequence of ordered
        # values to be computed by the base class (new methods added)
        base_cls._ordered += [class_method.__name__ for class_method in class_methods]
        base_cls._ordered += [instance_method.__name__ for instance_method in instance_methods]

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

            # iterates over the complete set of class methods to add to the current
            # model class, then instantiates them and set the as attributes
            for class_method in class_methods:
                bound_method = types.MethodType(class_method, model)
                setattr(model, class_method.__name__, bound_method)

            # invalidates the methods cache in the model class, so that the
            # next retrieval already includes the newly added methods
            if "_methods" in model.__dict__: del model.__dict__["_methods"]
