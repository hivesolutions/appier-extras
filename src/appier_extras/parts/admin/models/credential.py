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

from appier_extras.parts.admin.models import base


class Credential(base.Base):

    credential_id = appier.field(
        index=True, immutable=True, description="Credential ID"
    )

    credential_data = appier.field()

    account = appier.field(type=appier.reference("Account", name="id"))

    @classmethod
    def validate(cls):
        return super(Credential, cls).validate() + [
            appier.not_null("credential_id"),
            appier.not_empty("credential_id"),
            appier.not_null("credential_data"),
            appier.not_empty("credential_data"),
        ]

    @classmethod
    def list_names(cls):
        return ["credential_id", "description", "account"]

    def post_save(self):
        base.Base.post_save(self)
        account = self.account.reload()
        if not self in account.credentials:
            account.credentials.append(self)
            account.save()

    @classmethod
    def get_by_credential_id(cls, credential_id, *args, **kwargs):
        return cls.get(credential_id=credential_id, eager=("account",), *args, **kwargs)
