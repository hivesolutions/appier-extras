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

class Event(base.Base):

    name = appier.field(
        index = True,
        default = True
    )

    handler = appier.field(
        index = True
    )

    arguments = appier.field(
        type = dict
    )

    @classmethod
    def validate(cls):
        return super(Event, cls).validate() + [
            appier.not_null("name"),
            appier.not_empty("name"),

            appier.not_null("handler"),
            appier.not_empty("handler")
        ]

    @classmethod
    def list_names(cls):
        return ["name", "handler"]

    @classmethod
    def notify_g(cls, name, handlers = None, arguments = {}):
        kwargs = dict(name = name)
        if handlers: kwargs["handler"] = {"$in" : handlers}
        events = cls.find(**kwargs)
        for event in events: event.notify(arguments = arguments)

    @appier.operation(name = "Notify")
    def notify(self, arguments = {}, delay = True, owner = None):
        owner = owner or appier.get_app()
        method = getattr(self, "notify_" + self.handler)
        arguments_m = dict(self.arguments)
        arguments_m.update(arguments)
        arguments_m.update(event = self.name, handler = self.handler)
        kwargs = dict(arguments = arguments_m)
        if delay: owner.delay(method, kwargs = kwargs)
        else: method(arguments, **kwargs)

    def notify_http(self, arguments = {}):
        url = arguments.get("url", None)
        return appier.post(url, data_j = arguments)

    def notify_mailme(self, arguments = {}):
        import mailme
        api = mailme.Api()
        return api.send(arguments)
