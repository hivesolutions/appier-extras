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

class Twitter(object):

    def ensure_twitter(self):
        appier.ensure_pip("twitter", package = "twitter_api")

    def has_twitter(self):
        try: import twitter
        except: twitter = None
        if not twitter: return False
        if not appier.conf("TWITTER_KEY"): return False
        if not appier.conf("TWITTER_SECRET"): return False
        return True

    def ensure_twitter_account(self, create = True, safe = True):
        api = self.get_twitter_api()
        user = api.verify_account()
        email = "%s@twitter.com" % user["screen_name"]
        twitter_username = user["screen_name"]
        account = self.owner.admin_account.get(
            twitter_username = twitter_username,
            rules = False,
            raise_e = False
        )
        account = account or self.owner.admin_account.from_session()
        account = account or self.owner.admin_account.get(
            email = email,
            rules = False,
            raise_e = False
        )

        if safe and "tw.oauth_token" in self.session:
            del self.session["tw.oauth_token"]
        if safe and "tw.oauth_token_secret" in self.session:
            del self.session["tw.oauth_token_secret"]
        if safe and "tw.oauth_temporary" in self.session:
            del self.session["tw.oauth_temporary"]

        if not account:
            if not create: raise appier.NotFoundError(
                message = "No account found for Twitter account"
            )

            account = self.owner.admin_account(
                username = twitter_username,
                email = email,
                password = api.oauth_token,
                password_confirm = api.oauth_token,
                twitter_username = twitter_username,
                twitter_token = api.oauth_token,
                type = self.owner.admin_account.USER_TYPE
            )
            account.save()
            account = account.reload(rules = False)

        if not account.twitter_username:
            account.twitter_username = twitter_username
            account.twitter_token = api.oauth_token
            account.save()

        if not account.twitter_token == api.oauth_token:
            account.twitter_token = api.oauth_token
            account.save()

        account.touch_login_s()
        account._set_session()

        return account

    def unset_twitter_account(self):
        account = self.owner.admin_account.from_session()
        account.twitter_username = None
        account.twitter_token = None
        account.save()

    def ensure_twitter_api(self, state = None, refresh = False):
        oauth_token = self.session.get("tw.oauth_token", None)
        oauth_token_secret = self.session.get("tw.oauth_token_secret", None)
        oauth_temporary = self.session.get("tw.oauth_temporary", True)
        if not oauth_temporary and oauth_token and\
            oauth_token_secret and not refresh: return
        self.session["tw.oauth_token"] = None
        self.session["tw.oauth_token_secret"] = None
        self.session["tw.oauth_temporary"] = True
        api = self.get_twitter_api()
        url = api.oauth_authorize(state = state)
        self.session["tw.oauth_token"] = api.oauth_token
        self.session["tw.oauth_token_secret"] = api.oauth_token_secret
        self.session["tw.oauth_temporary"] = True
        return url

    def get_twitter_api(self):
        import twitter
        redirect_url = self.url_for("admin.oauth_twitter", absolute = True)
        oauth_token = self.session and self.session.get("tw.oauth_token", None)
        oauth_token_secret = self.session and self.session.get("tw.oauth_token_secret", None)
        return twitter.API(
            client_key = appier.conf("TWITTER_KEY"),
            client_secret = appier.conf("TWITTER_SECRET"),
            redirect_url = redirect_url,
            oauth_token = oauth_token,
            oauth_token_secret = oauth_token_secret
        )
