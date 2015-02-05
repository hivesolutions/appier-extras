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

import time

import appier

from appier_extras.parts.admin import models
from appier_extras.parts.admin import social

class AdminPart(
    appier.Part,
    social.Facebook,
    social.Twitter,
    social.Google,
    social.Github,
    social.Live
):
    """
    Modular part class providing the automation functionality for
    the generation of a web interface based on the application
    data model for fast prototyping.

    The interface configuration should be done by the way of
    "annotations" in the data model attributes.
    """

    def __init__(self, account_c = models.Account, *args, **kwargs):
        appier.Part.__init__(self, *args, **kwargs)
        self.account_c = account_c

    def load(self):
        appier.Part.load(self)

        self.logger.debug("Updating pre-defined application routes ...")
        self.owner.login_route = "admin.login"
        self.owner.login_redirect = "admin.index"

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
            (("GET",), "/admin/models/<str:model>.json", self.show_model_json, None, True),
            (("GET",), "/admin/models/<str:model>.csv", self.show_model_csv),
            (("GET",), "/admin/models/<str:model>", self.show_model),
            (("GET",), "/admin/models/<str:model>/new", self.new_entity),
            (("POST",), "/admin/models/<str:model>", self.create_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>.json", self.show_entity_json, None, True),
            (("GET",), "/admin/models/<str:model>/<str:_id>", self.show_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>/edit", self.edit_entity),
            (("POST",), "/admin/models/<str:model>/<str:_id>/edit", self.update_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>/delete", self.delete_entity),
            (("GET",), "/admin/facebook", self.facebook),
            (("GET",), "/admin/facebook/oauth", self.oauth_facebook),
            (("GET",), "/admin/twitter", self.twitter),
            (("GET",), "/admin/twitter/oauth", self.oauth_twitter),
            (("GET",), "/admin/google", self.google),
            (("GET",), "/admin/google/oauth", self.oauth_google),
            (("GET",), "/admin/github", self.github),
            (("GET",), "/admin/github/oauth", self.oauth_github),
            (("GET",), "/admin/live", self.live),
            (("GET",), "/admin/live/oauth", self.oauth_live),
            (("GET",), "/admin/log.json", self.show_log, None, True),
            (("GET",), "/api/admin/ping", self.ping_api, None, True),
            (("GET", "POST"), "/api/admin/login", self.login_api, None, True),
            (("GET",), "/api/admin/models/<str:model>", self.show_model_json, None, True),
            (("GET",), "/api/admin/models/<str:model>/<str:_id>", self.show_entity_json, None, True)
        ]

    def models(self):
        return models

    def template(self, template, layout = "fluid", *args, **kwargs):
        template = "%s/%s" % (layout, template)
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
        socials = self.socials()
        return self.template(
            "signin.html.tpl",
            next = next,
            socials = socials
        )

    def login(self):
        # retrieves the various fields that are going to be
        # used for the validation of the user under the current
        # authentication/authorization process
        username = self.field("username")
        password = self.field("password")
        next = self.field("next")
        socials = self.socials()
        try: account = self.account_c.login(username, password)
        except appier.AppierException as error:
            return self.template(
                "signin.html.tpl",
                next = next,
                socials = socials,
                username = username,
                error = error.message
            )

        # updates the current session with the proper
        # values to correctly authenticate the user
        self.session["username"] = account.username
        self.session["email"] = account.email
        self.session["type"] = account.type_s()
        self.session["tokens"] = account.tokens()

        # redirects the current operation to the next url or in
        # alternative to the root index of the administration
        return self.redirect(
            next or self.url_for(self.owner.login_redirect)
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
        if "tw.oauth_temporary" in self.session: del self.session["tw.oauth_temporary"]
        if "gg.access_token" in self.session: del self.session["gg.access_token"]
        if "gh.access_token" in self.session: del self.session["gh.access_token"]
        if "live.access_token" in self.session: del self.session["live.access_token"]

        # runs the proper redirect operation, taking into account if the
        # next value has been provided or not
        return self.redirect(
            next or self.url_for(self.owner.login_redirect)
        )

    def recover(self):
        return self.template("recover.html.tpl")

    def recover_do(self):
        identifier = self.field("identifier")
        try: self.account_c.recover(identifier)
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
        account = self.account_c.new()
        account.type = self.account_c.USER_TYPE
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
            labels = self._labels(),
            errors = dict()
        )

    @appier.ensure(token = "admin")
    def options_action(self):
        layout = self.field("layout")
        theme = self.field("theme")
        libs = self.field("libs")
        layout_s = layout.split("-", 1)
        theme_s = theme.split("-", 1)
        layout_l = len(layout_s)
        theme_l = len(theme_s)

        if layout_l == 1: layout_s.append("")
        layout_s, sub_layout_s = layout_s

        if theme_l == 1: theme_s.append("")
        theme_s, style_s = theme_s

        layout_s = layout_s.lower().strip()
        sub_layout_s = sub_layout_s.lower().strip()
        theme_s = theme_s.lower().strip()
        style_s = style_s.lower().strip()
        libs_s = libs.lower().strip()

        self.session["layout"] = layout_s
        self.session["sub_layout"] = sub_layout_s
        self.session["theme"] = theme_s
        self.session["style"] = style_s
        self.session["libs"] = libs_s
        self.session.permanent = True

        return self.template(
            "options.html.tpl",
            section = "options",
            labels = self._labels(),
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
    def show_model_json(self, model):
        meta = self.field("meta", False, cast = bool)
        model = self.get_model(model)
        object = appier.get_object(alias = True, find = True)
        entities = model.find(meta = meta, map = True, **object)
        return entities

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
    def show_entity_json(self, model, _id):
        rules = self.field("rules", False, cast = bool)
        meta = self.field("meta", False, cast = bool)
        model = self.get_model(model)
        entity = model.get(
            rules = rules,
            meta = meta,
            map = True,
            _id = appier.object_id(_id)
        )
        return entity

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

    @appier.ensure(token = "admin")
    def delete_entity(self, model, _id):
        model = self.get_model(model)
        entity = model.get(_id = appier.object_id(_id))
        entity.delete()
        return self.redirect(
            self.url_for(
                "admin.show_model",
                model = model._name()
            )
        )

    def facebook(self):
        next = self.field("next")
        url = self.ensure_facebook_api(state = next)
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for(self.owner.login_redirect)
        )

    def oauth_facebook(self):
        code = self.field("code")
        next = self.field("state")
        api = self.get_facebook_api()
        access_token = api.oauth_access(code)
        self.session["fb.access_token"] = access_token
        self.ensure_facebook_account()
        return self.redirect(
           next or self.url_for(self.owner.login_redirect)
        )

    def twitter(self):
        next = self.field("next")
        url = self.ensure_twitter_api(state = next)
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for(self.owner.login_redirect)
        )

    def oauth_twitter(self):
        oauth_verifier = self.field("oauth_verifier")
        next = self.field("state")
        api = self.get_twitter_api()
        oauth_token, oauth_token_secret = api.oauth_access(oauth_verifier)
        self.session["tw.oauth_token"] = oauth_token
        self.session["tw.oauth_token_secret"] = oauth_token_secret
        self.session["tw.oauth_temporary"] = False
        self.ensure_twitter_account()
        return self.redirect(
           next or self.url_for(self.owner.login_redirect)
        )

    def google(self):
        next = self.field("next")
        url = self.ensure_google_api(state = next)
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for(self.owner.login_redirect)
        )

    def oauth_google(self):
        code = self.field("code")
        next = self.field("state")
        api = self.get_google_api()
        access_token = api.oauth_access(code)
        self.session["gg.access_token"] = access_token
        self.ensure_google_account()
        return self.redirect(
           next or self.url_for(self.owner.login_redirect)
        )

    def github(self):
        next = self.field("next")
        url = self.ensure_github_api(state = next)
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for(self.owner.login_redirect)
        )

    def oauth_github(self):
        code = self.field("code")
        next = self.field("state")
        api = self.get_github_api()
        access_token = api.oauth_access(code)
        self.session["gh.access_token"] = access_token
        self.ensure_github_account()
        return self.redirect(
           next or self.url_for(self.owner.login_redirect)
        )

    def live(self):
        next = self.field("next")
        url = self.ensure_live_api(state = next)
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for(self.owner.login_redirect)
        )

    def oauth_live(self):
        code = self.field("code")
        next = self.field("state")
        api = self.get_live_api()
        access_token = api.oauth_access(code)
        self.session["live.access_token"] = access_token
        self.ensure_live_account()
        return self.redirect(
           next or self.url_for(self.owner.login_redirect)
        )

    @appier.ensure(token = "admin")
    def show_log(self):
        memory_handler = self.owner.handler_memory
        count = self.field("count", 100, cast = int)
        level = self.field("level", None)
        return dict(
            messages = memory_handler.get_latest(count = count, level = level)
        )

    def ping_api(self):
        return dict(time = time.time())

    def login_api(self):
        # retrieves the various fields that are going to be
        # used for the validation of the user under the current
        # authentication/authorization process
        username = self.field("username")
        password = self.field("password")
        account = self.account_c.login(username, password)

        # updates the current session with the proper
        # values to correctly authenticate the user
        self.session["username"] = account.username
        self.session["email"] = account.email
        self.session["type"] = account.type_s()
        self.session["tokens"] = account.tokens()

        # retrieves the session identifier (sid) for the currently
        # assigned session, this is going to be used in the next
        # requests to refer to the proper session
        sid = self.session.sid

        # redirects the current operation to the next url or in
        # alternative to the root index of the administration
        return dict(
            sid = sid,
            session_id = sid,
            username = username,
            tokens = account.tokens()
        )

    def socials(self):
        socials = []
        if self.has_facebook(): socials.append("facebook")
        if self.has_twitter(): socials.append("twitter")
        if self.has_google(): socials.append("google")
        if self.has_github(): socials.append("github")
        if self.has_live(): socials.append("live")
        return socials

    def _hybrid(self, name, default = None):
        if name in self.session: return self.session[name]
        if hasattr(self, name): return getattr(self, name)
        if hasattr(self.owner, name): return getattr(self.owner, name)
        return default

    def _labels(self):
        layout = self._hybrid("layout")
        sub_layout = self._hybrid("sub_layout")
        theme = self._hybrid("theme")
        style = self._hybrid("style")
        libs = self._hybrid("libs")

        layout_label = str()
        label = str()
        libs_label = str()

        if layout: layout_label += layout.capitalize()
        if sub_layout: layout_label += " - " + sub_layout.capitalize()

        if theme: label += theme.capitalize()
        if style: label += " - " + style.capitalize()

        if libs: libs_label += libs.capitalize()

        return dict(
            layout_label = layout_label,
            label = label,
            libs_label = libs_label
        )
