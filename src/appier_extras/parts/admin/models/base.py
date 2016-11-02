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

import csv
import time
import random
import string
import hashlib
import datetime

import appier

RANDOM_RANGE = string.ascii_uppercase + string.digits
""" The range defining the various characters that are
going to be used in the generation of the random string
value that is going to be used as basis for secret generation """

class Base(appier.Model):

    ENABLE_S = {
        True : "enabled",
        False : "disabled"
    }

    id = appier.field(
        type = int,
        index = True,
        increment = True,
        safe = True
    )

    enabled = appier.field(
        type = bool,
        index = True,
        initial = True,
        meta = "enum",
        enum = ENABLE_S
    )

    description = appier.field(
        meta = "text",
        default = True
    )

    created = appier.field(
        type = int,
        index = True,
        safe = True,
        immutable = True,
        meta = "datetime"
    )

    modified = appier.field(
        type = int,
        index = True,
        safe = True,
        meta = "datetime"
    )

    meta = appier.field(
        type = dict
    )

    def __str__(self):
        value = appier.Model.__str__(self)
        if not value: value = str(self.id)
        return value

    def __unicode__(self):
        value = appier.Model.__unicode__(self)
        if not value: value = appier.legacy.UNICODE(self.id)
        return value

    def __cmp__(self, value):
        if not hasattr(value, "id"): return -1
        return self.id.__cmp__(value.id)

    def __lt__(self, value):
        if not hasattr(value, "id"): return False
        return self.id.__lt__(value.id)

    def __eq__(self, value):
        if not hasattr(value, "id"): return False
        return self.id.__eq__(value.id)

    def __ne__(self, value):
        return not self.__eq__(value)

    @classmethod
    def get_e(cls, *args, **kwargs):
        return cls.get(enabled = True, *args, **kwargs)

    @classmethod
    def find_e(cls, *args, **kwargs):
        return cls.find(enabled = True, *args, **kwargs)

    @classmethod
    def create_names(cls):
        names = super(Base, cls).create_names()
        names.remove("id")
        return names

    @classmethod
    def list_names(cls):
        names = super(Base, cls).list_names()
        names.remove("enabled")
        return names

    @classmethod
    def order_name(self):
        return "id"

    @classmethod
    def index_names(cls):
        return [cls.default()]

    @classmethod
    def title_name(cls):
        return cls.default()

    @classmethod
    def description_name(cls):
        return None

    @classmethod
    def is_indexed(cls):
        return True

    @classmethod
    def is_snapshot(cls):
        return False

    @classmethod
    def build_index_g(cls, *args, **kwargs):
        models = cls.find(*args, **kwargs)
        for model in models: model.build_index()

    @classmethod
    def restore_snapshot(cls, id, snapshot_id = None):
        from appier_extras.parts.admin.models import snapshot
        kwargs = dict(
            target_id = id,
            target_cls = cls.__name__,
            sort = [("id", -1)]
        )
        if snapshot_id: kwargs["id"] = snapshot_id
        snapshot = snapshot.Snapshot.get(**kwargs)
        return snapshot.restore_s()

    @classmethod
    def send_email_g(cls, owner, *args, **kwargs):
        owner = owner or appier.get_app()
        sender = appier.conf("SENDER_EMAIL", "Appier <no-reply@appier.hive.pt>")
        base_url = appier.conf("BASE_URL", "http://appier.hive.pt")
        bulk = appier.conf("BULK_EMAIL", False, cast = bool)
        unsubscribe = appier.conf("UNSUBSCRIBE_EMAIL", False, cast = bool)
        logo = appier.conf("LOGO_EMAIL", False, cast = bool)
        inline = appier.conf("INLINE_EMAIL", False, cast = bool)
        sender = kwargs.pop("sender", sender)
        base_url = kwargs.pop("base_url", base_url)
        bulk = kwargs.pop("bulk", bulk)
        unsubscribe = kwargs.pop("unsubscribe", unsubscribe)
        logo = kwargs.pop("logo", logo)
        inline = kwargs.pop("inline", inline)
        kwargs["owner"] = owner
        settings = dict(
            bulk = bulk,
            unsubscribe = unsubscribe,
            logo = logo
        )
        headers = dict()
        if bulk: headers["Auto-Submitted"] = "auto-generated"
        if bulk: headers["Precedence"] = "bulk"
        if unsubscribe: headers["List-Unsubscribe"] = "<" + base_url + "/unsubscribe>"
        html_handler = lambda html: cls._inlinify(html)
        html_handler = html_handler if inline else None
        owner.email(
            sender = sender,
            base_url = base_url,
            settings = settings,
            headers = headers,
            html_handler = html_handler,
            *args,
            **kwargs
        )

    @classmethod
    @appier.operation(name = "Empty All", level = 2, devel = True)
    def op_empty_s(cls):
        cls.delete_c()

    @classmethod
    def _build(cls, model, map):
        pass

    @classmethod
    def _csv_import(
        cls,
        file,
        callback,
        strict = False,
        delimiter = ",",
        quotechar = "\"",
        quoting = csv.QUOTE_MINIMAL,
        encoding = "utf-8"
    ):
        is_unicode = appier.legacy.PYTHON_3
        _file_name, mime_type, data = file
        is_csv = mime_type in ("text/csv", "application/vnd.ms-excel")
        if not is_csv and strict:
            raise appier.OperationalError(
                message = "Invalid mime type '%s'" % mime_type
            )
        args, _varargs, kwargs = appier.legacy.getargspec(callback)[:3]
        has_header = True if "header" in args or kwargs else False
        if is_unicode:
            data = data.decode(encoding)
            buffer = appier.legacy.StringIO(data)
        else:
            buffer = appier.legacy.BytesIO(data)
        csv_reader = csv.reader(
            buffer,
            delimiter = delimiter,
            quotechar = quotechar,
            quoting = quoting
        )
        header = next(csv_reader)
        for line in csv_reader:
            if not is_unicode: line = [value.decode(encoding) for value in line]
            if has_header: callback(line, header = header)
            else: callback(line)

    @classmethod
    def _inlinify(cls, data, engine = None):
        engine = engine or appier.conf("INLINER_ENGINE", None)
        if not engine: return data
        method = getattr(cls, "_inlinify_" + engine)
        return method(data)

    @classmethod
    def _inlinify_premailer(cls, data):
        premailer = appier.import_pip("premailer")
        return premailer.transform(data)

    @classmethod
    def _inlinify_toronado(cls, data):
        toronado = appier.import_pip("toronado")
        return toronado.from_string(data)

    def pre_create(self):
        appier.Model.pre_create(self)

        if not hasattr(self, "enabled"): self.enabled = True
        self.created = time.time()
        self.modified = time.time()

    def pre_update(self):
        appier.Model.pre_update(self)

        self.modified = time.time()
        self.build_snapshot()

    def pre_delete(self):
        appier.Model.pre_delete(self)

        self.build_snapshot()

    def post_save(self):
        appier.Model.post_save(self)

        self.build_index()

    def post_delete(self):
        appier.Model.post_delete(self)

        self.destroy_index()

    def build_index(self, use_class = True):
        from appier_extras.parts.admin.models import search

        # retrieves the reference to the class of the entity to be indexed
        # and verifies that the (model) class is enabled for indexing, in
        # case it's not returns the control flow immediately no indexing required
        cls = self.__class__
        if not cls.is_indexed(): return

        # retrieves the complete set of attribute names that are going
        # to be used for characterization of the current entity, these
        # values should be changed on a model basis
        cls_name = cls._name()
        names = cls.index_names()
        title_name = cls.title_name()
        description_name = cls.description_name()

        # reloads the current instance, critical to obtain default values
        # and then deletes the complete set of indexes of the entity as
        # new ones are going to be built
        self = self.reload()
        self.destroy_index()

        # retrieves both the title and the description representation
        # values for the current entity, as expected for creation
        title = self[title_name]
        if description_name: description = self[description_name]
        elif use_class: description = cls_name
        else: description = None

        # verifies that the current instance contains both the identifier
        # and the title (requires representation) otherwise returns control
        if not self._id: return
        if not title: return

        # iterates over the complete set of names that are going to
        # be used in the indexing process and for each of them creates
        # new search index entry with the information of the entity
        for name in names:
            value = self[name]
            if not value: continue
            search.Search.create_index(
                value,
                self._id,
                cls,
                title,
                target_description = description
            )

    def destroy_index(self):
        from appier_extras.parts.admin.models import search

        cls = self.__class__
        search.Search.delete_indexes(self._id, cls)

    def build_snapshot(self):
        from appier_extras.parts.admin.models import snapshot

        # retrieves the reference to the class of the entity to have a snapshot
        # and verifies that the (model) class is enabled for snapshotting, in
        # case it's not returns the control flow immediately no snapshot required
        cls = self.__class__
        if not cls.is_snapshot(): return

        # reloads the current model with the proper settings to be able to store
        # any data present in the model including safe, private and immutable as
        # this model is going to be used as the basis of the snapshot
        self = self.reload(
            eager_l = False,
            rules = False,
            build = False,
            meta = False,
            raise_e = False
        )

        # in case the instance was not found, possible under some circumstances where
        # the data is not currently stored in the data source (eg: snapshot restore)
        # the control flow is returned immediately (not possible to restore data)
        if not self: return

        # applies the filter to the model to be able to retrieve a sanitized map
        # based model to be used in the snapshot process
        model = self._filter(
            increment_a = False,
            immutables_a = False,
            normalize = True
        )

        # runs the snapshot creation process for the current instance, note that
        # the provided model data should always represent the complete state
        snapshot.Snapshot.create_snapshot(self.id, cls, model_data = model)

    def enable_s(self):
        self.enabled = True
        self.save()

    def disable_s(self):
        self.enabled = False
        self.save()

    def to_locale(self, *args, **kwargs):
        return self.owner.to_locale(*args, **kwargs)

    def send_email(self, *args, **kwargs):
        cls = self.__class__
        return cls.send_email_g(self.owner, *args, **kwargs)

    def secret(self):
        token = "".join(random.choice(RANDOM_RANGE) for _index in range(32))
        token_bytes = appier.legacy.bytes(token)
        url_sha1 = hashlib.sha1(token_bytes)
        return url_sha1.hexdigest()

    @appier.operation(name = "Enable")
    def op_enable_s(self):
        self = self.reload(rules = False)
        self.enable_s()

    @appier.operation(name = "Disable")
    def op_disable_s(self):
        self = self.reload(rules = False)
        self.disable_s()

    @property
    def created_d(self):
        return datetime.datetime.fromtimestamp(self.created)

    @property
    def modified_d(self):
        return datetime.datetime.fromtimestamp(self.modified)
