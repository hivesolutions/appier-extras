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
    def build_index_g(cls, *args, **kwargs):
        models = cls.find(*args, **kwargs)
        for model in models: model.build_index()

    @classmethod
    def send_email_g(cls, owner, *args, **kwargs):
        owner = owner or appier.get_app()
        sender = appier.conf("SENDER_EMAIL", "Appier <no-reply@appier.hive.pt>")
        base_url = appier.conf("BASE_URL", "http://appier.hive.pt")
        bulk = appier.conf("BULK_EMAIL", False, cast = bool)
        unsubscribe = appier.conf("UNSUBSCRIBE_EMAIL", False, cast = bool)
        logo = appier.conf("LOGO_EMAIL", False, cast = bool)
        sender = kwargs.pop("sender", sender)
        base_url = kwargs.pop("base_url", base_url)
        bulk = kwargs.pop("bulk", bulk)
        unsubscribe = kwargs.pop("unsubscribe", unsubscribe)
        logo = kwargs.pop("logo", logo)
        settings = dict(
            bulk = bulk,
            unsubscribe = unsubscribe,
            logo = logo
        )
        headers = dict()
        if bulk: headers["Auto-Submitted"] = "auto-generated"
        if bulk: headers["Precedence"] = "bulk"
        if unsubscribe: headers["List-Unsubscribe"] = "<" + base_url + "/unsubscribe>"
        owner.email(
            sender = sender,
            base_url = base_url,
            settings = settings,
            headers = headers,
            *args,
            **kwargs
        )

    @classmethod
    def _build(cls, model, map):
        pass

    def pre_create(self):
        appier.Model.pre_create(self)

        if not hasattr(self, "enabled"): self.enabled = True
        self.created = time.time()
        self.modified = time.time()

    def pre_update(self):
        appier.Model.pre_update(self)

        self.modified = time.time()

    def post_save(self):
        appier.Model.post_save(self)

        self.build_index()

    def build_index(self, use_class = True):
        from appier_extras.parts.admin.models import search
        cls = self.__class__
        if not cls.is_indexed(): return
        cls_name = cls._name()
        names = cls.index_names()
        title_name = cls.title_name()
        description_name = cls.description_name()
        search.Search.delete_indexes(self._id, cls)
        for name in names:
            value = self[name]
            title = self[title_name]
            if description_name: description = self[description_name]
            elif use_class: description = cls_name
            else: description = None
            if not self._id: continue
            if not title: continue
            search.Search.create_index(
                value,
                self._id,
                cls,
                title,
                target_description = description
            )

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

    @property
    def created_d(self):
        return datetime.datetime.fromtimestamp(self.created)

    @property
    def modified_d(self):
        return datetime.datetime.fromtimestamp(self.modified)
