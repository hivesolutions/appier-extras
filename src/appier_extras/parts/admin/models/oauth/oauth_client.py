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
from appier_extras.parts.admin.models.oauth import oauth_token

class OAuthClient(base.Base):

    name = appier.field(
        index = "hashed",
        immutable = True
    )
    """ The name of the client, this should be used as primary
    identification to the end-user """

    client_id = appier.field(
        index = "hashed",
        safe = True,
        immutable = True,
        description = "Client ID"
    )
    """ The client identifier issued to the client during the
    registration process (should be globally unique) """

    client_secret = dict(
        index = "hashed",
        safe = True,
        private = True,
        immutable = True
    )
    """ The client secret issued to the client during the
    registration process (should be globally unique) """

    redirect_uri = dict(
        meta = "url",
        description = "Redirect URI"
    )
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

            appier.not_null("redirect_uri"),
            appier.not_empty("redirect_uri"),
            appier.is_url("redirect_uri")
        ]

    @classmethod
    def list_names(cls):
        return ["name", "client_id", "redirect_uri"]

    @classmethod
    def _readable(cls, plural = False):
        return "OAuth Clients" if plural else "OAuth Client"

    def pre_create(self):
        base.Base.pre_create(self)

        if not hasattr(self, "client_id") or not self.client_id:
            self.client_id = appier.gen_token()
        if not hasattr(self, "client_secret") or not self.client_secret:
            self.client_secret = appier.gen_token()

    @appier.operation(name = "Invalidate Tokens", level = 2)
    def invalidate_s(self):
        """
        Operation that invalidates the complete set of oauth (access)
        tokens associated with the current oauth client.

        This is a serious operation that should be used carefully to
        avoid unwanted behavior and loss of availability.
        """

        # retrieves the complete set of oauth (access) tokens for the
        # current client and runs the delete operation (removing them)
        tokens = oauth_token.OAuthToken.find(client = self.id)
        for token in tokens: token.delete()
