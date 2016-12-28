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

import os
import json
import time
import datetime
import tempfile

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
        self.layout = "fluid"
        self.theme = "modern"
        self.style = "romantic"
        self.libs = "current"

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
        self.owner.admin_open = True
        self.owner.admin_login_route = "admin.login"
        self.owner.admin_login_redirect = "admin.index"
        self.owner.admin_facebook_scope = ("email",)
        self.owner.admin_github_scope = ("user:email",)
        self.owner.admin_google_scope = ("email",)
        self.owner.admin_live_scope = ("wl.basic", "wl.emails")

        self.owner.lib_loaders["appier_extras"] = self._appier_extras_loader
        self.owner.lib_loaders["netius"] = self._netius_loader
        self.owner.lib_loaders["PIL"] = self._pil_loader
        self.owner.lib_loaders["pymongo"] = self._pymongo_loader
        self.owner.lib_loaders["redis"] = self._redis_loader
        self.owner.lib_loaders["jinja2"] = self._jinja2_loader
        self.owner.lib_loaders["ssl"] = self._ssl_loader

        if self.owner.allow_headers: self.owner.allow_headers += ", X-Secret-Key"

        self.logger.debug("Generating admin interfaces ...")
        for model_c in self.models_r:
            if not model_c.is_attached(): continue
            self.logger.debug(model_c)

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
            (("GET",), "/admin/status", self.status),
            (("GET",), "/admin/social", self.social),
            (("GET",), "/admin/operations", self.operations),
            (("GET",), "/admin/routes", self.list_routes),
            (("GET",), "/admin/configs", self.list_configs),
            (("GET",), "/admin/parts", self.list_parts),
            (("GET",), "/admin/libraries", self.list_libraries),
            (("GET",), "/admin/operations/build_index", self.build_index),
            (("GET",), "/admin/operations/test_email", self.test_email),
            (("GET",), "/admin/operations/test_event", self.test_event),
            (("GET",), "/admin/sessions", self.list_sessions),
            (("GET",), "/admin/sessions/empty", self.empty_sessions),
            (("GET",), "/admin/sessions/me", self.show_session_me),
            (("GET",), "/admin/sessions/me/delete", self.delete_session_me),
            (("GET",), "/admin/sessions/<str:sid>", self.show_session),
            (("GET",), "/admin/sessions/<str:sid>/delete", self.delete_session),
            (("GET",), "/admin/counters", self.list_counters),
            (("GET",), "/admin/events.csv", self.list_events_csv),
            (("GET",), "/admin/database", self.database),
            (("GET",), "/admin/database/export", self.database_export),
            (("GET",), "/admin/database/import", self.database_import),
            (("POST",), "/admin/database/import", self.database_import_do),
            (("GET",), "/admin/database/reset", self.database_reset),
            (("GET",), "/admin/search", self.search),
            (("GET",), "/admin/accounts/new", self.new_account),
            (("POST",), "/admin/accounts", self.create_account),
            (("GET",), "/admin/accounts/<str:username>", self.show_account),
            (("GET",), "/admin/accounts/<str:username>/mail", self.mail_account),
            (("GET",), "/admin/models", self.list_models),
            (("GET",), "/admin/models/<str:model>.json", self.show_model_json, None, True),
            (("GET",), "/admin/models/<str:model>.csv", self.show_model_csv),
            (("GET",), "/admin/models/<str:model>", self.show_model),
            (("GET", "POST"), "/admin/models/<str:model>/links/<str:link>", self.link_model),
            (("GET", "POST"), "/admin/models/<str:model>/operations/<str:operation>", self.operation_model),
            (("GET",), "/admin/models/<str:model>/new", self.new_entity),
            (("POST",), "/admin/models/<str:model>", self.create_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>.json", self.show_entity_json, None, True),
            (("GET",), "/admin/models/<str:model>/<str:_id>", self.show_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>/edit", self.edit_entity),
            (("POST",), "/admin/models/<str:model>/<str:_id>/edit", self.update_entity),
            (("GET",), "/admin/models/<str:model>/<str:_id>/delete", self.delete_entity),
            (("GET",), "/admin/facebook", self.facebook),
            (("GET",), "/admin/facebook/unlink", self.unlink_facebook),
            (("GET",), "/admin/facebook/oauth", self.oauth_facebook),
            (("GET",), "/admin/github", self.github),
            (("GET",), "/admin/github/unlink", self.unlink_github),
            (("GET",), "/admin/github/oauth", self.oauth_github),
            (("GET",), "/admin/google", self.google),
            (("GET",), "/admin/google/unlink", self.unlink_google),
            (("GET",), "/admin/google/oauth", self.oauth_google),
            (("GET",), "/admin/live", self.live),
            (("GET",), "/admin/live/unlink", self.unlink_live),
            (("GET",), "/admin/live/oauth", self.oauth_live),
            (("GET",), "/admin/twitter", self.twitter),
            (("GET",), "/admin/twitter/unlink", self.unlink_twitter),
            (("GET",), "/admin/twitter/oauth", self.oauth_twitter),
            (("GET",), "/admin/log.json", self.show_log, None, True),
            (("GET",), "/admin/configs.json", self.show_configs, None, True),
            (("GET",), "/api/admin/ping", self.ping_api, None, True),
            (("GET", "POST"), "/api/admin/login", self.login_api, None, True),
            (("GET",), "/api/admin/models/<str:model>", self.show_model_json, None, True),
            (("GET",), "/api/admin/models/<str:model>/<str:_id>", self.show_entity_json, None, True)
        ]

    def models(self):
        return models

    def template(self, template, layout = None, *args, **kwargs):
        layout = self.session.get("layout", self.layout)
        template = "%s/%s" % (layout, template)
        return appier.Part.template(
            self,
            template,
            owner = self.owner,
            models_d = self.models_d,
            *args,
            **kwargs
        )

    def before_request(self):
        key = self.get_field("skey", None)
        key = self.get_field("secret_key", key)
        key = self.request.get_header("X-Secret-Key", key)
        if not key: return
        try: account = models.Account.login_key(key)
        except appier.OperationalError: pass
        else: account._set_session(method = "set_t")

    def exception_handler(self, error):
        import traceback
        lines = traceback.format_exc().splitlines()
        lines = self._lines(lines)
        lines = lines if self.owner.is_devel() else []
        return self.template(
            "error.html.tpl",
            error = error,
            lines = lines
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
        account._set_session()

        # redirects the current operation to the next url or in
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
        models.Account._unset_session()

        # runs the proper redirect operation, taking into account if the
        # next value has been provided or not
        return self.redirect(
            next or self.url_for(self.owner.admin_login_redirect)
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
        password = self.field("password")
        password_confirm = self.field("password_confirm")
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
        if not self.owner.admin_open: raise appier.SecurityError(
            message = "signup not allowed"
        )
        return self.template(
            "account/new.html.tpl",
            account = dict(),
            errors = dict()
        )

    def create_account(self):
        if not self.owner.admin_open: raise appier.SecurityError(
            message = "signup not allowed"
        )
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
    def social(self):
        socials = self.socials()
        linked = self.linked()
        return self.template(
            "social.html.tpl",
            section = "social",
            socials = socials,
            linked = linked
        )

    @appier.ensure(token = "admin")
    def operations(self):
        return self.template(
            "operations.html.tpl",
            section = "operations"
        )

    @appier.ensure(token = "admin")
    def list_routes(self):
        return self.template(
            "routes.html.tpl",
            section = "status",
            routes = self._routes()
        )

    @appier.ensure(token = "admin")
    def list_configs(self):
        configs = appier.config.CONFIGS
        configs = appier.legacy.items(configs)
        configs.sort()
        return self.template(
            "configs.html.tpl",
            section = "status",
            configs = configs
        )

    @appier.ensure(token = "admin")
    def list_parts(self):
        app = appier.get_app()
        parts = app.get_parts()
        return self.template(
            "parts.html.tpl",
            section = "status",
            parts = parts
        )

    @appier.ensure(token = "admin")
    def list_libraries(self):
        app = appier.get_app()
        libraries = app.get_libraries()
        return self.template(
            "libraries.html.tpl",
            section = "status",
            libraries = libraries
        )

    @appier.ensure(token = "admin")
    def build_index(self):
        empty = self.field("empty", True, cast = bool)
        if empty: models.Search.delete_c()
        for model in self._attached(self.models_r):
            model.build_index_g()
        return self.redirect(
            self.url_for(
                "admin.operations",
                message = "Search index built with success"
            )
        )

    @appier.ensure(token = "admin")
    def test_email(self):
        receiver = appier.conf("TEST_EMAIL", None)
        receiver = self.field("email", receiver)
        receiver = self.field("receiver", receiver)
        if not receiver: raise appier.OperationalError(
            message = "No test email defined"
        )
        models.Base.send_email_g(
            appier.get_app(),
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

    @appier.ensure(token = "admin")
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

    @appier.ensure(token = "admin")
    def list_sessions(self):
        return self.template(
            "sessions.html.tpl",
            section = "status",
            sessions = self.request.session_c.all()
        )

    @appier.ensure(token = "admin")
    def empty_sessions(self):
        self.request.session_c.empty()
        return self.redirect(
            self.url_for(
                "admin.list_sessions",
                message = "Sessions emptied with success"
            )
        )

    @appier.ensure(token = "admin")
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

    @appier.ensure(token = "admin")
    def show_session(self, sid):
        sid = str(sid)
        return self.template(
            "session.html.tpl",
            section = "status",
            session_s = self.request.session_c.get_s(sid)
        )

    @appier.ensure(token = "admin")
    def delete_session(self, sid):
        sid = str(sid)
        self.request.session_c.expire(sid)
        return self.redirect(
            self.url_for(
                "admin.list_sessions",
                message = "Session deleted with success"
            )
        )

    @appier.ensure(token = "admin")
    def list_counters(self):
        collection = self._counters()
        counters = collection.find()
        return self.template(
            "counters.html.tpl",
            section = "status",
            counters = counters
        )

    @appier.ensure(token = "admin")
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

    @appier.ensure(token = "admin")
    def database(self):
        return self.template(
            "database.html.tpl",
            section = "database"
        )

    @appier.ensure(token = "admin")
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
        self.request.set_header(
            "Content-Disposition",
            "attachment; filename=\"%s\"" % file_name
        )

        return file.getvalue()

    @appier.ensure(token = "admin")
    def database_import(self):
        return self.template(
            "database/import.html.tpl",
            section = "database"
        )

    @appier.ensure(token = "admin")
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

    @appier.ensure(token = "admin")
    def search(self):
        object = appier.get_object(
            alias = True,
            find = True,
            find_i = True,
            find_t = "right"
        )
        indexes = models.Search.find(map = True, **object)
        return indexes

    @appier.ensure(token = "admin")
    def database_reset(self):
        adapter = self.get_adapter()
        adapter.drop_db()
        return self.redirect(
            self.url_for(
                "admin.database",
                message = "Database dropped/reset with success"
            )
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
        object = self._sort(object, model)
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
    def link_model(self, model, link):
        parameters = self.get_fields("parameters", [])
        ids = self.field("ids", "")
        ids = ids.split(",")
        ids = [self.get_adapter().object_id(_id) for _id in ids if _id]
        is_global = self.field("is_global", False, cast = bool)
        model = self.get_model(model)
        if ids: kwargs = dict(_id = {"$in" : ids})
        else: kwargs = dict()
        if is_global: entities = (model,)
        else: entities = model.find(**kwargs)
        result = None
        for entity in entities:
            method = getattr(entity, link)
            result = method(*parameters)
        return self.redirect(result)

    @appier.ensure(token = "admin")
    def operation_model(self, model, operation):
        # retrieves the complete set of fields that are going to
        # be used while performing the operation and runs the
        # complete set of casting operations for each of them
        parameters = self.get_fields("parameters", [])
        next = self.field("next")
        ids = self.field("ids", "")
        ids = ids.split(",")
        ids = [self.get_adapter().object_id(_id) for _id in ids if _id]
        is_global = self.field("is_global", False, cast = bool)

        # retrieves the model information (class) for the provided
        # name and then also the operation definition (metadata)
        model = self.get_model(model)
        definition = model.operation(operation)

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
        if is_global: entities = (model,)
        else: entities = model.find(**kwargs)

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
        # new entity is shown instead of the default show model
        if factory:
            cls = result.__class__
            model_name = cls._name()
            model_id = result._id
            return self.redirect(
                self.url_for(
                    "admin.show_entity",
                    model = model_name,
                    _id = model_id
                )
            )

        # runs the default redirection process that displays the model
        # page for the model used as target for the operation
        return self.redirect(
            next or self.url_for("admin.show_model", model = model._name())
        )

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
            _id = self.get_adapter().object_id(_id)
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
            _id = self.get_adapter().object_id(_id)
        )
        return entity

    @appier.ensure(token = "admin")
    def edit_entity(self, model, _id):
        model = self.get_model(model)
        entity = model.get(
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

    @appier.ensure(token = "admin")
    def update_entity(self, model, _id):
        model = self.get_model(model)
        entity = model.get(
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
                model = model._name(),
                _id = _id
            )
        )

    @appier.ensure(token = "admin")
    def delete_entity(self, model, _id):
        model = self.get_model(model)
        entity = model.get(_id = self.get_adapter().object_id(_id))
        entity.delete()
        return self.redirect(
            self.url_for(
                "admin.show_model",
                model = model._name()
            )
        )

    def facebook(self):
        next = self.field("next")
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

    def oauth_facebook(self):
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
        next = self.field("next")
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

    def oauth_github(self):
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
        next = self.field("next")
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

    def oauth_google(self):
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
        next = self.field("next")
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

    def oauth_live(self):
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
        next = self.field("next")
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

    def oauth_twitter(self):
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

    @appier.ensure(token = "admin")
    def show_log(self):
        memory_handler = self.owner.handler_memory
        count = self.field("count", 100, cast = int)
        level = self.field("level", None)
        return dict(
            messages = memory_handler.get_latest(count = count, level = level)
        )

    @appier.ensure(token = "admin")
    def show_configs(self):
        return appier.config.CONFIGS

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
        account._set_session()

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
        if self.has_github(): socials.append("github")
        if self.has_google(): socials.append("google")
        if self.has_live(): socials.append("live")
        if self.has_twitter(): socials.append("twitter")
        return socials

    def linked(self):
        return models.Settings.linked_apis()

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
