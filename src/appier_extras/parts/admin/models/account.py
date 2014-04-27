#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Appier Framework.
#
# Hive Appier Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Appier Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Appier Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time
import appier
import hashlib
import binascii

from appier_extras.parts.admin.models import base

class Account(base.Base):

    ADMIN_TYPE = 1
    USER_TYPE = 2

    ACCOUNT_S = {
        ADMIN_TYPE : "admin",
        USER_TYPE : "user"
    }

    username = appier.field(
        index = True
    )

    email = appier.field(
        index = True,
        immutable = True
    )

    password = appier.field(
        private = True
    )

    type = appier.field(
        type = int,
        safe = True,
        meta = "enum",
        enum = ACCOUNT_S
    )

    last_login = appier.field(
        type = int,
        safe = True,
        meta = "datetime"
    )

    @classmethod
    def setup(cls):
        super(Account, cls).setup()

        # tries to find the root account (default) in case it's not
        # found returns immediately nothing to be done
        root = cls.find(username = "root")
        if root: return

        # creates the structure to be used as the server description
        # using the values provided as parameters
        account = {
            "enabled" : True,
            "username" : "root",
            "email" : "root@root.com",
            "password" : cls.generate("root"),
            "type" : Account.ADMIN_TYPE
        }
        collection = cls._collection()
        collection.save(account)

    @classmethod
    def validate(cls):
        return super(Account, cls).validate() + [
            appier.not_null("username"),
            appier.not_empty("username"),
            appier.string_gt("username", 3),
            appier.string_lt("username", 20),
            appier.not_duplicate("username", cls._name()),

            appier.not_null("type"),

            appier.equals("password_confirm", "password")
        ]

    @classmethod
    def validate_new(cls):
        return super(Account, cls).validate_new() + [
            appier.not_null("password"),
            appier.not_empty("password"),

            appier.not_null("password_confirm"),
            appier.not_empty("password_confirm")
        ]

    @classmethod
    def extra_names(cls):
        return super(Account, cls).extra_names() + [
            "password_confirm"
        ]

    @classmethod
    def login(cls, username, password):
        # verifies that both the provided username and password are valid
        # and that are correctly and properly defined (required for validation)
        if not username or not password:
            raise appier.OperationalError(
                message = "Both username and password must be provided",
                code = 400
            )

        # tries to retrieve the account with the provided username, so that
        # the other validation steps may be done as required by login operation
        account = cls.get(
            username = username,
            build = False,
            raise_e = False
        )
        if not account:
            raise appier.OperationalError(
                message = "No valid account found",
                code = 403
            )

        # verifies that the retrieved account is currently enabled, because
        # disabled accounts are not considered to be valid ones
        if not account.enabled:
            raise appier.OperationalError(
                message = "Account is not enabled",
                code = 403
            )

        # retrieves the value of the password for the stored account and then
        # verifies that the value matched the one that has been provided
        _password = account.password
        if not cls.verify(_password, password):
            raise appier.OperationalError(
                message = "Invalid or mismatch password",
                code = 403
            )

        # updates the last login of the account with the current timestamp
        # and saves the account so that this value is persisted, then returns
        # the account to the caller method so that it may be used
        account.last_login = time.time()
        account.save()
        return account

    @classmethod
    def verify(cls, encoded, decoded):
        type, salt, digest, plain = cls.unpack(encoded)
        if plain: return encoded == decoded
        if salt: decoded += salt
        type = type.lower()
        decoded = appier.bytes(decoded)
        hash = hashlib.new(type, decoded)
        _digest = hash.hexdigest()
        return _digest == digest

    @classmethod
    def generate(cls, password, type = "sha256", salt = "appier"):
        if cls.is_encrypted(password): return password
        if type == "plain" : return password
        if salt: password += salt
        password = appier.bytes(password)
        hash = hashlib.new(type, password)
        digest = hash.hexdigest()
        if not salt: return "%s:%s" % (type, digest)
        salt = appier.bytes(salt)
        salt = binascii.hexlify(salt)
        salt = appier.str(salt)
        return "%s:%s:%s" % (type, salt, digest)

    @classmethod
    def unpack(cls, password):
        count = password.count(":")
        if count == 2: type, salt, digest = password.split(":")
        elif count == 1: type, digest = password.split(":"); salt = None
        else: plain = password; type = "plain"; salt = None; digest = None
        if not type == "plain": plain = None
        if salt: salt = appier.bytes(salt)
        if salt: salt = binascii.unhexlify(salt)
        if salt: salt = appier.str(salt)
        return (type, salt, digest, plain)

    @classmethod
    def is_encrypted(cls, password):
        return password.count(":") > 0

    def pre_save(self):
        base.Base.pre_save(self)
        if hasattr(self, "password"): self.password = self.encrypt(self.password)

    def tokens(self):
        if self.type == Account.ADMIN_TYPE:
            return ["*"]

        if self.type == Account.USER_TYPE:
            return ["base", "user"]

    def type_s(self, capitalize = False):
        type_s = Account.ACCOUNT_S.get(self.type, None)
        type_s = type_s.capitalize() if capitalize else type_s
        return type_s

    def encrypt(self, value):
        cls = self.__class__
        return cls.generate(value)
