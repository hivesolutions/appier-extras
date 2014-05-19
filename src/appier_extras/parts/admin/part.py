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

import appier

from appier_extras.parts.admin import models

class AdminPart(appier.Part):
    """
    Modular part class providing the automation functionality for
    the generation of a web interface based on the application
    data model for fast prototyping.

    The interface configuration should be done by the way of
    "annotations" in the data model attributes.
    """

    def load(self):
        appier.Part.load(self)

        self.logger.debug("Updating pre-defined application routes ...")
        self.owner.login_route = "admin.login"

        self.logger.debug("Generating admin interfaces ...")
        for model_c in self.models_r:
            self.logger.debug(model_c)

    def routes(self):
        return [
            (("GET",), "/admin", self.index),
            (("GET",), "/admin/signin", self.signin),
            (("POST",), "/admin/signin", self.login),
            (("GET", "POST"), "/admin/signout", self.logout),
            (("GET"), "/admin/recover", self.recover),
            (("POST"), "/admin/recover", self.recover_do),
            (("GET",), "/admin/options", self.options),
            (("POST",), "/admin/options", self.options_action),
            (("GET",), "/admin/status", self.status),
            (("GET",), "/admin/routes", self.list_routes),
            (("GET",), "/admin/accounts/new", self.new_account),
            (("POST",), "/admin/accounts", self.create_account),
            (("GET",), "/admin/accounts/<str:username>", self.show_account),
            (("GET",), "/admin/accounts/<str:username>/mail", self.mail_account),
            (("GET",), "/admin/models", self.list_models),
            (("GET",), "/admin/models/<str:model>.csv", self.show_model_csv),
            (("GET",), "/admin/models/<str:model>", self.show_model),
            (("GET",), "/admin/models/<str:model>/new", self.new_entity),
            (("POST",), "/admin/models/<str:model>", self.create_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>", self.show_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>/edit", self.edit_entity),
            (("POST",), "/admin/models/<str:model>/<str:_id>/edit", self.update_entity),
            (("GET",), "/admin/facebook", self.facebook),
            (("GET",), "/admin/facebook/oauth", self.oauth_facebook),
            (("GET",), "/admin/twitter", self.twitter),
            (("GET",), "/admin/twitter/oauth", self.oauth_twitter),
            (("GET",), "/admin/log.json", self.show_log)
        ]

    def models(self):
        return models

    def template(self, template, style = "fluid", *args, **kwargs):
        template = "%s/%s" % (style, template)
        return appier.Part.template(
            self,
            template,
            owner = self.owner,
            models_d = self.models_d,
            *args,
            **kwargs
        )

    def index(self):
        return self.list_models()

    def signin(self):
        next = self.field("next")
        return self.template("signin.html.tpl", next = next)

    def login(self):
        # retrieves the various fields that are going to be
        # used for the validation of the user under the current
        # authentication/authorization process
        username = self.field("username")
        password = self.field("password")
        next = self.field("next")
        try: account = models.Account.login(username, password)
        except appier.AppierException as error:
            return self.template(
                "signin.html.tpl",
                next = next,
                username = username,
                error = error.message
            )

        # updates the current session with the proper
        # values to correctly authenticate the user
        self.session["username"] = account.username
        self.session["email"] = account.email
        self.session["type"] = account.type_s()
        self.session["tokens"] = account.tokens()

        return self.redirect(
            next or self.url_for("admin.index")
        )

    def logout(self):
        # tries to retrieve the next field as it's going to be used for
        # the redirection operation at the end of the logout operation
        next = self.field("next")

        # verifies the existence of the various account related session
        # attributes and in case they exist removes them from session as
        # the user is currently logging out from session
        if "username" in self.session: del self.session["username"]
        if "email" in self.session: del self.session["email"]
        if "type" in self.session: del self.session["type"]
        if "tokens" in self.session: del self.session["tokens"]
        if "fb.access_token" in self.session: del self.session["fb.access_token"]
        if "tw.oauth_token" in self.session: del self.session["tw.oauth_token"]
        if "tw.oauth_token_secret" in self.session: del self.session["tw.oauth_token_secret"]

        # runs the proper redirect operation, taking into account if the
        # next value has been provided or not
        return self.redirect(
            next or self.url_for("admin.index")
        )

    def recover(self):
        return self.template("recover.html.tpl")

    def recover_do(self):
        identifier = self.field("identifier")
        try: models.Account.recover(identifier)
        except appier.AppierException as error:
            return self.template(
                "recover.html.tpl",
                identifier = identifier,
                error = error.message
            )

        return self.template("done.html.tpl")

    def new_account(self):
        return self.template(
            "account/new.html.tpl",
            account = dict(),
            errors = dict()
        )

    def create_account(self):
        account = models.Account.new()
        account.type = models.Account.USER_TYPE
        account.enabled = False
        try: account.save()
        except appier.ValidationError as error:
            return self.template(
                "account/new.html.tpl",
                account = error.model,
                errors = error.errors
            )

        return self.redirect(
            self.url_for(
                "admin.mail_account",
                username = account.username
            )
        )

    def show_account(self, username):
        raise appier.NotImplementedError()

    def mail_account(self, username):
        raise appier.NotImplementedError()

    @appier.ensure(token = "admin")
    def options(self):
        return self.template(
            "options.html.tpl",
            section = "options",
            errors = dict()
        )

    @appier.ensure(token = "admin")
    def options_action(self):
        type = self.field("type")
        theme = self.field("theme")
        libs = self.field("libs")
        type_s = type.split("-", 1)
        theme_s = theme.split("-", 1)
        type_l = len(type_s)
        theme_l = len(theme_s)

        if type_l == 1: type_s.append("")
        type_s, sub_type_s = type_s

        if theme_l == 1: theme_s.append("")
        theme_s, style_s = theme_s

        type_s = type_s.lower().strip()
        sub_type_s = sub_type_s.lower().strip()
        theme_s = theme_s.lower().strip()
        style_s = style_s.lower().strip()
        libs_s = libs.lower().strip()

        if style_s == "default": style_s = ""

        self.session["type_label"] = type
        self.session["type"] = type_s
        self.session["sub_type"] = sub_type_s
        self.session["label"] = theme
        self.session["theme"] = theme_s
        self.session["style"] = style_s
        self.session["libs"] = libs_s
        self.session["libs_label"] = libs
        self.session.permanent = True

        return self.template(
            "options.html.tpl",
            section = "options",
            errors = dict()
        )

    @appier.ensure(token = "admin")
    def status(self):
        return self.template(
            "status.html.tpl",
            section = "status"
        )

    @appier.ensure(token = "admin")
    def list_routes(self):
        return self.template(
            "routes.html.tpl",
            section = "status",
            routes = self._routes()
        )

    @appier.ensure(token = "admin")
    def list_models(self):
        return self.template(
            "models/list.html.tpl",
            section = "admin"
        )

    @appier.ensure(token = "admin")
    def show_model(self, model):
        model = self.get_model(model)
        object = appier.get_object(
            alias = True,
            page = True,
            find = True
        )
        page = model.paginate(**object)
        entities = model.find(meta = True, **object)
        return self.template(
            "models/show.html.tpl",
            section = "models",
            model = model,
            page = page,
            entities = entities
        )

    @appier.ensure(token = "admin")
    def show_model_csv(self, model):
        model = self.get_model(model)
        entities = model.find(map = True)
        result = appier.serialize_csv(entities)
        self.content_type("text/csv")
        return result

    @appier.ensure(token = "admin")
    def new_entity(self, model):
        model = self.get_model(model)
        return self.template(
            "entities/new.html.tpl",
            section = "models",
            entity = model.__new__(model),
            errors = dict(),
            model = model
        )

    @appier.ensure(token = "admin")
    def create_entity(self, model):
        model = self.get_model(model)
        entity = model.new(safe = False)
        try: entity.save()
        except appier.ValidationError as error:
            return self.template(
                "entities/new.html.tpl",
                section = "models",
                entity = error.model,
                errors = error.errors,
                model = model
            )

        return self.redirect(
            self.url_for("admin.show_model", model = model._name())
        )

    @appier.ensure(token = "admin")
    def show_entity(self, model, _id):
        model = self.get_model(model)
        entity = model.get(
            rules = False,
            meta = True,
            _id = appier.object_id(_id)
        )
        return self.template(
            "entities/show.html.tpl",
            section = "models",
            entity = entity,
            model = model
        )

    @appier.ensure(token = "admin")
    def edit_entity(self, model, _id):
        model = self.get_model(model)
        entity = model.get(
            rules = False,
            meta = True,
            _id = appier.object_id(_id)
        )
        return self.template(
            "entities/edit.html.tpl",
            section = "models",
            entity = entity,
            errors = dict(),
            model = model
        )

    @appier.ensure(token = "admin")
    def update_entity(self, model, _id):
        model = self.get_model(model)
        entity = model.get(
            rules = False,
            meta = True,
            _id = appier.object_id(_id)
        )
        entity.apply(safe_a = False)
        try: entity.save()
        except appier.ValidationError as error:
            return self.template(
                "entities/edit.html.tpl",
                section = "accounts",
                entity = error.model,
                errors = error.errors,
                model = model
            )

        return self.redirect(
            self.url_for(
                "admin.show_entity",
                model = model._name(),
                _id = _id
            )
        )

    def facebook(self):
        next = self.field("next")
        url = self.ensure_facebook_api(state = next)
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for("admin.index")
        )

    def oauth_facebook(self):
        code = self.field("code")
        next = self.field("state")
        api = self.get_facebook_api()
        access_token = api.oauth_access(code)
        self.session["fb.access_token"] = access_token
        self.ensure_facebook_account()
        return self.redirect(
           next or self.url_for("admin.index")
        )

    def twitter(self):
        next = self.field("next")
        url = self.ensure_twitter_api(state = next)
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for("admin.index")
        )

    def oauth_twitter(self):
        oauth_verifier = self.field("oauth_verifier")
        next = self.field("state")
        api = self.get_twitter_api()
        oauth_token, oauth_token_secret = api.oauth_access(oauth_verifier)
        self.session["tw.oauth_token"] = oauth_token
        self.session["tw.oauth_token_secret"] = oauth_token_secret
        self.ensure_twitter_account()
        return self.redirect(
           next or self.url_for("admin.index")
        )

    @appier.ensure(token = "admin")
    def show_log(self):
        memory_handler = self.owner.handler_memory
        count = self.field("count", 100, cast = int)
        level = self.field("level", None)
        return dict(
            messages = memory_handler.get_latest(count = count, level = level)
        )

    def socials(self):
        socials = []
        if self.has_facebook(): socials.append("facebook")
        if self.has_twitter(): socials.append("twitter")

    def has_facebook(self):
        try: import facebook
        except: facebook = None
        if not facebook: return False
        if not appier.conf("FB_ID"): return False
        if not appier.conf("FB_SECRET"): return False
        return True

    def ensure_facebook_account(self):
        api = self.get_facebook_api()
        user = api.self_user()
        account = models.Account.get(
            email = user["email"],
            rules = False,
            raise_e = False
        )

        if not account:
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

        if not account.facebook_token == account.facebook_token:
            account.facebook_token = api.access_token
            account.save()

        account.touch_s()

        self.session["username"] = account.username
        self.session["email"] = account.email
        self.session["type"] = account.type_s()
        self.session["tokens"] = account.tokens()

        return account

    def ensure_facebook_api(self, state = None):
        access_token = self.session.get("fb.access_token", None)
        if access_token: return
        api = self.get_facebook_api()
        return api.oauth_authorize(state = state)

    def get_facebook_api(self):
        import facebook
        redirect_url = self.url_for("admin.oauth_facebook", absolute = True)
        access_token = self.session and self.session.get("fb.access_token", None)
        return facebook.Api(
            client_id = appier.conf("FB_ID"),
            client_secret = appier.conf("FB_SECRET"),
            redirect_url = redirect_url,
            access_token = access_token
        )

    def has_twitter(self):
        try: import twitter
        except: twitter = None
        if not twitter: return False
        if not appier.conf("TWITTER_KEY"): return False
        if not appier.conf("TWITTER_SECRET"): return False
        return True

    def ensure_twitter_account(self):
        api = self.get_twitter_api()
        user = api.verify_account()
        email = "%s@twitter.com" % user["screen_name"]
        account = models.Account.get(
            email = email,
            rules = False,
            raise_e = False
        )

        if not account:
            account = models.Account(
                username = user["screen_name"],
                email = email,
                password = api.oauth_token,
                password_confirm = api.oauth_token,
                twitter_username = user["screen_name"],
                twitter_token = api.oauth_token,
                type = models.Account.USER_TYPE
            )
            account.save()
            account = account.reload(rules = False)

        if not account.twitter_username:
            account.twitter_username = user["screen_name"]
            account.twitter_token = api.oauth_token
            account.save()

        if not account.twitter_token == account.twitter_token:
            account.twitter_token = api.oauth_token
            account.save()

        account.touch_s()

        self.session["username"] = account.username
        self.session["email"] = account.email
        self.session["type"] = account.type_s()
        self.session["tokens"] = account.tokens()

        return account

    def ensure_twitter_api(self, state = None):
        oauth_token = self.session.get("tw.oauth_token", None)
        oauth_token_secret = self.session.get("tw.oauth_token_secret", None)
        if oauth_token: return
        if oauth_token_secret: return
        api = self.get_twitter_api()
        url = api.oauth_authorize(state = state)
        self.session["tw.oauth_token"] = api.oauth_token
        self.session["tw.oauth_token_secret"] = api.oauth_token_secret
        return url

    def get_twitter_api(self):
        import twitter
        redirect_url = self.url_for("admin.oauth_twitter", absolute = True)
        oauth_token = self.session and self.session.get("tw.oauth_token", None)
        oauth_token_secret = self.session and self.session.get("tw.oauth_token_secret", None)
        return twitter.Api(
            client_key = appier.conf("TWITTER_KEY"),
            client_secret = appier.conf("TWITTER_SECRET"),
            redirect_url = redirect_url,
            oauth_token = oauth_token,
            oauth_token_secret = oauth_token_secret
        )
