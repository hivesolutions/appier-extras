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

from appier_extras.parts.admin import models

class Facebook(object):

    def has_facebook(self):
        try: import facebook
        except: facebook = None
        if not facebook: return False
        if not appier.conf("FB_ID"): return False
        if not appier.conf("FB_SECRET"): return False
        return True

    def ensure_facebook_account(self, create = True):
        api = self.get_facebook_api()
        user = api.self_user()
        account = models.Account.get(
            email = user["email"],
            rules = False,
            raise_e = False
        )

        if not account:
            if not create: raise appier.NotFoundError(
                message = "no account found for facebook account"
            )

            account = models.Account(
                username = user["email"],
                email = user["email"],
                password = api.access_token,
                password_confirm = api.access_token,
                facebook_id = user["id"],
                facebook_token = api.access_token,
                type = models.Account.USER_TYPE
            )
            account.save()
            account = account.reload(rules = False)

        if not account.facebook_id:
            account.facebook_id = user["id"]
            account.facebook_token = api.access_token
            account.save()

        if not account.facebook_token == api.access_token:
            account.facebook_token = api.access_token
            account.save()

        account.touch_s()
        account._set_session()

        return account

    def ensure_facebook_api(self, state = None, scope = None, refresh = False):
        access_token = self.session.get("fb.access_token", None)
        if access_token and not refresh: return
        api = self.get_facebook_api(scope = scope)
        return api.oauth_authorize(state = state)

    def get_facebook_api(self, scope = None):
        import facebook
        kwargs = dict()
        redirect_url = self.url_for("admin.oauth_facebook", absolute = True)
        access_token = self.session and self.session.get("fb.access_token", None)
        if scope: kwargs["scope"] = scope
        return facebook.Api(
            client_id = appier.conf("FB_ID"),
            client_secret = appier.conf("FB_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token,
            **kwargs
        )
