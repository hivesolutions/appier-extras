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

import csv
import json
import time
import random
import string
import hashlib
import datetime
import collections

import appier

RANDOM_RANGE = string.ascii_uppercase + string.digits
""" The range defining the various characters that are
going to be used in the generation of the random string
value that is going to be used as basis for secret generation """

class Base(appier.Model):
    """
    Top level abstract class from which all the appier admin
    based models should inherit. It contains utility structures
    and logic to better handle a model under appier admin.

    Only models that inherit from this abstract model will be
    shown in the appier admin back-office.
    """

    ENABLE_S = {
        True : "enabled",
        False : "disabled"
    }

    id = appier.field(
        type = int,
        index = "all",
        increment = True,
        safe = True,
        description = "ID",
        observations = """The base identifier of the entity to
        be used as a unique value on the entity context"""
    )
    """ The global incremental identifier of the base model
    this should always be considered a unique way of addressing
    a certain model inhering from this base class """

    enabled = appier.field(
        type = bool,
        index = "all",
        initial = True,
        meta = "enum",
        enum = ENABLE_S,
        observations = """Simple flag that controls if the entity
        is considered to be enabled, respecting this flag is not
        mandatory and relies on specific usage context"""
    )
    """ Boolean field that defines if a certain entity is considered
    to be enabled or disabled, the meaning of disable should depend
    on the usage context, but typically should be used instead of a
    concrete removal operation """

    description = appier.field(
        meta = "text",
        default = True,
        observations = """Plain text description of the entity, proper
        usage should be defined by the context"""
    )
    """ Global description value for which the meaning should be defined
    by the context of usage (eg: name, observations, etc.) """

    created = appier.field(
        type = int,
        index = "all",
        safe = True,
        immutable = True,
        meta = "datetime",
        observations = """Date when the entity was initially created, should
        be immutable (not changeable)"""
    )
    """ The original date and time of the entity creation, this should
    be an immutable timestamp and never changed """

    modified = appier.field(
        type = int,
        index = "all",
        safe = True,
        meta = "datetime",
        observations = """Date when the entity was last modified"""
    )
    """ The date and time of the latest save operation for the current
    entity, note that the create operation changes this value """

    meta = appier.field(
        type = dict,
        description = "Metadata",
        observations = """Dictionary based information to be "attached"
        to the entity, proper usage depends on context"""
    )
    """ Additional (unstructured) information to be stored together with
    the entity for unpredicted purposes, note that these values should not
    be used for search operation as they are not indexed """

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
    def count_e(cls, *args, **kwargs):
        return cls.count(enabled = True, *args, **kwargs)

    @classmethod
    def paginate_e(cls, *args, **kwargs):
        return cls.paginate(enabled = True, *args, **kwargs)

    @classmethod
    def get_v(cls, *args, **kwargs):
        kwargs = cls.apply_views(kwargs)
        return cls.get(*args, **kwargs)

    @classmethod
    def find_v(cls, *args, **kwargs):
        kwargs = cls.apply_views(kwargs)
        return cls.find(*args, **kwargs)

    @classmethod
    def count_v(cls, *args, **kwargs):
        kwargs = cls.apply_views(kwargs)
        return cls.count(*args, **kwargs)

    @classmethod
    def paginate_v(cls, *args, **kwargs):
        kwargs = cls.apply_views(kwargs)
        return cls.paginate(*args, **kwargs)

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
    def order_name(cls):
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
    def is_abstract(cls):
        return True

    @classmethod
    def is_indexed(cls):
        return True

    @classmethod
    def is_snapshot(cls):
        return False

    @classmethod
    def secret_g(cls, hash = None):
        hash = hash or hashlib.sha1
        token = "".join(random.choice(RANDOM_RANGE) for _index in range(32))
        token_bytes = appier.legacy.bytes(token)
        token_hash = hash(token_bytes)
        return token_hash.hexdigest()

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
        settings = dict(
            bulk = bulk,
            unsubscribe = unsubscribe,
            logo = logo
        )
        headers = dict()
        if bulk: headers["Auto-Submitted"] = "auto-generated"
        if bulk: headers["Precedence"] = "bulk"
        if unsubscribe: headers["List-Unsubscribe"] = "<" + base_url + "/unsubscribe>"
        html_handler = cls._inlinify
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
    def apply_views(cls, object, owner = None):
        # tries to retrieve the reference to the owner of the current
        # context or uses the global one otherwise (fallback)
        owner = owner or appier.get_app()

        # verifies if there are any view defined under the current
        # session if that's not the case returns immediately as there's
        # nothing left to be filtered, otherwise retrieves the views to
        # be used to filter the current object context
        if not "views" in owner.session: return object
        views = owner.session["views"]

        # creates a copy of the object so that it does not get modified
        # by the operation to be applied to it (avoids possible issues)
        object = dict(object)

        # iterates over the complete set of views defined under the current
        # session to be able to update the object accordingly, constraining
        # the context of resolution of that object (less results)
        for view in views:
            if appier.legacy.is_str(view):
                view_cls = owner.get_model(view)
                view = view_cls.view_r
            is_callable = hasattr(view, "__call__")
            if is_callable: view = view(target = cls, owner = owner)
            object.update(view)

        # returns the final object to the caller method so that it can be
        # used to constrain contexts according to the current session views
        return object

    @classmethod
    @appier.operation(name = "Empty All", level = 2, devel = True)
    def op_empty_s(cls):
        cls.delete_c()

    @classmethod
    def _csv_import(
        cls,
        file,
        callback,
        callback_header = None,
        strict = False,
        named = False,
        delimiter = ",",
        quotechar = "\"",
        quoting = csv.QUOTE_MINIMAL,
        encoding = "utf-8"
    ):
        is_unicode = appier.legacy.PYTHON_3
        csv_reader = cls._csv_read(
            file,
            strict = strict,
            named = named,
            delimiter = delimiter,
            quotechar = quotechar,
            quoting = quoting,
            encoding = encoding
        )
        args, _varargs, kwargs = appier.legacy.getargspec(callback)[:3]
        has_header = True if "header" in args or kwargs else False
        has_map = True if "map" in args or kwargs else False
        header = next(csv_reader)
        if not is_unicode: header = [value.decode(encoding) for value in header]
        if callback_header: callback_header(header)
        if named: tuple_t = collections.namedtuple("csv_tuple", header)
        for line in csv_reader:
            kwargs = dict()
            if not is_unicode: line = [value.decode(encoding) for value in line]
            if named: line = tuple_t(*line)
            if has_header: kwargs["header"] = header
            if has_map: kwargs["map"] = dict(zip(header, line))
            callback(line, **kwargs)

    @classmethod
    def _csv_read(
        cls,
        file,
        strict = False,
        named = False,
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
                message = "Invalid MIME type '%s'" % mime_type
            )
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
        return csv_reader

    @classmethod
    def _json_import(
        cls,
        file,
        callback,
        callback_header = None,
        strict = False,
        encoding = "utf-8"
    ):
        json_data = cls._json_read(file, strict = strict, encoding = encoding)
        header = appier.legacy.keys(json_data[0]) if json_data else []
        if callback_header: callback_header(header)
        for item in json_data: callback(item)

    @classmethod
    def _json_read(
        cls,
        file,
        strict = False,
        encoding = "utf-8"
    ):
        _file_name, mime_type, data = file
        is_json = mime_type in ("text/json", "application/json")
        if not is_json and strict:
            raise appier.OperationalError(
                message = "Invalid MIME type '%s'" % mime_type
            )
        data = data.decode(encoding)
        json_data = json.loads(data)
        return json_data

    @classmethod
    def _inlinify(cls, data, engine = None, *args, **kwargs):
        engine = engine or appier.conf("INLINER_ENGINE", None)
        if not engine: return data
        method = getattr(cls, "_inlinify_" + engine)
        return method(data, *args, **kwargs)

    @classmethod
    def _inlinify_premailer(cls, data, *args, **kwargs):
        premailer = appier.import_pip("premailer")
        keep_style_tags = kwargs.get("keep_style_tags", True)
        inliner = premailer.Premailer(data, keep_style_tags = keep_style_tags)
        return inliner.transform(data)

    @classmethod
    def _inlinify_toronado(cls, data, *args, **kwargs):
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

    def previous(self, name = "id", raise_e = False, *args, **kwargs):
        kwargs[name] = {"$lt" : getattr(self, name)}
        kwargs["sort"] = ((name, -1),)
        return self.get_v(
            raise_e = raise_e,
            **kwargs
        )

    def next(self, name = "id", raise_e = False, *args, **kwargs):
        kwargs[name] = {"$gt" : getattr(self, name)}
        kwargs["sort"] = ((name, 1),)
        return self.get_v(
            raise_e = raise_e,
            **kwargs
        )

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

    def touch_s(self):
        self.save()

    def update_meta_s(self, meta = None, **kwargs):
        meta = kwargs if meta == None else meta
        appier.verify(isinstance(meta, dict))
        if not self.meta: self.meta = meta
        else: self.meta.update(meta)
        self.save()

    def to_locale(self, *args, **kwargs):
        return self.owner.to_locale(*args, **kwargs)

    def send_email(self, *args, **kwargs):
        cls = self.__class__
        owner = kwargs.pop("owner", self.owner)
        kwargs["own"] = kwargs.pop("own", self)
        return cls.send_email_g(owner, *args, **kwargs)

    def secret(self, hash = None):
        cls = self.__class__
        return cls.secret_g(hash = hash)

    @appier.operation(name = "Enable")
    def op_enable_s(self):
        self = self.reload(rules = False)
        self.enable_s()

    @appier.operation(name = "Disable")
    def op_disable_s(self):
        self = self.reload(rules = False)
        self.disable_s()

    @appier.operation(name = "Touch", devel = True)
    def op_touch_s(self):
        self = self.reload(rules = False)
        self.touch_s()

    @property
    def created_d(self):
        return datetime.datetime.fromtimestamp(self.created)

    @property
    def modified_d(self):
        return datetime.datetime.fromtimestamp(self.modified)
