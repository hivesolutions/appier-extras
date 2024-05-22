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

import base64

import appier

from appier_extras.parts.admin.models import base


class Credential(base.Base):
    """
    Model that represents a credential that is associated with
    an account, this credential may be used for authentication
    purposes and may be of different types (eg: FIDO2).

    It is expected that the FIDO2 authentication is going to be
    performed using WebAuthn and the credential is going to be
    created using the `navigator.credentials.create` method.

    Sometimes these credentials are also referred to as "Passkeys".

    :see: https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API
    """

    credential_id = appier.field(
        index=True, immutable=True, description="Credential ID"
    )

    credential_data = appier.field(immutable=True)

    account = appier.field(type=appier.reference("Account", name="id"), immutable=True)

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

    def post_create(self):
        base.Base.post_create(self)

        account = self.account.reload()
        account.credentials.append(self)
        account.fido2_enabled = True
        account.save()

    def post_delete(self):
        base.Base.post_create(self)

        account = self.account.reload()
        if self in account.credentials:
            account.credentials.remove(self)
        if len(account.credentials) == 0:
            account.fido2_enabled = False
        account.save()

    @classmethod
    def get_by_credential_id(cls, credential_id, *args, **kwargs):
        return cls.get(credential_id=credential_id, eager=("account",), *args, **kwargs)

    @classmethod
    def find_by_account(cls, account, *args, **kwargs):
        return cls.find(account=account.id, *args, **kwargs)

    @classmethod
    def credentials_data_account(cls, account, *args, **kwargs):
        credentials = cls.find_by_account(account=account, *args, **kwargs)
        return [
            base64.b64decode(credential.credential_data) for credential in credentials
        ]
