#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (C) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from appier_extras.parts.admin.models import base

class Settings(base.Base):

    facebook_token = appier.field(
        index = True
    )

    github_token = appier.field(
        index = True
    )

    google_token = appier.field(
        index = True
    )

    live_token = appier.field(
        index = True
    )

    twitter_token = appier.field(
        index = True
    )

    twitter_token_secret = appier.field(
        index = True
    )

    extra = appier.field(
        type = dict,
        index = True
    )

    @classmethod
    def list_names(cls):
        return ["id", "description", "created"]

    @classmethod
    def get_settings(cls, *args, **kwargs):
        return cls.singleton(*args, **kwargs)

    def get_facebook_api(self):
        import facebook
        redirect_url = self.url_for("admin.oauth_facebook", absolute = True)
        access_token = self.facebook_token
        return facebook.Api(
            client_id = appier.conf("FB_ID"),
            client_secret = appier.conf("FB_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token
        )

    def get_github_api(self):
        import github
        redirect_url = self.url_for("admin.oauth_github", absolute = True)
        access_token = self.github_token
        return github.Api(
            client_id = appier.conf("GITHUB_ID"),
            client_secret = appier.conf("GITHUB_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token
        )

    def get_google_api(self):
        import google
        redirect_url = self.url_for("admin.oauth_google", absolute = True)
        access_token = self.google_token
        return google.Api(
            client_id = appier.conf("GOOGLE_ID"),
            client_secret = appier.conf("GOOGLE_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token
        )

    def get_live_api(self):
        import live
        redirect_url = self.url_for("admin.oauth_live", absolute = True)
        access_token = self.live_token
        return live.Api(
            client_id = appier.conf("LIVE_ID"),
            client_secret = appier.conf("LIVE_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token
        )

    def get_twitter_api(self):
        import twitter
        redirect_url = self.url_for("admin.oauth_twitter", absolute = True)
        oauth_token = self.twitter_token
        oauth_token_secret = self.twitter_token_secret
        return twitter.Api(
            client_key = appier.conf("TWITTER_KEY"),
            client_secret = appier.conf("TWITTER_SECRET"),
            redirect_url = redirect_url,
            oauth_token = oauth_token,
            oauth_token_secret = oauth_token_secret
        )
