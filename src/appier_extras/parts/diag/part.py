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

import socket
import datetime

import appier

from appier_extras import base

from appier_extras.parts.diag import models

class DiagPart(appier.Part):
    """
    Modular part class that provides an infra-structure of diagnostics
    that allow more and better debugging of an Application.

    Notice that most of the diagnostics is performed locally and is
    not optimized for proper asynchronous usage.
    """

    def __init__(self, *args, **kwargs):
        appier.Part.__init__(self, *args, **kwargs)
        self.store = kwargs.get("store", False)
        self.loggly = kwargs.get("loggly", False)
        self.logstash = kwargs.get("logstash", False)
        self.output = kwargs.get("output", True)
        self.geo = kwargs.get("geo", True)
        self.level = kwargs.get("level", "normal")
        self.verbose = kwargs.get("verbose", False)
        self.minimal = kwargs.get("minimal", False)
        self.format = kwargs.get("format", "combined")
        self.empty = kwargs.get("empty", False)
        self.store = appier.conf("DIAG_STORE", self.store, cast = bool)
        self.loggly = appier.conf("DIAG_LOGGLY", self.loggly, cast = bool)
        self.logstash = appier.conf("DIAG_LOGSTASH", self.loggly, cast = bool)
        self.output = appier.conf("DIAG_OUTPUT", self.output, cast = bool)
        self.output = appier.conf("DIAG_STDOUT", self.output, cast = bool)
        self.geo = appier.conf("DIAG_GEO", self.geo, cast = bool)
        self.level = appier.conf("DIAG_LEVEL", self.level)
        self.verbose = appier.conf("DIAG_VERBOSE", self.verbose, cast = bool)
        self.minimal = appier.conf("DIAG_MINIMAL", self.minimal, cast = bool)
        self.format = appier.conf("DIAG_FORMAT", self.format)
        self.empty = appier.conf("DIAG_EMPTY", self.empty, cast = bool)
        self._loggly_api = None
        self._logstash_api = None
        self._hostname_s = None

        # normalizes the verbosity level values and sets the extra values (verbose
        # and minimal) in case the values have been provided
        self.level = self.level.lower()
        if self.verbose: self.level = "verbose"
        if self.minimal: self.level = "minimal"

    def version(self):
        return base.VERSION

    def info(self):
        info = appier.Part.info(self)
        info.update(
            store = self.store,
            loggly = self.loggly,
            logstash = self.logstash,
            output = self.output,
            format = self.format
        )
        return info

    def load(self):
        appier.Part.load(self)

        if self.owner.admin_part:
            self.owner.admin_part.add_section_item(
                "Requests", "diag.list_requests",
                section = "Diag"
            )

        appier.App.add_custom("before_request", self.before_request)
        appier.App.add_custom("after_request", self.after_request)

        # in case the empty flag is set the complete set of
        # request entities in the data store are deleted
        if self.empty: models.DiagRequest.delete_c()

    def unload(self):
        appier.Part.unload(self)

        if self.owner.admin_part:
            self.owner.admin_part.remove_section_item(
                "Requests",
                section = "Diag"
            )

        appier.App.remove_custom("before_request", self.before_request)
        appier.App.remove_custom("after_request", self.after_request)

        self.flush_all()

    def routes(self):
        return [
            (("GET",), "/admin/diag/requests", self.list_requests),
            (("GET",), "/admin/diag/requests/<int:id>", self.show_request)
        ]

    def models(self):
        return models

    def before_request(self):
        pass

    def after_request(self):
        try:
            if self.output: self._output_log()
            if self.store: self._store_log()
            if self.loggly: self._loggly_log()
            if self.logstash: self._logstash_log()
        except BaseException as exception:
            self.owner.log_error(
                exception,
                message = "Problem running diag logging: %s"
            )

    def flush_all(self):
        self._loggly_flush()
        self._logstash_flush()

    @appier.ensure(token = "admin.status")
    def list_requests(self):
        object = appier.get_object(
            alias = True,
            page = True,
            find = True,
            sort = (("id", -1),)
        )
        page = models.DiagRequest.paginate(**object)
        requests = models.DiagRequest.find(meta = True, **object)
        return self.template(
            "request/list.html.tpl",
            section = "section:diag:requests",
            page = page,
            requests = requests,
            model = models.DiagRequest
        )

    @appier.ensure(token = "admin.status")
    def show_request(self, id):
        return self.template(
            "request/show.html.tpl",
            section = "section:diag:requests",
            request = models.DiagRequest.get(id = id)
        )

    def _common_log(self, user = "root"):
        template = "%s - %s [%s] \"%s %s %s\" %d %s"
        return template % (
            self.request.get_address(),
            user,
            self.request.get_sdate(),
            self.request.method,
            self.request.path,
            self.request.protocol,
            self.request.code,
            str(self.request.result_l or "-")
        )

    def _combined_log(self, user = "root"):
        template = "%s - %s [%s] \"%s %s %s\" %d %s \"%s\" \"%s\""
        return template % (
            self.request.get_address(),
            user,
            self.request.get_sdate(),
            self.request.method,
            self.request.path,
            self.request.protocol,
            self.request.code,
            str(self.request.result_l or "-"),
            self.request.get_header("Referer") or "",
            self.request.get_header("User-Agent") or ""
        )

    def _output_log(self):
        method = getattr(self, "_%s_log" % self.format)
        result = method()
        print(result)

    def _store_log(self):
        browser_info = self.request.browser_info
        browser_info = browser_info or dict()
        diag_request = models.DiagRequest(
            address = self.request.get_address(),
            url = self.request.get_url(),
            method = self.request.method,
            path = self.request.path,
            query = self.request.query,
            code = self.request.code,
            protocol = self.request.protocol,
            duration = self.request.duration,
            browser = self._browser,
            headers = self.request.in_headers,
            browser_info = self.request.browser_info,
            meta_info = self._meta_info,
            geo_info = self._geo_info
        )
        diag_request.save()

    def _loggly_log(self):
        api = self._get_loggly_api()
        if not api: return
        item = self._get_item(format = self.level)
        api.log_buffer(item)

    def _loggly_flush(self):
        if not self._loggly_api: return
        api = self._get_loggly_api()
        api.log_flush()

    def _logstash_log(self):
        api = self._get_logstash_api()
        if not api: return
        item = self._get_item(format = self.level)
        api.log_buffer(item)

    def _logstash_flush(self):
        if not self._logstash_api: return
        api = self._get_logstash_api()
        api.log_flush()

    def _get_loggly_api(self):
        if self._loggly_api: return self._loggly_api
        try: loggly = appier.import_pip("loggly", package = "loggly_api_python")
        except: loggly = None
        if not loggly: return None
        self._loggly_api = loggly.API(delayer = self.owner.delay)
        return self._loggly_api

    def _get_logstash_api(self):
        if self._logstash_api: return self._logstash_api
        try: logstash = appier.import_pip("logstash", package = "logstash_api")
        except: logstash = None
        if not logstash: return None
        self._logstash_api = logstash.API(delayer = self.owner.delay)
        return self._logstash_api

    def _get_item(self, format = "normal"):
        method = getattr(self, "_get_item_" + format)
        return method()

    def _get_item_base(self):
        return dict()

    def _get_item_minimal(self):
        item = self._get_item_base()
        item.update(
            timestamp = self._timestamp,
            address = self.request.get_address(),
            url = self.request.get_url(),
            method = self.request.method,
            path = self.request.path,
            query = self.request.query,
            code = self.request.code
        )
        return item

    def _get_item_normal(self):
        item = self._get_item_minimal()
        item.update(
            protocol = self.request.protocol,
            duration = self.request.duration,
            browser = self._browser,
            in_headers = self.request.in_headers,
            out_headers = self.request.out_headers,
            hostname = self._hostname,
            name = self.owner.name_b,
            instance = self.owner.instance,
            appier = appier.VERSION,
            platform = appier.PLATFORM,
            server = self.owner.server_full,
            libraries = self.owner.get_libraries(map = True),
            parts = self.owner.get_parts(simple = True)
        )
        return item

    def _get_item_verbose(self):
        item = self._get_item_normal()
        item.update(
            browser_info = self.request.browser_info,
            meta_info = self._meta_info,
            geo_info = self._geo_info
        )
        if self.request.exception:
            exception = self.request.exception
            item["exception"] = dict(
                name = exception.__class__.__name__,
                uid = exception.uid if hasattr(exception, "uid") else None,
                message = exception.message if hasattr(exception, "message") else None
            )
        if self.request.stacktrace:
            item["stacktrace"] = self.request.stacktrace
        return item

    def _get_item_debug(self):
        item = self._get_item_verbose()
        item.update(
            info_dict = self.owner.info_dict()
        )
        return item

    @property
    def _timestamp(self, format = "%Y-%m-%dT%H:%M:%S"):
        now = datetime.datetime.utcnow()
        return now.strftime(format)

    @property
    def _hostname(self):
        if self._hostname_s: return self._hostname_s
        self._hostname_s = socket.gethostname()
        return self._hostname_s

    @property
    def _browser(self, default = "unknown"):
        browser_info = self.request.browser_info
        browser_info = browser_info or {}
        browser_name = browser_info.get("name", None)
        browser_version = browser_info.get("version", None)
        if browser_name and browser_version:
            return "%s/%s" % (browser_name, browser_version)
        elif browser_name:
            return browser_name
        return default

    @property
    def _meta_info(self):
        return dict(
            is_mobile = self.request.is_mobile(),
            is_tablet = self.request.is_tablet(),
            is_browser = self.request.is_browser(),
            is_bot = self.request.is_bot()
        )

    @property
    def _geo_info(self):
        if not self.geo: return {}
        address = self.request.get_address()
        return appier.GeoResolver.resolve(address) or {}
