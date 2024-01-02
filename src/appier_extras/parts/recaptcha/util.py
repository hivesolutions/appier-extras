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

import functools

import appier


def recaptcha_protect(action="default", name="recaptcha_token"):
    def decorator(function):
        @functools.wraps(function)
        def interceptor(self, *args, **kwargs):
            token = self.field(name, None)
            recaptcha_ensure(self, token, action=action)
            return appier.call_safe(function, self, *args, **kwargs)

        return interceptor

    return decorator


def recaptcha_ensure(self, token, action="default", force=False):
    if not _recaptcha_available() and not force:
        return
    secret = appier.conf("RECAPTCHA_SECRET", None)
    min_score = appier.conf("RECAPTCHA_MIN", 0.5)
    result = appier.post(
        "https://www.google.com/recaptcha/api/siteverify",
        params=dict(secret=secret, response=token),
    )
    if result.get("score", 0) >= min_score and result.get("action", None) == action:
        return token
    raise appier.AppierException(message="Invalid reCAPTCHA score or action", code=403)


def _recaptcha_available():
    key = appier.conf("RECAPTCHA_KEY", None)
    secret = appier.conf("RECAPTCHA_SECRET", None)
    return True if key and secret else False
