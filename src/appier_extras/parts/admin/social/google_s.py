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

import appier

class Google(object):

    def ensure_google(self):
        appier.ensure_pip("google", package = "google_api")

    def has_google(self):
        try: import google
        except: google = None
        if not google: return False
        if not appier.conf("GOOGLE_ID"): return False
        if not appier.conf("GOOGLE_SECRET"): return False
        return True

    def ensure_google_account(self, create = True, safe = True):
        api = self.get_google_api()
        user = api.self_user()
        email = user["emails"][0]["value"]
        google_id = user["id"]
        account = self.owner.admin_account.get(
            google_id = google_id,
            rules = False,
            raise_e = False
        )
        account = account or self.owner.admin_account.from_session()
        account = account or self.owner.admin_account.get(
            email = email,
            rules = False,
            raise_e = False
        )

        if safe and "gg.access_token" in self.session:
            del self.session["gg.access_token"]

        if not account:
            if not create: raise appier.NotFoundError(
                message = "No account found for Google account"
            )

            account = self.owner.admin_account(
                username = email,
                email = email,
                password = api.access_token,
                password_confirm = api.access_token,
                google_id = google_id,
                google_token = api.access_token,
                type = self.owner.admin_account.USER_TYPE
            )
            account.save()
            account = account.reload(rules = False)

        if not account.google_id:
            account.google_id = google_id
            account.google_token = api.access_token
            account.save()

        if not account.google_token == api.access_token:
            account.google_token = api.access_token
            account.save()

        account.touch_login_s()
        account._set_session()

        return account

    def unset_google_account(self):
        account = self.owner.admin_account.from_session()
        account.google_id = None
        account.google_token = None
        account.save()

    def ensure_google_api(
        self,
        state = None,
        access_type = None,
        approval_prompt = False,
        scope = None,
        refresh = False
    ):
        access_token = self.session.get("gg.access_token", None)
        if access_token and not refresh: return
        api = self.get_google_api(scope = scope)
        return api.oauth_authorize(
            state = state,
            access_type = access_type,
            approval_prompt = approval_prompt
        )

    def get_google_api(self, scope = None):
        import google
        kwargs = dict()
        redirect_url = self.url_for("admin.oauth_google", absolute = True)
        access_token = self.session and self.session.get("gg.access_token", None)
        if scope: kwargs["scope"] = scope
        return google.API(
            client_id = appier.conf("GOOGLE_ID"),
            client_secret = appier.conf("GOOGLE_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token,
            **kwargs
        )
