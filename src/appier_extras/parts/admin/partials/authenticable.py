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


class Authenticable(appier.Observable):
    @classmethod
    def _unset_account(cls, prefixes=None, safes=[], method="delete"):
        session = appier.get_session()
        _cls = session.get("cls", None)
        if _cls:
            cls = appier.get_model(_cls)
        cls._unset_session(prefixes=prefixes, safes=safes, method=method)
        Authenticable.trigger_g(
            "unset_account", prefixes=prefixes, safes=safes, method=method
        )

    @classmethod
    def _unset_session(cls, prefixes=None, safes=[], method="delete"):
        pass

    def _set_account(self, unset=True, safes=[], method="set"):
        self._set_session(unset=unset, safes=safes, method=method)
        Authenticable.trigger_g(
            "set_account", self, unset=unset, safes=safes, method=method
        )

    def _set_session(self, unset=True, safes=[], method="set"):
        pass

    @property
    def two_factor_enabled(self):
        return False
