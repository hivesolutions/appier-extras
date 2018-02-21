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

from appier_extras import base

from appier_extras.parts.diag import models

class DiagPart(appier.Part):
    """
    Modular part class that provides an infra-structure of diagnostics
    that allow more and better debugging of an Application.
    """

    def __init__(self, *args, **kwargs):
        appier.Part.__init__(self, *args, **kwargs)
        self.store = kwargs.get("store", True)
        self.output = kwargs.get("output", True)
        self.format = kwargs.get("format", "combined")
        self.store = appier.conf("DIAG_STORE", self.store, cast = bool)
        self.output = appier.conf("DIAG_OUTPUT", self.output, cast = bool)
        self.format = appier.conf("DIAG_FORMAT", self.format)

    def version(self):
        return base.VERSION

    def info(self):
        info = appier.Part.info(self)
        info.update(
            store = self.store,
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

    def unload(self):
        appier.Part.unload(self)

        if self.owner.admin_part:
            self.owner.admin_part.remove_section_item(
                "Requests",
                section = "Diag"
            )

        appier.App.remove_custom("before_request", self.before_request)
        appier.App.remove_custom("after_request", self.after_request)

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
        method = getattr(self, "_%s_log" % self.format)
        result = method()
        if self.output: print(result)
        if self.store: self._store_log()

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
            self.request.address,
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
            self.request.address,
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

    def _store_log(self):
        browser_info = self.request.browser_info
        diag_request = models.DiagRequest(
            address = self.request.address,
            method = self.request.method,
            path = self.request.path,
            query = self.request.query,
            code = self.request.code,
            protocol = self.request.protocol,
            browser = "%s/%s" % (browser_info["name"], browser_info["version"]),
            headers = self.request.in_headers,
            browser_info = browser_info
        )
        diag_request.save()
