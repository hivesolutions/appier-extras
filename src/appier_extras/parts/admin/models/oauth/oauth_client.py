#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from appier_extras.parts.admin.models import base

class OAuthClient(base.Base):

    name = appier.field(
        index = "hashed",
        immutable = True
    )
    """ The name of the client, this should be used as primary
    identification to the end-user """

    client_id = appier.field(
        index = "hashed",
        private = True,
        immutable = True
    )
    """ The client identifier issued to the client during the
    registration process (should be globally unique) """

    client_secret = dict(
        index = "hashed",
        private = True,
        immutable = True
    )
    """ The client secret issued to the client during the
    registration process (should be globally unique) """

    redirect_uri = dict()
    """ The redirect uri where to redirect, the user agent
    after a successful token request operation """

    @classmethod
    def validate(cls):
        return super(OAuthClient, cls).validate() + [
            appier.not_null("name"),
            appier.not_empty("name"),
            appier.is_lower("name"),
            appier.string_gt("name", 3),
            appier.string_lt("name", 64),
            appier.not_duplicate("name", cls._name()),

            appier.not_null("client_id"),
            appier.not_empty("client_id"),
            appier.string_gt("client_id", 32),
            appier.not_duplicate("client_id", cls._name()),

            appier.not_null("client_secret"),
            appier.not_empty("client_secret"),
            appier.string_gt("client_secret", 32),
            appier.not_duplicate("client_secret", cls._name()),

            appier.not_null("redirect_uri"),
            appier.not_empty("redirect_uri"),
            appier.is_url("redirect_uri")
        ]

    def pre_validate(self):
        base.Base.pre_create(self)

        if not hasattr(self, "client_id") or self.client_id == None:
            self.client_id = appier.gen_token()
        if not hasattr(self, "client_secret") or self.client_secret == None:
            self.client_secret = appier.gen_token()
