#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Appier Framework.
#
# Hive Appier Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Appier Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Appier Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

import appier

class Base(appier.Model):

    ENABLE_S = {
        True : "enabled",
        False : "disabled"
    }

    id = appier.field(
        type = int,
        index = True,
        increment = True
    )

    enabled = appier.field(
        type = bool,
        index = True,
        meta = "enum",
        enum = ENABLE_S
    )

    description = appier.field(
        meta = "text"
    )

    created = appier.field(
        type = int,
        index = True,
        immutable = True,
        meta = "datetime"
    )

    modified = appier.field(
        type = int,
        index = True,
        meta = "datetime"
    )

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

    def pre_create(self):
        appier.Model.pre_create(self)

        if not hasattr(self, "enabled"): self.enabled = True
        self.created = time.time()
        self.modified = time.time()

    def pre_update(self):
        appier.Model.pre_update(self)

        self.modified = time.time()

    def get_e(self, *args, **kwargs):
        return self.get(enabled = True, *args, **kwargs)

    def find_e(self, *args, **kwargs):
        return self.find(enabled = True, *args, **kwargs)

    def enable_s(self):
        self.enabled = True
        self.save()

    def disable_s(self):
        self.enabled = False
        self.save()

    def to_locale(self, *args, **kwargs):
        return self.owner.to_locale(*args, **kwargs)

    def send_email(self, *args, **kwargs):
        bulk = kwargs.get("bulk", False)
        sender = appier.conf("SENDER_EMAIL", "Appier <no-reply@appier.hive.pt>")
        base_url = appier.conf("BASE_URL", "http://appier.hive.pt")
        settings = dict(logo = True)
        headers = {
            "List-Unsubscribe" : "<" + base_url + "/unsubscribe>"
        }
        if bulk: headers["Auto-Submitted"] = "auto-generated"
        if bulk: headers["Precedence"] = "bulk"
        self.owner.email(
            sender = sender,
            base_url = base_url,
            settings = settings,
            headers = headers,
            *args,
            **kwargs
        )
