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

from appier_extras import base

from . import util


class ReCaptchaPart(appier.Part):
    """
    Modular part class that provides the required infra-structure
    for the control of Google's reCAPTCHA service.

    Should be used with proper knowledge of the inner workings of
    the captcha mechanism to avoid any security problems.

    :see: https://developers.google.com/recaptcha
    """

    def version(self):
        return base.VERSION

    def load(self):
        appier.Part.load(self)

        self.owner.context["recaptcha"] = self.recaptcha
        self.owner.context["recaptcha_input"] = self.recaptcha_input
        self.owner.context["recaptcha_script"] = self.recaptcha_script
        self.owner.context["recaptcha_available"] = self.recaptcha_available

    def recaptcha(self, action="default", name="recaptcha_token", force=False):
        if not util._recaptcha_available() and not force:
            return ""
        return self.owner.escape_template(
            self._build_input(name) + self._build_script(action)
        )

    def recaptcha_input(self, name="recaptcha_token", force=False):
        if not util._recaptcha_available() and not force:
            return ""
        return self.owner.escape_template(self._build_input(name))

    def recaptcha_script(self, action="default", force=False):
        if not util._recaptcha_available() and not force:
            return ""
        return self.owner.escape_template(self._build_script(action))

    def recaptcha_available(self):
        return util._recaptcha_available()

    def _build_input(self, name):
        return '<input type="hidden" id="recaptcha-token" name="%s" />' % name

    def _build_script(self, action):
        recaptcha_key = appier.conf("RECAPTCHA_KEY", None)
        appier.verify(recaptcha_key, message="No reCAPTCHA site key provided")
        return (
            '<script type="application/javascript" src="https://www.google.com/recaptcha/api.js?render=%s"></script>'
            % recaptcha_key
            + '<script type="application/javascript">window.genRecaptcha = function () {'
            + "grecaptcha.ready(function () {"
            + 'var elements = document.querySelectorAll("[name=recaptcha_token], #recaptcha-token");'
            + "for (var index = 0; index < elements.length; index++) {"
            + "(function () {"
            + "var element = elements[index];"
            + 'grecaptcha.execute("%s", {action: "%s"}).then(function (token) {'
            % (recaptcha_key, action)
            + "element.value = token;"
            + "});"
            + "})();"
            + "}"
            + "});"
            + "};"
            + "window.genRecaptcha();"
            + "</script>"
        )
