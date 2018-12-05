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

import os
import json
import time
import datetime
import tempfile

import appier

from appier_extras import base
from appier_extras import utils
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

    def __init__(
        self,
        account_c = models.Account,
        role_c = models.Role,
        *args,
        **kwargs
    ):
        appier.Part.__init__(self, *args, **kwargs)
        self.account_c = account_c
        self.role_c = role_c
        self.layout = kwargs.get("layout", "fluid")
        self.theme = kwargs.get("theme", "flat")
        self.style = kwargs.get("style", "")
        self.libs = kwargs.get("libs", "current")
        self.social_libs = kwargs.get("libs", [])
        self.available = kwargs.get("available", True)
        self.open = kwargs.get("open", False)
        self.oauth = kwargs.get("oauth", True)
        self.avatar_default = kwargs.get("avatar_default", False)
        self.layout = appier.conf("ADMIN_LAYOUT", self.layout)
        self.theme = appier.conf("ADMIN_THEME", self.theme)
        self.style = appier.conf("ADMIN_STYLE", self.style)
        self.libs = appier.conf("ADMIN_LIBS", self.libs)
        self.social_libs = appier.conf("ADMIN_SOCIAL_LIBS", self.social_libs, cast = list)
        self.available = appier.conf("ADMIN_AVAILABLE", self.available, cast = bool)
        self.open = appier.conf("ADMIN_OPEN", self.open, cast = bool)
        self.oauth = appier.conf("ADMIN_OAUTH", self.oauth, cast = bool)
        self.avatar_default = appier.conf(
            "ADMIN_AVATAR_DEFAULT",
            self.avatar_default,
            cast = bool
        )

        self._last_login = None
        self._login_count = 0
        self._sections = appier.OrderedDict()
        self._operations = appier.OrderedDict()

    def version(self):
        return base.VERSION

    def info(self):
        info = appier.Part.info(self)
        info.update(
            last_login = self._last_login_s,
            login_count = self._login_count
        )
        return info

    def load(self):
        appier.Part.load(self)

        self.logger.debug("Registering pre request handler ...")
        appier.App.add_custom("before_request", self.before_request)
        appier.App.add_exception(
            BaseException,
            self.exception_handler,
            scope = AdminPart
        )

        self.logger.debug("Updating pre-defined application routes ...")
        self.owner.login_route = "admin.login"
        self.owner.login_route_admin = "admin.login"
        self.owner.login_redirect = "admin.index"
        self.owner.logout_redirect = "admin.login"
        self.owner.admin_account = self.account_c
        self.owner.admin_role = self.role_c
        self.owner.admin_login_redirect = "admin.index"
        self.owner.admin_logout_redirect = "admin.login"
        self.owner.admin_facebook_scope = ("email",)
        self.owner.admin_github_scope = ("user:email",)
        self.owner.admin_google_scope = ("email",)
        self.owner.admin_live_scope = ("wl.basic", "wl.emails")

        self.owner.admin_available = self.available
        self.owner.admin_open = self.open
        self.owner.admin_oauth = self.oauth
        self.owner.admin_avatar_default = self.avatar_default

        self.owner.lib_loaders["appier_extras"] = self._appier_extras_loader
        self.owner.lib_loaders["netius"] = self._netius_loader
        self.owner.lib_loaders["pconvert"] = self._pconvert_loader
        self.owner.lib_loaders["PIL"] = self._pil_loader
        self.owner.lib_loaders["pymongo"] = self._pymongo_loader
        self.owner.lib_loaders["redis"] = self._redis_loader
        self.owner.lib_loaders["jinja2"] = self._jinja2_loader
        self.owner.lib_loaders["ssl"] = self._ssl_loader

        self.owner.add_filter(self.markdown_jinja, "markdown")

        if self.owner.allow_headers: self.owner.allow_headers += ", X-Secret-Key"

        self.logger.debug("Generating admin interfaces ...")
        for model_c in self.models_r:
            if not model_c.is_attached(): continue
            if not model_c.is_concrete(): continue
            if not model_c.is_child(models.Base): continue
            self.logger.debug(model_c)

        for social_lib in self.social_libs:
            method = getattr(self, "ensure_" + social_lib)
            method()

        self.load_settings()
        self.load_operations()

        self.account_c.bind_g("touch_login", self._on_touch_login)

    def unload(self):
        appier.Part.unload(self)

        self.account_c.unbind_g("touch_login", self._on_touch_login)

        self.unload_operations()
        self.unload_settings()

        self.owner.remove_filter("markdown")

    def routes(self):
        return [
            (("GET",), "/admin", self.index),
            (("GET",), "/admin/signin", self.signin),
            (("POST",), "/admin/signin", self.login),
            (("GET", "POST"), "/admin/signout", self.logout),
            (("GET"), "/admin/confirm", self.confirm),
            (("GET"), "/admin/recover", self.recover),
            (("POST"), "/admin/recover", self.recover_do),
            (("GET"), "/admin/reset", self.reset),
            (("POST"), "/admin/reset", self.reset_do),
            (("GET",), "/admin/options", self.options),
            (("POST",), "/admin/options", self.options_action),
            (("GET",), "/admin/social", self.social),
            (("GET",), "/admin/operations", self.operations),
            (("GET",), "/admin/status", self.status),
            (("GET",), "/admin/routes", self.list_routes),
            (("GET",), "/admin/configs", self.list_configs),
            (("GET",), "/admin/parts", self.list_parts),
            (("GET",), "/admin/parts/<str:name>", self.show_part),
            (("GET",), "/admin/parts/<str:name>/load", self.load_part),
            (("GET",), "/admin/parts/<str:name>/unload", self.unload_part),
            (("GET",), "/admin/libraries", self.list_libraries),
            (("GET",), "/admin/oauth/authorize", self.oauth_authorize),
            (("POST",), "/admin/oauth/authorize", self.do_oauth_authorize),
            (("GET",), "/admin/oauth/deny", self.oauth_deny),
            (("GET", "POST"), "/admin/oauth/access_token", self.oauth_access_token, None, True),
            (("GET", "POST"), "/admin/oauth/login", self.oauth_login, None, True),
            (("GET",), "/admin/operations/build_index", self.build_index),
            (("GET",), "/admin/operations/build_index_db", self.build_index_db),
            (("GET",), "/admin/operations/test_email", self.test_email),
            (("GET",), "/admin/operations/test_event", self.test_event),
            (("GET",), "/admin/sessions", self.list_sessions),
            (("GET",), "/admin/sessions/empty", self.empty_sessions),
            (("GET",), "/admin/sessions/me", self.show_session_me),
            (("GET",), "/admin/sessions/me/delete", self.delete_session_me),
            (("GET",), "/admin/sessions/<str:sid>", self.show_session),
            (("GET",), "/admin/sessions/<str:sid>/delete", self.delete_session),
            (("GET",), "/admin/peers", self.list_peers),
            (("GET",), "/admin/counters", self.list_counters),
            (("GET",), "/admin/events.csv", self.list_events_csv),
            (("GET",), "/admin/locales/<int:id>/bundle.json", self.bundle_locale_json, None, True),
            (("GET",), "/admin/database", self.database),
            (("GET",), "/admin/database/export", self.database_export),
            (("GET",), "/admin/database/import", self.database_import),
            (("POST",), "/admin/database/import", self.database_import_do),
            (("GET",), "/admin/database/reset", self.database_reset),
            (("GET",), "/admin/search", self.search),
            (("GET",), "/admin/accounts/new", self.new_account),
            (("POST",), "/admin/accounts", self.create_account),
            (("GET",), "/admin/accounts/me", self.me_account),
            (("GET",), "/admin/accounts/<str:username>", self.show_account),
            (("GET",), "/admin/accounts/<str:username>/mail", self.mail_account),
            (("GET",), "/admin/accounts/<str:username>/avatar", self.avatar_account),
            (("GET",), "/admin/models", self.list_models),
            (("GET",), "/admin/models/<str:model>.json", self.show_model_json, None, True),
            (("GET",), "/admin/models/<str:model>.csv", self.show_model_csv),
            (("GET",), "/admin/models/<str:model>", self.show_model),
            (("GET", "POST"), "/admin/models/<str:model>/links/<str:link>", self.link_model),
            (("GET", "POST"), "/admin/models/<str:model>/operations/<str:operation>", self.operation_model),
            (("GET", "POST"), "/admin/models/<str:model>/view/<str:view>", self.view_model),
            (("GET",), "/admin/models/<str:model>/new", self.new_entity),
            (("POST",), "/admin/models/<str:model>", self.create_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>.json", self.show_entity_json, None, True),
            (("GET",), "/admin/models/<str:model>/<str:_id>", self.show_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>/edit", self.edit_entity),
            (("POST",), "/admin/models/<str:model>/<str:_id>/edit", self.update_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>/delete", self.delete_entity),
            (("GET",), "/admin/facebook", self.facebook),
            (("GET",), "/admin/facebook/unlink", self.unlink_facebook),
            (("GET",), "/admin/facebook/unset", self.unset_facebook),
            (("GET",), "/admin/facebook/oauth", self.oauth_facebook),
            (("GET",), "/admin/github", self.github),
            (("GET",), "/admin/github/unlink", self.unlink_github),
            (("GET",), "/admin/github/unset", self.unset_github),
            (("GET",), "/admin/github/oauth", self.oauth_github),
            (("GET",), "/admin/google", self.google),
            (("GET",), "/admin/google/unlink", self.unlink_google),
            (("GET",), "/admin/google/unset", self.unset_google),
            (("GET",), "/admin/google/oauth", self.oauth_google),
            (("GET",), "/admin/live", self.live),
            (("GET",), "/admin/live/unlink", self.unlink_live),
            (("GET",), "/admin/live/unset", self.unset_live),
            (("GET",), "/admin/live/oauth", self.oauth_live),
            (("GET",), "/admin/twitter", self.twitter),
            (("GET",), "/admin/twitter/unlink", self.unlink_twitter),
            (("GET",), "/admin/twitter/unset", self.unset_twitter),
            (("GET",), "/admin/twitter/oauth", self.oauth_twitter),
            (("GET",), "/admin/log.json", self.show_log, None, True),
            (("GET",), "/admin/configs.json", self.show_configs, None, True),
            (("GET",), "/api/admin/ping", self.ping_api, None, True),
            (("GET", "POST"), "/api/admin/login", self.login_api, None, True),
            (("GET", "POST"), "/api/admin/oauth/access_token", self.oauth_access_token_api, None, True),
            (("GET", "POST"), "/api/admin/oauth/login", self.oauth_login_api, None, True),
            (("GET",), "/api/admin/accounts/me", self.me_account_api, None, True),
            (("GET",), "/api/admin/models/<str:model>", self.show_model_json, None, True),
            (("GET",), "/api/admin/models/<str:model>/<str:_id>", self.show_entity_json, None, True)
        ]

    def models(self):
        if not self.available: return None
        return models

    def template(self, template, layout = None, *args, **kwargs):
        layout = self.session.get("layout", self.layout)
        template = "%s/%s" % (layout, template)
        return appier.Part.template(
            self,
            template,
            *args,
            **kwargs
        )

    def before_request(self):
        key = self.field("skey", None)
        key = self.field("secret_key", key)
        key = self.request.get_header("X-Secret-Key", key)
        if not key: return
        try: account = self.account_c.login_key(key)
        except appier.OperationalError: pass
        else: account._set_session(method = "set_t")

    def exception_handler(self, error):
        import traceback
        lines = traceback.format_exc().splitlines()
        lines = appier.App._lines(lines)
        lines = lines if self.owner.is_devel() else []
        return self.template(
            "error.html.tpl",
            error = error,
            lines = lines
        )

    def load_settings(self):
        settings = self.owner.get_preference(self.name() + ":settings")
        if not settings: return
        for name in self.settings_l:
            current = getattr(self, name)
            value = settings.get(name, current)
            setattr(self, name, value)

    def unload_settings(self):
        settings = self.owner.get_preference(self.name() + ":settings")
        if not settings: return
        for name in self.settings_l:
            delattr(self, name)

    def dump_settings(self):
        settings = dict()
        for name in self.settings_l:
            value = getattr(self, name)
            settings[name] = value
        self.owner.set_preference(self.name() + ":settings", settings)

    def flush_settings(self):
        self.dump_settings()

    def load_operations(self):
        self.add_operation(
            "build_index", "admin.build_index",
            description = "Build search index",
            message = "Are you really sure you want to re-build the search index?",
            note = "Re-building the complete search index, may take some time",
            level = 3
        )
        self.add_operation(
            "build_index_db", "admin.build_index_db",
            description = "Build database index",
            message = "Are you really sure you want to re-build the database index?",
            note = "Re-building the complete database index, may take some time",
            level = 3
        )
        self.add_operation(
            "test_email", "admin.test_email",
            description = "Send test email",
            note = "Sending this email is going to use loaded SMTP configuration"
        )
        self.add_operation(
            "test_event", "admin.test_event",
            description = "Trigger test event",
            note = "All handlers for the event are going to be triggered"
        )

    def unload_operations(self):
        self.remove_operation("build_index")
        self.remove_operation("build_index_db")
        self.remove_operation("test_email")
        self.remove_operation("test_event")

    def add_section(self, name):
        self._sections[name] = appier.OrderedDict()

    def remove_section(self, name):
        del self._sections[name]

    def add_section_item(self, name, route, section = None):
        if not section in self._sections:
            self.add_section(section)
        self._sections[section][name] = route

    def remove_section_item(self, name, section = None):
        del self._sections[section][name]
        if self._sections[section]: return
        del self._sections[section]

    def add_operation(
        self,
        name,
        route,
        description = None,
        message = None,
        note = None,
        level = 1,
        args = [],
        kwargs = {}
    ):
        self._operations[name] = dict(
            name = name,
            route = route,
            description = description,
            message = message,
            note = note,
            level = level,
            args = args,
            kwargs = kwargs
        )

    def remove_operation(self, name):
        del self._operations[name]

    def index(self):
        return self.list_models()

    def signin(self):
        next = self.field("next")
        error = self.field("error")
        socials = self.socials()
        return self.template(
            "signin.html.tpl",
            next = next,
            error = error,
            socials = socials
        )

    def login(self):
        # verifies if the current administration interface is
        # available and if that's not the cases raises an error
        if not self.owner.admin_available: raise appier.SecurityError(
            message = "Administration not available"
        )

        # retrieves the various fields that are going to be
        # used for the validation of the user under the current
        # authentication/authorization process
        username = self.field("username", mandatory = True)
        password = self.field("password", mandatory = True)
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
        account._set_session()

        # redirects the current operation to the next URL or in
        # alternative to the root index of the administration
        return self.redirect(
            next or self.url_for(self.owner.admin_login_redirect)
        )

    def logout(self):
        # tries to retrieve the next field as it's going to be used for
        # the redirection operation at the end of the logout operation
        next = self.field("next")

        # verifies the existence of the various account related session
        # attributes and in case they exist removes them from session as
        # the user is currently logging out from session
        self.account_c._unset_account()

        # runs the proper redirect operation, taking into account if the
        # next value has been provided or not
        return self.redirect(
            next or self.url_for(self.owner.admin_logout_redirect)
        )

    def recover(self):
        return self.template("recover.html.tpl")

    def recover_do(self):
        identifier = self.field("identifier")
        send_email = self.field("send_email", True, cast = bool)
        try: self.account_c.recover(identifier, send_email = send_email)
        except appier.AppierException as error:
            return self.template(
                "recover.html.tpl",
                identifier = identifier,
                error = error.message
            )

        return self.template("done.html.tpl")

    def reset(self):
        next = self.field("next")
        reset_token = self.field(
            "reset_token",
            mandatory = True,
            not_empty = True
        )
        self.account_c.validate_reset(reset_token)
        return self.template(
            "reset.html.tpl",
            next = next,
            reset_token = reset_token
        )

    def reset_do(self):
        next = self.field("next")
        reset_token = self.field(
            "reset_token",
            mandatory = True,
            not_empty = True
        )
        password = self.field(
            "password",
            mandatory = True
        )
        password_confirm = self.field(
            "password_confirm",
            mandatory = True
        )
        try: self.account_c.reset(reset_token, password, password_confirm)
        except appier.AppierException as error:
            return self.template(
                "reset.html.tpl",
                next = next,
                reset_token = reset_token,
                password = password,
                password_confirm = password_confirm,
                error = error.message
            )

        return self.redirect(
            next or self.url_for(self.login_route_admin)
        )

    def confirm(self):
        next = self.field("next")
        confirmation_token = self.field(
            "confirmation_token",
            mandatory = True,
            not_empty = True
        )
        send_email = self.field("send_email", True, cast = bool)
        self.account_c.confirm(confirmation_token, send_email = send_email)
        return self.redirect(
            next or self.url_for(self.login_route_admin)
        )

    def new_account(self):
        if not self.owner.admin_available: raise appier.SecurityError(
            message = "Administration not available"
        )
        if not self.owner.admin_open: raise appier.SecurityError(
            message = "Signup not allowed"
        )
        return self.template(
            "account/new.html.tpl",
            account = dict(),
            errors = dict()
        )

    def create_account(self):
        if not self.owner.admin_available: raise appier.SecurityError(
            message = "Administration not available"
        )
        if not self.owner.admin_open: raise appier.SecurityError(
            message = "Signup not allowed"
        )
        account = self.account_c.new()
        account.type = self.account_c.USER_TYPE
        account.enabled = False
        try: account.save()
        except appier.ValidationError as error:
            return self.template(
                "account/new.html.tpl",
                error = "Problems occurred creating account",
                account = error.model,
                errors = error.errors
            )

        return self.redirect(
            self.url_for(
                "admin.mail_account",
                username = account.username
            )
        )

    @appier.ensure(context = "admin")
    def me_account(self):
        account_c = self._get_cls(self.account_c)
        account = account_c.from_session(meta = True)
        return self.template(
            "account/show.html.tpl",
            account = account
        )

    @appier.ensure(token = "admin.accounts", context = "admin")
    def show_account(self, username):
        account_c = self._get_cls(self.account_c)
        account = account_c.get(
            username = username,
            meta = True
        )
        return self.template(
            "account/show.html.tpl",
            account = account
        )

    @appier.ensure(token = "admin.accounts", context = "admin")
    def mail_account(self, username):
        raise appier.NotImplementedError()

    def avatar_account(self, username):
        strict = self.field("strict", False, cast = bool)
        cache = self.field("cache", False, cast = bool)
        account_c = self._get_cls(self.account_c)
        account = account_c.get(
            username = username,
            rules = False
        )
        return account._send_avatar(
            strict = strict,
            cache = cache
        )

    @appier.ensure(token = "admin.options", context = "admin")
    def options(self):
        return self.template(
            "options.html.tpl",
            section = "options",
            labels = self._labels(),
            errors = dict()
        )

    @appier.ensure(token = "admin.options", context = "admin")
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

    @appier.ensure(token = "admin.social", context = "admin")
    def social(self):
        socials = self.socials()
        linked = self.linked()
        return self.template(
            "social.html.tpl",
            section = "social",
            socials = socials,
            linked = linked
        )

    @appier.ensure(token = "admin.operations", context = "admin")
    def operations(self):
        return self.template(
            "operations.html.tpl",
            section = "operations"
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def status(self):
        return self.template(
            "status.html.tpl",
            section = "status"
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def list_routes(self):
        return self.template(
            "routes.html.tpl",
            section = "status",
            routes = self._routes()
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def list_configs(self):
        configs = appier.config.CONFIGS
        configs = appier.legacy.items(configs)
        configs.sort()
        return self.template(
            "configs.html.tpl",
            section = "status",
            configs = configs
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def list_parts(self):
        parts = self.owner.get_parts()
        return self.template(
            "parts.html.tpl",
            section = "status",
            parts = parts
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def show_part(self, name):
        part = self.owner.get_part(name)
        info = part.info()
        info_l = appier.legacy.keys(info)
        info_l.sort()
        return self.template(
            "part.html.tpl",
            section = "status",
            part = part,
            info = info,
            info_l = info_l
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def load_part(self, name):
        part = self.owner.get_part(name)
        self.owner._load_part(part)
        return self.redirect(
            self.url_for(
                "admin.show_part",
                name = name,
                message = "Part %s has been loaded" % name
            )
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def unload_part(self, name):
        part = self.owner.get_part(name)
        self.owner._unload_part(part)
        return self.redirect(
            self.url_for(
                "admin.show_part",
                name = name,
                message = "Part %s has been unloaded" % name
            )
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def list_libraries(self):
        libraries = self.owner.get_libraries()
        return self.template(
            "libraries.html.tpl",
            section = "status",
            libraries = libraries
        )

    @appier.ensure(context = "admin")
    def oauth_authorize(self):
        # verifies if the oauth system is allowed if that's not
        # the case raises an exception indicating so
        if not self.owner.admin_oauth: raise appier.SecurityError(
            message = "OAuth not allowed"
        )

        # retrieves the complete set of fields that are going
        # to be used on the initial authorize state of oauth
        client_id = self.field("client_id", mandatory = True)
        redirect_uri = self.field("redirect_uri", mandatory = True)
        scope = self.field("scope", mandatory = True)
        response_type = self.field("response_type", "code")
        state = self.field("state", None)

        # verifies/ensures that the response type to be received
        # is the code, as that's the only one supported
        appier.verify("response_type", "code")

        # normalizes the scope value to the list representation
        # and then sorts it in the normal manner (normalization)
        scope_l = scope.split(" ")
        scope_l.sort()

        # runs the mandatory retrieval of the oauth client associated
        # with the provided client id
        oauth_client = models.OAuthClient.get_e(
            client_id = client_id,
            redirect_uri = redirect_uri
        )

        # tries to re-use an already authorized token that is considered
        # equivalent to the current one, if the re-usage operation is a
        # success then redirects the user agent immediately
        result, tokens, oauth_token = models.OAuthToken.reuse_s(
            redirect_uri, scope_l, oauth_client
        )
        if result: return self.redirect(
            redirect_uri,
            params = dict(
                code = oauth_token.authorization_code,
                scope = " ".join(oauth_token.tokens),
                tokens = oauth_token.tokens,
            )
        )

        # runs the template rendering for the oauth authorize panel
        # it should prompt the final user for permission agreement
        return self.template(
            "oauth/authorize.html.tpl",
            client_id = client_id,
            redirect_uri = redirect_uri,
            scope = scope,
            response_type = response_type,
            state = state,
            oauth_client = oauth_client,
            tokens = tokens
        )

    @appier.ensure(context = "admin")
    def do_oauth_authorize(self):
        if not self.owner.admin_oauth: raise appier.SecurityError(
            message = "OAuth not allowed"
        )

        client_id = self.field("client_id", mandatory = True)
        redirect_uri = self.field("redirect_uri", mandatory = True)
        scope = self.field("scope", mandatory = True)
        state = self.field("state", mandatory = True)

        scope_l = scope.split(" ")
        scope_l.sort()

        account = self.account_c.from_session()
        oauth_client = models.OAuthClient.get_e(
            client_id = client_id,
            redirect_uri = redirect_uri
        )
        oauth_token = oauth_client.build_token_s(
            username = account.username,
            scope = scope_l
        )

        return self.redirect(
            redirect_uri,
            params = dict(
                code = oauth_token.authorization_code,
                scope = " ".join(oauth_token.tokens),
                state = state,
            )
        )

    @appier.ensure(context = "admin")
    def oauth_deny(self):
        if not self.owner.admin_oauth: raise appier.SecurityError(
            message = "OAuth not allowed"
        )
        redirect_uri = self.field("redirect_uri", mandatory = True)
        return self.redirect(
            redirect_uri,
            params = dict(
                error = "access_denied",
                error_description = "Permissions error"
            )
        )

    def oauth_access_token(self):
        # verifies if the oauth system is allowed if that's not
        # the case raises an exception indicating so
        if not self.owner.admin_oauth: raise appier.SecurityError(
            message = "OAuth not allowed"
        )

        # retrieve the multiple fields that are going to be used for the
        # process of issuing the access token (only authorization code is
        # going to be returned to the client)
        client_id = self.field("client_id", mandatory = True)
        client_secret = self.field("client_secret", mandatory = True)
        redirect_uri = self.field("redirect_uri", mandatory = True)
        code = self.field("code", mandatory = True)
        grant_type = self.field("grant_type", "authorization_code")

        # tries to retrieve the oauth client associated with the
        # provided client id and secret and then uses the value to
        # retrieve the associated oauth token via association
        oauth_client = models.OAuthClient.get_e(
            client_id = client_id,
            client_secret = client_secret,
            redirect_uri = redirect_uri
        )
        oauth_token = models.OAuthToken.get_e(
            authorization_code = code,
            client = oauth_client.id,
            rules = False
        )

        # verifies that the authorization code is the expected
        # one and then unsets it from the oauth token, so that
        # it's no longer going to be used
        oauth_token.verify_code(code, grant_type = grant_type)
        oauth_token.unset_code_s()

        # returns the final map based response containing the complete
        # set of elements to the client to be used, notice that both
        # the scope and the tokens are also returned so that the OAuth
        # client is able to modify experience taking that into account
        return dict(
            access_token = oauth_token.access_token,
            token_type = "bearer",
            expires_in = oauth_token.expires_in,
            refresh_token = oauth_token.refresh_token,
            scope = oauth_token.scope,
            tokens = oauth_token.tokens
        )

    def oauth_login(self):
        # verifies if the current administration interface is
        # available and if that's not the cases raises an error
        if not self.owner.admin_available: raise appier.SecurityError(
            message = "Administration not available"
        )

        # verifies if the oauth system is allowed if that's not
        # the case raises an exception indicating so
        if not self.owner.admin_oauth: raise appier.SecurityError(
            message = "OAuth not allowed"
        )

        # retrieves the reference to the access token that has been
        # provided to the request and then uses it to retrieve the
        # token, note that an exception is raised if no access token
        # is provided (as expected)
        access_token = self.field("access_token", mandatory = True)
        oauth_token = models.OAuthToken.login(access_token)

        # updates the current session with the proper
        # values to correctly authenticate the user
        oauth_token._set_session()

        # retrieves the session identifier (SID) for the currently
        # assigned session, this is going to be used in the next
        # requests to refer to the proper session
        sid = self.session.sid

        # redirects the current operation to the next URL or in
        # alternative to the root index of the administration
        return dict(
            sid = sid,
            session_id = sid,
            username = oauth_token.username,
            tokens = oauth_token.tokens
        )

    @appier.ensure(token = "admin", context = "admin")
    def build_index(self):
        empty = self.field("empty", True, cast = bool)
        _async = self.field("async", True, cast = bool)

        def builder():
            if empty: models.Search.delete_c()
            for model in self._administrable(self.models_r):
                model.build_index_g()

        if _async: self.owner.delay(builder)
        else: builder()

        return self.redirect(
            self.url_for(
                "admin.operations",
                message = "Search index built with success"
            )
        )

    @appier.ensure(token = "admin", context = "admin")
    def build_index_db(self):
        for model in self._administrable(self.models_r):
            model._destroy_indexes()
            model._build_indexes()
        return self.redirect(
            self.url_for(
                "admin.operations",
                message = "Database index built with success"
            )
        )

    @appier.ensure(token = "admin", context = "admin")
    def test_email(self):
        receiver = appier.conf("TEST_EMAIL", None)
        receiver = self.field("email", receiver)
        receiver = self.field("receiver", receiver)
        if not receiver: raise appier.OperationalError(
            message = "No test email defined"
        )
        models.Base.send_email_g(
            self.owner,
            "admin/email/test.html.tpl",
            receivers = [receiver],
            subject = "Test email",
            title = "Test email"
        )
        return self.redirect(
            self.url_for(
                "admin.operations",
                message = "Test email sent"
            )
        )

    @appier.ensure(token = "admin", context = "admin")
    def test_event(self):
        name = appier.conf("TEST_EVENT", "test")
        name = self.field("event", name)
        name = self.field("name", name)
        models.Event.notify_g(name)
        return self.redirect(
            self.url_for(
                "admin.operations",
                message = "Test event triggered"
            )
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def list_sessions(self):
        return self.template(
            "sessions.html.tpl",
            section = "status",
            sessions = self.request.session_c.all()
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def empty_sessions(self):
        self.request.session_c.empty()
        return self.redirect(
            self.url_for(
                "admin.list_sessions",
                message = "Sessions emptied with success"
            )
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def show_session_me(self):
        sid = self.session.sid
        return self.template(
            "session.html.tpl",
            section = "status",
            session_s = self.request.session_c.get_s(sid)
        )

    def delete_session_me(self):
        sid = self.session.sid
        self.request.session_c.expire(sid)
        return self.redirect(
            self.url_for(
                "admin.list_sessions",
                message = "Session deleted with success"
            )
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def show_session(self, sid):
        sid = str(sid)
        return self.template(
            "session.html.tpl",
            section = "status",
            session_s = self.request.session_c.get_s(sid)
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def delete_session(self, sid):
        sid = str(sid)
        self.request.session_c.expire(sid)
        return self.redirect(
            self.url_for(
                "admin.list_sessions",
                message = "Session deleted with success"
            )
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def list_peers(self):
        peers = appier.legacy.items(self.owner._peers)
        peers.sort()
        return self.template(
            "peers.html.tpl",
            section = "status",
            peers = peers
        )

    @appier.ensure(token = "admin.status", context = "admin")
    def list_counters(self):
        collection = self._counters()
        counters = collection.find()
        return self.template(
            "counters.html.tpl",
            section = "status",
            counters = counters
        )

    @appier.ensure(token = "admin", context = "admin")
    def list_events_csv(self):
        object = appier.get_object(
            alias = True,
            find = True,
            limit = 0
        )
        events = models.Event.find(**object)

        events_s = [(
            "name",
            "handler",
            "arguments"
        )]
        for event in events:
            event_s = (
                event.name,
                event.handler,
                event.arguments and json.dumps(event.arguments)
            )
            events_s.append(event_s)

        result = appier.serialize_csv(events_s, delimiter = ",")
        self.content_type("text/csv")
        return result

    @appier.ensure(token = "admin", context = "admin")
    def bundle_locale_json(self, id):
        name = self.field("name", None)
        locale = models.Locale.get(id = id, rules = False)
        name = name or locale.context or "global"
        file_name = "%s.%s.json" % (name, locale.locale)
        self.content_disposition("filename=\"%s\"" % file_name) 
        return self.json(locale.data_j, sort_keys = True)

    @appier.ensure(token = "admin.database", context = "admin")
    def database(self):
        return self.template(
            "database.html.tpl",
            section = "database"
        )

    @appier.ensure(token = "admin.database", context = "admin")
    def database_export(self):
        adapter = self.get_adapter()
        file = appier.legacy.BytesIO()
        manager = appier.ExportManager(
            adapter,
            multiple = self.resolve()
        )
        manager.export_data(file)

        date_time = datetime.datetime.utcnow()
        date_time_s = date_time.strftime("%Y%m%d")
        file_name = "%s_%s.dat" % (self.owner.name, date_time_s)

        self.content_type("application/octet-stream")
        self.content_disposition("attachment; filename=\"%s\"" % file_name) 

        return file.getvalue()

    @appier.ensure(token = "admin.database", context = "admin")
    def database_import(self):
        return self.template(
            "database/import.html.tpl",
            section = "database"
        )

    @appier.ensure(token = "admin.database", context = "admin")
    def database_import_do(self):
        # tries to retrieve the reference to the import file tuple
        # and in case it's not found raises an error to the template
        import_file = self.field("import_file", None)
        if import_file == None:
            return self.template(
                "database/import.html.tpl",
                section = "database",
                error = "No file defined"
            )

        # creates a temporary file path for the storage of the file
        # and then saves it into that directory
        fd, file_path = tempfile.mkstemp()
        import_file.save(file_path)

        # retrieves the database and creates a new export manager for
        # the currently defined entities then imports the data defined
        # in the current temporary path
        adapter = self.get_adapter()
        manager = appier.ExportManager(
            adapter,
            multiple = self.resolve()
        )
        try: manager.import_data(file_path)
        finally: os.close(fd); os.remove(file_path)
        return self.redirect(
            self.url_for(
                "admin.database_import",
                message = "Database file imported with success"
            )
        )

    @appier.ensure(token = "admin.database", context = "admin")
    def database_reset(self):
        adapter = self.get_adapter()
        adapter.drop_db()
        return self.redirect(
            self.url_for(
                "admin.database",
                message = "Database dropped/reset with success"
            )
        )

    @appier.ensure(token = "admin", context = "admin")
    def search(self):
        object = appier.get_object(
            alias = True,
            find = True,
            find_i = True,
            find_t = "right"
        )
        indexes = models.Search.find(map = True, **object)
        return indexes

    @appier.ensure(token = "admin", context = "admin")
    def list_models(self):
        return self.template(
            "models/list.html.tpl",
            section = "admin"
        )

    @appier.ensure(token = "admin", context = "admin")
    def show_model(self, model):
        appier.ensure_login(self, token = "admin.models." + model)
        model = self.get_model(model, raise_e = True)
        model.assert_is_concrete_g()
        object = appier.get_object(
            alias = True,
            page = True,
            find = True
        )
        object = self._sort(object, model)
        page = model.paginate_v(**object)
        entities = model.find_v(meta = True, **object)
        return self.template(
            "models/show.html.tpl",
            section = "models",
            model = model,
            page = page,
            entities = entities
        )

    @appier.ensure(token = "admin", context = "admin")
    def show_model_json(self, model):
        appier.ensure_login(self, token = "admin.models." + model)
        eager_l = self.field("eager_l", False, cast = bool)
        meta = self.field("meta", False, cast = bool)
        model = self.get_model(model)
        object = appier.get_object(alias = True, find = True)
        entities = model.find_v(
            eager_l = eager_l,
            meta = meta,
            map = True,
            **object
        )
        return entities

    @appier.ensure(token = "admin", context = "admin")
    def show_model_csv(self, model):
        appier.ensure_login(self, token = "admin.models." + model)
        eager_l = self.field("eager_l", False, cast = bool)
        meta = self.field("meta", False, cast = bool)
        model = self.get_model(model)
        object = appier.get_object(alias = True, find = True)
        entities = model.find_v(
            eager_l = eager_l,
            meta = meta,
            map = True,
            **object
        )
        result = appier.serialize_csv(entities)
        self.content_type("text/csv")
        return result

    @appier.ensure(token = "admin", context = "admin")
    def link_model(self, model, link):
        # ensures that the proper token is available so that the
        # operation may be executed under the current context
        appier.ensure_login(self, token = "admin.models." + model)

        # retrieves the complete set of sequential parameters that
        # are going to be applied to the link operations
        parameters = self.get_fields("parameters", [])

        # retrieves the reference to the view that is going to be used
        # to filter the entities for which to generate the link (if any)
        view = self.field("view", None)

        # tries to get the context reference that is going to be "passed"
        # to the underlying link operation if required
        context = self.field("context", None)
        context = context.split(",") if context else None

        # retrieves the reference to the complete set of ids of entities
        # for which the link operation should be applied
        ids = self.field("ids", "")
        ids = ids.split(",")

        ids = [self.get_adapter().object_id(_id) for _id in ids if _id]
        is_global = self.field("is_global", False, cast = bool)
        model = self.get_model(model)

        # creates the set of named arguments dictionary to be used
        # for the selection of the target entities
        if ids: kwargs = dict(_id = {"$in" : ids})
        else: kwargs = dict()

        # retrieves the reference to the appropriate entities (or
        # classes) taking into account if the link is global or not
        if is_global: entities = (model,)
        else: entities = model.find_v(**kwargs)

        # creates the new keyword based dictionary that is going to
        # be used to set the named arguments for the link method call
        # in case there's some (eg: context)
        kwargs = dict()

        # applies both the view and the context to the keyword based
        # dictionary to be passed to the link (generation) method, they
        # are going to constrain the domain for the link execution
        if view: kwargs["view"] = view
        if context: kwargs["context"] = "_id:in:" + ";".join(context)

        # defines the default result value as an invalid value,
        # this will ensure an error in the redirection process
        result = None

        # iterates over the complete set of selected entities to
        # obtain the result redirection string value for each of
        # them, notice that only the last is going to be used
        for entity in entities:
            method = getattr(entity, link)
            result = method(*parameters, **kwargs)

        # runs the redirection of the user agent to the final
        # result string (and URL) value
        return self.redirect(result)

    @appier.ensure(token = "admin", context = "admin")
    def operation_model(self, model, operation):
        # ensures that the proper token is available so that the
        # operation may be executed under the current context
        appier.ensure_login(self, token = "admin.models." + model)

        # retrieves the complete set of fields that are going to
        # be used while performing the operation and runs the
        # complete set of casting operations for each of them
        parameters = self.get_fields("parameters", [])
        next = self.field("next")
        view = self.field("view", None)
        ids = self.field("ids", "")
        ids = ids.split(",")
        ids = [self.get_adapter().object_id(_id) for _id in ids if _id]
        is_global = self.field("is_global", False, cast = bool)

        # retrieves the model information (class) for the provided
        # name and then also the operation definition (metadata)
        model = self.get_model(model)
        definition = model.operation(operation)

        # uses the definition of the operation to retrieve its descriptive
        # name to be used in the message to be sent to the end-user
        operation_s = definition.get("name", operation)

        # using the retrieved information determines if the operation
        # is considered to be a factory one (generates entity) and
        # then casts the provided parameters according to metadata
        factory = definition.get("factory", False)
        parameters = definition.cast(parameters)
        parameters_kw = definition.cast(parameters, keyword = True)

        # determines the filter information that is going to be passed
        # to the find operations and retrieves the associated entities
        # that are going to be the target for the operations, note that
        # if this is a global operation classes are used instead
        if ids: kwargs = dict(_id = {"$in" : ids})
        else: kwargs = dict()
        kwargs = self._apply_view(view, kwargs = kwargs, cls = model)
        if is_global: entities = (model,)
        else: entities = model.find_v(**kwargs)

        # determines if this is going to be a single entity target
        # operation or if otherwise it's a multiple target one, taking
        # that into account determines if this is considered a factory
        # operation, note that only single operations are allowed
        is_single = len(entities) == 1
        factory = factory and is_single

        # defines the original/default result value for the complete
        # set of operations to be performed
        result = None

        # iterates over the complete set of selected entities and
        # performs the requested operation for each of them
        for entity in entities:
            method = getattr(entity, operation)
            method_kw = appier.legacy.getargspec(method)[2]
            result = method(**parameters_kw) if method_kw else method(*parameters)

        # in case the factory mode is enabled, a new entity has been
        # created and proper redirection must be performed so that the
        # new entity is shown instead of the default show model, in case
        # the returned value from the operation is a string one the
        # redirection is made directly to that target value
        if factory:
            is_string = appier.legacy.is_string(result)
            if is_string: return self.redirect(result)
            cls = result.__class__
            model_name = cls._under()
            model_id = result._id
            return self.redirect(
                self.url_for(
                    "admin.show_entity",
                    message = "Operation %s completed with success" % operation_s,
                    model = model_name,
                    _id = model_id
                )
            )

        # runs the default redirection process that displays the model
        # page for the model used as target for the operation
        return self.redirect(
            next or self.url_for(
                "admin.show_model",
                message = "Operation %s completed with success" % operation_s,
                model = model._under()
            ),
            message = "Operation %s completed with success" % operation_s
        )

    @appier.ensure(token = "admin", context = "admin")
    def view_model(self, model, view):
        appier.ensure_login(self, token = "admin.models." + model)

        parameters = self.get_fields("parameters", [])
        _id = self.field("id", None)
        is_global = False if _id else True

        model_s = model
        parameters_s = ",".join(parameters)

        model = self.get_model(model)
        model.assert_is_concrete_g()

        if _id: entity = model.get_v(_id = self.get_adapter().object_id(_id))
        else: entity = model

        object = appier.get_object(
            alias = True,
            page = True,
            find = True
        )

        definition = model.view(view)
        parameters = definition.cast(parameters)
        method = getattr(entity, view)
        result = method(
            rules = False,
            meta = True,
            *parameters,
            **object
        )
        target = result["model"]
        entities = result["entities"]
        page = result["page"]
        names = result.get("names", None)

        if _id: view_s = "%s:%s.%s" % (model_s, _id, view)
        else: view_s = "%s.%s" % (model_s, view)
        if parameters_s: view_s += "(%s)" % parameters_s

        return self.template(
            "views/show.html.tpl",
            section = "models",
            model = model,
            target = target,
            entity = entity,
            entities = entities,
            page = page,
            definition = definition,
            names = names,
            view = view_s,
            is_global = is_global
        )

    @appier.ensure(token = "admin", context = "admin")
    def new_entity(self, model):
        model = self.get_model(model)
        return self.template(
            "entities/new.html.tpl",
            section = "models",
            entity = model.__new__(model),
            errors = dict(),
            model = model
        )

    @appier.ensure(token = "admin", context = "admin")
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
            self.url_for("admin.show_model", model = model._under())
        )

    @appier.ensure(token = "admin", context = "admin")
    def show_entity(self, model, _id):
        appier.ensure_login(self, token = "admin.models." + model)
        model = self.get_model(model, raise_e = True)
        entity = model.get_v(
            rules = False,
            meta = True,
            _id = self.get_adapter().object_id(_id)
        )
        previous_url, next_url = self._entity_urls(entity)
        return self.template(
            "entities/show.html.tpl",
            section = "models",
            entity = entity,
            model = model,
            previous_url = previous_url,
            next_url = next_url
        )

    @appier.ensure(token = "admin", context = "admin")
    def show_entity_json(self, model, _id):
        appier.ensure_login(self, token = "admin.models." + model)
        eager_l = self.field("eager_l", True, cast = bool)
        rules = self.field("rules", False, cast = bool)
        meta = self.field("meta", False, cast = bool)
        model = self.get_model(model, raise_e = True)
        entity = model.get_v(
            eager_l = eager_l,
            rules = rules,
            meta = meta,
            map = True,
            _id = self.get_adapter().object_id(_id)
        )
        return entity

    @appier.ensure(token = "admin", context = "admin")
    def edit_entity(self, model, _id):
        appier.ensure_login(self, token = "admin.models." + model)
        model = self.get_model(model, raise_e = True)
        entity = model.get_v(
            rules = False,
            meta = True,
            _id = self.get_adapter().object_id(_id)
        )
        return self.template(
            "entities/edit.html.tpl",
            section = "models",
            entity = entity,
            errors = dict(),
            model = model
        )

    @appier.ensure(token = "admin", context = "admin")
    def update_entity(self, model, _id):
        appier.ensure_login(self, token = "admin.models." + model)
        model = self.get_model(model, raise_e = True)
        entity = model.get_v(
            rules = False,
            meta = True,
            _id = self.get_adapter().object_id(_id)
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
                model = model._under(),
                _id = _id
            )
        )

    @appier.ensure(token = "admin", context = "admin")
    def delete_entity(self, model, _id):
        appier.ensure_login(self, token = "admin.models." + model)
        model = self.get_model(model, raise_e = True)
        entity = model.get_v(_id = self.get_adapter().object_id(_id))
        entity.delete()
        return self.redirect(
            self.url_for(
                "admin.show_model",
                model = model._under()
            )
        )

    def facebook(self):
        next = self.field("next", "")
        context = self.field("context", "login")
        state = context + ":" + next
        secure = not context == "login"
        if secure: appier.ensure("admin")
        scope = self.owner.admin_facebook_scope if secure else None
        url = self.ensure_facebook_api(
            state = state,
            scope = scope,
            refresh = secure
        )
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def unlink_facebook(self):
        next = self.field("next")
        context = self.field("context", "login")
        if context == "login":
            self.session.pop("fb.access_token", None)
        elif context == "global":
            settings = models.Settings.get_settings()
            settings.facebook_token = None
            settings.save()
        return self.redirect(
           next or self.url_for("admin.social")
        )

    def unset_facebook(self):
        next = self.field("next")
        self.unset_facebook_account()
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def oauth_facebook(self):
        if not self.owner.admin_available: raise appier.SecurityError(
            message = "Administration not available"
        )
        code = self.field("code")
        state = self.field("state")
        context, next = state.split(":", 1)
        api = self.get_facebook_api()
        access_token = api.oauth_access(code)
        if context == "login":
            self.session["fb.access_token"] = access_token
            self.ensure_facebook_account(create = self.owner.admin_open)
        elif context == "global":
            settings = models.Settings.get_settings()
            settings.facebook_token = access_token
            settings.save()
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def github(self):
        next = self.field("next", "")
        context = self.field("context", "login")
        state = context + ":" + next
        secure = not context == "login"
        if secure: appier.ensure("admin")
        scope = self.owner.admin_github_scope if secure else None
        url = self.ensure_github_api(
            state = state,
            scope = scope,
            refresh = secure
        )
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def unlink_github(self):
        next = self.field("next")
        context = self.field("context", "login")
        if context == "login":
            self.session.pop("gh.access_token", None)
        elif context == "global":
            settings = models.Settings.get_settings()
            settings.github_token = None
            settings.save()
        return self.redirect(
           next or self.url_for("admin.social")
        )

    def unset_github(self):
        next = self.field("next")
        self.unset_twitter_account()
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def oauth_github(self):
        if not self.owner.admin_available: raise appier.SecurityError(
            message = "Administration not available"
        )
        code = self.field("code")
        state = self.field("state")
        context, next = state.split(":", 1)
        api = self.get_github_api()
        access_token = api.oauth_access(code)
        if context == "login":
            self.session["gh.access_token"] = access_token
            self.ensure_github_account(create = self.owner.admin_open)
        elif context == "global":
            settings = models.Settings.get_settings()
            settings.github_token = access_token
            settings.save()
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def google(self):
        next = self.field("next", "")
        context = self.field("context", "login")
        state = context + ":" + next
        secure = not context == "login"
        if secure: appier.ensure("admin")
        scope = self.owner.admin_google_scope if secure else None
        access_type = "offline" if secure else None
        approval_prompt = True if secure else False
        url = self.ensure_google_api(
            state = state,
            access_type = access_type,
            approval_prompt = approval_prompt,
            scope = scope,
            refresh = secure
        )
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def unlink_google(self):
        next = self.field("next")
        context = self.field("context", "login")
        if context == "login":
            self.session.pop("gg.access_token", None)
        elif context == "global":
            settings = models.Settings.get_settings()
            settings.google_token = None
            settings.google_refresh_token = None
            settings.google_email = None
            settings.google_scope = None
            settings.save()
        return self.redirect(
           next or self.url_for("admin.social")
        )

    def unset_google(self):
        next = self.field("next")
        self.unset_google_account()
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def oauth_google(self):
        if not self.owner.admin_available: raise appier.SecurityError(
            message = "Administration not available"
        )
        code = self.field("code")
        state = self.field("state")
        context, next = state.split(":", 1)
        api = self.get_google_api()
        access_token = api.oauth_access(code)
        if context == "login":
            self.session["gg.access_token"] = access_token
            self.ensure_google_account(create = self.owner.admin_open)
        elif context == "global":
            user = api.self_user()
            email = user["emails"][0]["value"]
            info = api.token_info()
            scope = info["scope"]
            scope = scope.split(" ")
            settings = models.Settings.get_settings()
            settings.google_token = access_token
            settings.google_refresh_token = api.refresh_token
            settings.google_email = email
            settings.google_scope = scope
            settings.save()
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def live(self):
        next = self.field("next", "")
        context = self.field("context", "login")
        state = context + ":" + next
        secure = not context == "login"
        if secure: appier.ensure("admin")
        scope = self.owner.admin_live_scope if secure else None
        url = self.ensure_live_api(
            state = state,
            scope = scope,
            refresh = secure
        )
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def unlink_live(self):
        next = self.field("next")
        context = self.field("context", "login")
        if context == "login":
            self.session.pop("live.access_token", None)
        elif context == "global":
            settings = models.Settings.get_settings()
            settings.live_token = None
            settings.save()
        return self.redirect(
           next or self.url_for("admin.social")
        )

    def unset_live(self):
        next = self.field("next")
        self.unset_live_account()
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def oauth_live(self):
        if not self.owner.admin_available: raise appier.SecurityError(
            message = "Administration not available"
        )
        code = self.field("code")
        state = self.field("state")
        context, next = state.split(":", 1)
        api = self.get_live_api()
        access_token = api.oauth_access(code)
        if context == "login":
            self.session["live.access_token"] = access_token
            self.ensure_live_account(create = self.owner.admin_open)
        elif context == "global":
            settings = models.Settings.get_settings()
            settings.live_token = access_token
            settings.save()
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def twitter(self):
        next = self.field("next", "")
        context = self.field("context", "login")
        state = context + ":" + next
        secure = not context == "login"
        if secure: appier.ensure("admin")
        url = self.ensure_twitter_api(state = state, refresh = secure)
        if url: return self.redirect(url)
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def unlink_twitter(self):
        next = self.field("next")
        context = self.field("context", "login")
        if context == "login":
            self.session.pop("tw.access_token", None)
            self.session.pop("tw.oauth_token_secret", None)
            self.session.pop("tw.oauth_temporary", None)
        elif context == "global":
            settings = models.Settings.get_settings()
            settings.twitter_token = None
            settings.twitter_token_secret = None
            settings.save()
        return self.redirect(
           next or self.url_for("admin.social")
        )

    def unset_twitter(self):
        next = self.field("next")
        self.unset_twitter_account()
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    def oauth_twitter(self):
        if not self.owner.admin_available: raise appier.SecurityError(
            message = "Administration not available"
        )
        oauth_verifier = self.field("oauth_verifier")
        state = self.field("state")
        context, next = state.split(":", 1)
        api = self.get_twitter_api()
        oauth_token, oauth_token_secret = api.oauth_access(oauth_verifier)
        if context == "login":
            self.session["tw.oauth_token"] = oauth_token
            self.session["tw.oauth_token_secret"] = oauth_token_secret
            self.session["tw.oauth_temporary"] = False
            self.ensure_twitter_account(create = self.owner.admin_open)
        elif context == "global":
            settings = models.Settings.get_settings()
            settings.twitter_token = oauth_token
            settings.twitter_token_secret = oauth_token_secret
            settings.save()
        return self.redirect(
           next or self.url_for(self.owner.admin_login_redirect)
        )

    @appier.ensure(token = "admin", context = "admin")
    def show_log(self):
        memory_handler = self.owner.handler_memory
        count = self.field("count", 100, cast = int)
        level = self.field("level", None)
        return dict(
            messages = memory_handler.get_latest(count = count, level = level)
        )

    @appier.ensure(token = "admin", context = "admin")
    def show_configs(self):
        return appier.config.CONFIGS

    def ping_api(self):
        return dict(time = time.time())

    def oauth_access_token_api(self):
        return self.oauth_access_token()

    def oauth_login_api(self):
        return self.oauth_login()

    def login_api(self):
        # verifies if the current administration interface is
        # available and if that's not the cases raises an error
        if not self.owner.admin_available: raise appier.SecurityError(
            message = "Administration not available"
        )

        # retrieves the various fields that are going to be
        # used for the validation of the user under the current
        # authentication/authorization process
        username = self.field("username", mandatory = True)
        password = self.field("password", mandatory = True)
        account = self.account_c.login(username, password)

        # updates the current session with the proper
        # values to correctly authenticate the user
        account._set_session()

        # retrieves the session identifier (SID) for the currently
        # assigned session, this is going to be used in the next
        # requests to refer to the proper session
        sid = self.session.sid

        # redirects the current operation to the next URL or in
        # alternative to the root index of the administration
        return dict(
            sid = sid,
            session_id = sid,
            username = username,
            tokens = account.tokens()
        )

    @appier.ensure(context = "admin")
    def me_account_api(self):
        account_c = self._get_cls(self.account_c)
        account = account_c.from_session(map = True)
        return account

    def socials(self):
        socials = []
        if self.has_facebook(): socials.append("facebook")
        if self.has_github(): socials.append("github")
        if self.has_google(): socials.append("google")
        if self.has_live(): socials.append("live")
        if self.has_twitter(): socials.append("twitter")
        return socials

    def linked(self):
        return models.Settings.linked_apis()

    def markdown_jinja(self, value, *args, **kwargs):
        result = self.markdown(value, *args, **kwargs)
        return self.owner.escape_template(result)

    def markdown(
        self,
        value,
        anchors = False,
        blank = True,
        encoding = "utf-8"
    ):
        value = utils.MarkdownHTML.process_str(
            value,
            options = dict(
                anchors = anchors,
                blank = blank
            ),
            encoding = encoding
        )
        return appier.legacy.u(
            value,
            encoding = encoding,
            force = True
        )

    @property
    def settings_l(self):
        return (
            "_last_login",
            "_login_count"
        )

    def _counters(self):
        adapter = self.get_adapter()
        collection = adapter.collection("counters")
        return collection

    def _appier_extras_loader(self, module):
        versions = []
        if hasattr(module, "VERSION"):
            versions.append(("AppierExtras", module.VERSION))
        return versions

    def _netius_loader(self, module):
        versions = []
        if hasattr(module, "VERSION"):
            versions.append(("Netius", module.VERSION))
        return versions

    def _pconvert_loader(self, module):
        versions = []
        if hasattr(module, "VERSION"):
            versions.append(("P(NG)Convert", module.VERSION))
        return versions

    def _pil_loader(self, module):
        versions = []
        if hasattr(module, "VERSION"):
            versions.append(("PIL", module.VERSION))
        if hasattr(module, "PILLOW_VERSION"):
            versions.append(("Pillow", module.PILLOW_VERSION))
        return versions

    def _pymongo_loader(self, module):
        versions = []
        if hasattr(module, "version"):
            versions.append(("PyMongo", module.version))
        return versions

    def _redis_loader(self, module):
        versions = []
        if hasattr(module, "VERSION"):
            version = ".".join([str(item) for item in module.VERSION])
            versions.append(("RedisPy", version))
        return versions

    def _jinja2_loader(self, module):
        versions = []
        if hasattr(module, "__version__"):
            versions.append(("Jinja2", module.__version__))
        return versions

    def _ssl_loader(self, module):
        versions = []
        if hasattr(module, "OPENSSL_VERSION"):
            versions.append(("SSL", module.OPENSSL_VERSION))
        return versions

    def _attached(self, models):
        return [model for model in models if model.is_attached()]

    def _visible(self, models):
        return [model for model in models if model.is_visible()]

    def _concrete(self, models):
        models = self._attached(models)
        return [model for model in models if model.is_concrete()]

    def _administrable(self, _models, parent = None):
        parent = parent or models.Base
        _models = self._concrete(_models)
        return [model for model in _models if model.is_child(parent)]

    def _accessible(self, models):
        return [model for model in models if\
             appier.check_login(self, "admin.models." + model._under())]

    def _available(self, models):
        models = self._administrable(models)
        models = self._visible(models)
        models = self._accessible(models)
        return models

    def _is_available(self, model, parent = None):
        parent = parent or models.Base
        if not model.is_child(parent): return False
        if not model.is_concrete(): return False
        if not model.is_visible(): return False
        if not appier.check_login(self, "admin.models." + model._under()): return False
        return True

    def _sort(self, object, model):
        if "sort" in object: return object
        order = model.order_name()
        if not order: return object
        is_sequence = isinstance(order, (list, tuple))
        if not is_sequence: order = (order, 1)
        object["sort"] = [order]
        return object

    def _hybrid(self, name, default = None):
        if name in self.session: return self.session[name]
        if hasattr(self.owner, name): return getattr(self.owner, name)
        if hasattr(self, name): return getattr(self, name)
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

    def _to_meta(self, type):
        return appier.Model._to_meta(type)

    def _get_cls(self, default = None, raise_e = True):
        cls = self.field("cls", None)
        if not cls: return default
        return self.owner.get_model(cls, raise_e = raise_e)

    def _entity_urls(self, entity):
        model = entity.__class__
        previous = entity.previous()
        next = entity.next()
        previous_url = self.url_for(
            "admin.show_entity",
            model = model._under(),
            _id = previous._id
        ) if previous else None
        next_url = self.url_for(
            "admin.show_entity",
            model = model._under(),
            _id = next._id
        ) if next else None
        return previous_url, next_url

    def _find_view(self, cls, *args, **kwargs):
        """
        Runs a find operation taking into account the provided
        view (as a field) constraining the domain.

        This method is extremely useful for back-office operations
        that use the dynamic view filtering.

        :type cls: Class
        :param cls: The (model) class that is going to be used in
        the find operation.
        :rtype: List
        :return: The complete set of results from the data source
        according to the provided parameters and filtered view.
        """

        view = self.field("view", None)
        kwargs = self._apply_view(view, kwargs = kwargs, cls = cls)
        return cls.find(*args, **kwargs)

    def _apply_view(self, view, kwargs = None, cls = None):
        """
        Applies a certain view (with properly defined syntax) into
        the provided arguments so that it's possible to run the
        final result in a typical find operation.

        Optionally one may provide the model class so that the view
        is ensured to be associated with such class.

        :type view: String
        :param view: The string describing the view that should be
        applied to the provided arguments.
        :type kwargs: Dictionary
        :param kwargs: The dictionary that contains the extra arguments
        that are going to be affected by the view apply operation.
        This object is going to be mutated.
        :type cls: Class
        :param cls: The class that if provided is going to be validated
        against the view, meaning that only views that were designed to
        returns entities of this class are going to pass validation.
        :rtype: Dictionary
        :return: The final dictionary with the view filter applied.
        """

        kwargs = dict() if kwargs == None else kwargs

        if not view: return kwargs

        model, view = view.split(".")

        is_instance = ":" in model
        if is_instance: model, id = model.split(":")

        model = self.get_model(model, raise_e = True)
        model.assert_is_concrete_g()

        if is_instance: model = model.get(
            _id = self.get_adapter().object_id(id)
        )

        start_param = view.find("(")
        end_param = view.find(")")
        is_valid = not start_param == -1 and not end_param == -1

        if is_valid:
            view, parameters = view[:start_param], view[start_param + 1:end_param]
            parameters = [parameter.strip() for parameter in parameters.split(",")]
        else:
            parameters = []

        definition = model.view(view)
        parameters = definition.cast(parameters)
        parameters_kw = definition.cast(parameters, keyword = True)
        parameters_kw.update(kwargs)

        method = getattr(model, view)
        method_kw = appier.legacy.getargspec(method)[2]
        result = method(**parameters_kw) if method_kw else method(*parameters, **kwargs)

        # ensures that the model type in the result from the view apply
        # is the expected one (if entity class is provided) this is relevant
        # to avoid issues with bad filtering methods
        appier.verify(not cls or result["model"].is_equal(cls))

        kwargs = result["kwargs"]
        return kwargs

    def _on_touch_login(self, account):
        self._last_login = time.time()
        self._login_count += 1
        self.flush_settings()

    @property
    def _last_login_s(self, format = "%Y-%m-%d %H:%M:%S UTC"):
        if not self._last_login: return None
        try:
            date_time = datetime.datetime.utcfromtimestamp(self._last_login)
            return date_time.strftime(format)
        except TypeError:
            return None
