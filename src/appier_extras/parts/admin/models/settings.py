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

from appier_extras.parts.admin.models import base

class Settings(base.Base):

    facebook_token = appier.field(
        index = "hashed"
    )

    github_token = appier.field(
        index = "hashed"
    )

    google_token = appier.field(
        index = "hashed"
    )

    google_refresh_token = appier.field(
        index = "hashed"
    )

    google_email = appier.field(
        index = "hashed"
    )

    google_scope = appier.field(
        type = list
    )

    live_token = appier.field(
        index = "hashed"
    )

    twitter_token = appier.field(
        index = "hashed"
    )

    twitter_token_secret = appier.field(
        index = "hashed"
    )

    extra = appier.field(
        type = dict
    )

    @classmethod
    def list_names(cls):
        return ["id", "description", "created"]

    @classmethod
    def get_settings(cls, *args, **kwargs):
        return cls.singleton(*args, **kwargs)

    @classmethod
    def refresh_google_api(cls, access_token):
        settings = cls.get_settings()
        settings.google_token = access_token
        settings.save()

    @classmethod
    def linked_apis(cls):
        linked = dict()
        settings = cls.get_settings()
        if settings.facebook_token: linked["facebook"] = settings.facebook_token
        if settings.github_token: linked["github"] = settings.github_token
        if settings.google_token: linked["google"] = settings.google_email
        if settings.live_token: linked["live"] = settings.live_token
        if settings.twitter_token: linked["twitter"] = settings.twitter_token
        return linked

    @classmethod
    def get_extra(cls, name, default = None):
        settings = cls.get_settings()
        if not settings: return default
        if not settings.extra: return default
        return settings.extra.get(name, default)

    @classmethod
    def set_extra_s(cls, name, value):
        settings = cls.get_settings()
        settings.extra[name] = value
        settings.save()

    @classmethod
    def del_extra_s(cls, name):
        settings = cls.get_settings()
        if not settings: return
        if not settings.extra: return
        if not name in settings.extra: return
        del settings.extra[name]
        settings.save()

    @classmethod
    def _plural(cls):
        return "Settings"

    def get_facebook_api(self):
        try: import facebook
        except: return None
        if not self.facebook_token: return None
        redirect_url = self.owner.url_for("admin.oauth_facebook", absolute = True)
        access_token = self.facebook_token
        return facebook.API(
            client_id = appier.conf("FB_ID"),
            client_secret = appier.conf("FB_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token
        )

    def get_github_api(self):
        try: import github
        except: return None
        if not self.github_token: return None
        redirect_url = self.owner.url_for("admin.oauth_github", absolute = True)
        access_token = self.github_token
        return github.API(
            client_id = appier.conf("GITHUB_ID"),
            client_secret = appier.conf("GITHUB_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token
        )

    def get_google_api(self):
        try: import google
        except: return None
        if not self.google_token: return None
        cls = self.__class__
        redirect_url = self.owner.url_for("admin.oauth_google", absolute = True)
        access_token = self.google_token
        refresh_token = self.google_refresh_token
        api = google.API(
            client_id = appier.conf("GOOGLE_ID"),
            client_secret = appier.conf("GOOGLE_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token,
            refresh_token = refresh_token
        )
        api.bind("access_token", cls.refresh_google_api)
        return api

    def get_live_api(self):
        try: import live
        except: return None
        if not self.live_token: return None
        redirect_url = self.owner.url_for("admin.oauth_live", absolute = True)
        access_token = self.live_token
        return live.API(
            client_id = appier.conf("LIVE_ID"),
            client_secret = appier.conf("LIVE_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token
        )

    def get_twitter_api(self):
        try: import twitter
        except: return None
        if not self.twitter_token: return None
        if not self.twitter_token_secret: return None
        redirect_url = self.owner.url_for("admin.oauth_twitter", absolute = True)
        oauth_token = self.twitter_token
        oauth_token_secret = self.twitter_token_secret
        return twitter.API(
            client_key = appier.conf("TWITTER_KEY"),
            client_secret = appier.conf("TWITTER_SECRET"),
            redirect_url = redirect_url,
            oauth_token = oauth_token,
            oauth_token_secret = oauth_token_secret
        )
