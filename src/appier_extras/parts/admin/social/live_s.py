#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier


class Live(object):
    def ensure_live(self):
        appier.ensure_pip("live", package="live_api")

    def has_live(self):
        try:
            import live
        except Exception:
            live = None
        if not live:
            return False
        if not appier.conf("LIVE_ID"):
            return False
        if not appier.conf("LIVE_SECRET"):
            return False
        return True

    def ensure_live_account(self, create=True, safe=True, next=None):
        api = self.get_live_api()
        user = api.self_user()
        email = user["emails"]["preferred"]
        live_id = user["id"]
        account = self.owner.admin_account.get(
            live_id=live_id, rules=False, raise_e=False
        )
        account = account or self.owner.admin_account.from_session()
        account = account or self.owner.admin_account.get(
            email=email, rules=False, raise_e=False
        )

        if safe and "live.access_token" in self.session:
            del self.session["live.access_token"]

        if not account:
            if not create:
                raise appier.NotFoundError(
                    message="No account found for Microsoft Live account"
                )

            account = self.owner.admin_account(
                username=email,
                email=email,
                password=api.access_token,
                password_confirm=api.access_token,
                live_id=live_id,
                live_token=api.access_token,
                type=self.owner.admin_account.USER_TYPE,
            )
            account.save()
            account = account.reload(rules=False)

        if not account.live_id:
            account.live_id = live_id
            account.live_token = api.access_token
            account.save()

        if not account.live_token == api.access_token:
            account.live_token = api.access_token
            account.save()

        if account.two_factor_enabled:
            account._set_2fa()
            return self.url_for(self.owner.two_factor_route_admin, next=next)

        account.touch_login_s()
        account._set_account()

    def unset_live_account(self):
        account = self.owner.admin_account.from_session()
        account.live_id = None
        account.live_token = None
        account.save()

    def ensure_live_api(self, state=None, scope=None, refresh=False):
        access_token = self.session.get("live.access_token", None)
        if access_token and not refresh:
            return
        api = self.get_live_api()
        return api.oauth_authorize(state=state)

    def get_live_api(self, scope=None):
        import live

        kwargs = dict()
        redirect_url = self.url_for("admin.oauth_live", absolute=True)
        access_token = self.session and self.session.get("live.access_token", None)
        if scope:
            kwargs["scope"] = scope
        return live.API(
            client_id=appier.conf("LIVE_ID"),
            client_secret=appier.conf("LIVE_SECRET"),
            redirect_url=redirect_url,
            access_token=access_token,
            **kwargs
        )
