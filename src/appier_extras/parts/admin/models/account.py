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

    PREFIXES = [
        "fb.",
        "tw.",
        "gg.",
        "gh.",
        "live.",
        "params."
    ]

    ROOT_USERNAME = "root"

    ROOT_PASSWORD = "root"

    ROOT_EMAIL = "root@root.com"

    username = appier.field(
        index = True,
        default = True
    )

    email = appier.field(
        index = True,
        immutable = True,
        meta = "email"
    )

    password = appier.field(
        private = True,
        meta = "secret"
    )

    key = appier.field(
        safe = True,
        private = True,
        meta = "secret"
    )

    reset_token = appier.field(
        safe = True,
        private = True,
        meta = "secret"
    )

    facebook_id = appier.field(
        index = True
    )

    twitter_username = appier.field(
        index = True
    )

    google_id = appier.field(
        index = True
    )

    live_id = appier.field(
        index = True
    )

    github_login = appier.field(
        index = True
    )

    facebook_token = appier.field(
        private = True,
        meta = "secret"
    )

    twitter_token = appier.field(
        private = True,
        meta = "secret"
    )

    google_token = appier.field(
        private = True,
        meta = "secret"
    )

    live_token = appier.field(
        private = True,
        meta = "secret"
    )

    github_token = appier.field(
        private = True,
        meta = "secret"
    )

    type = appier.field(
        type = int,
        initial = USER_TYPE,
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

        # retrieves the reference to the global logger that is going
        # to be used (should be initialized) and then prints the initial
        # information about the account to be generated
        logger = appier.get_logger()
        logger.info("Generating initial root account ...")

        # creates the structure to be used as the root account description
        # using the default value and then stores the account as it's going
        # to be used as the default root entity (for administration)
        account = cls(
            enabled = True,
            username = cls.ROOT_USERNAME,
            email = cls.ROOT_EMAIL,
            password = cls.generate(cls.ROOT_PASSWORD),
            type = cls.ADMIN_TYPE
        )
        account.save(validate = False)

        # tries to retrieve the newly generated account with no rules and then
        # uses it to print information about the newly created account
        account = cls.get(id = account.id, rules = False)
        logger.info("Username: %s" % account.username)
        logger.info("Password: %s" % cls.ROOT_PASSWORD)
        logger.info("Secret Key: %s" % account.key)

    @classmethod
    def validate(cls):
        return super(Account, cls).validate() + [
            appier.not_null("username"),
            appier.not_empty("username"),
            appier.string_gt("username", 3),
            appier.string_lt("username", 64),
            appier.not_duplicate("username", cls._name()),

            appier.not_null("email"),
            appier.not_empty("email"),
            appier.is_email("email"),
            appier.not_duplicate("email", cls._name()),

            appier.not_empty("password"),
            appier.string_gt("password", 3),
            appier.string_lt("password", 256),

            appier.not_null("type"),

            appier.not_empty("password_confirm"),
            appier.string_gt("password_confirm", 3),
            appier.string_lt("password_confirm", 256),
            appier.equals("password_confirm", "password")
        ]

    @classmethod
    def validate_new(cls):
        return super(Account, cls).validate_new() + [
            appier.not_null("password"),

            appier.not_null("password_confirm")
        ]

    @classmethod
    def list_names(cls):
        return ["username", "email", "last_login", "type", "enabled"]

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
            rules = False,
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

        # "touches" the current account meaning that the last login value will be
        # updated to reflect the current time and then returns the current logged
        # in account to the caller method so that it may used (valid account)
        account.touch_s()
        return account

    @classmethod
    def login_key(cls, key):
        # verifies that secret key is provided, is considered valid for domain
        # and that it is correctly and properly defined (required for validation)
        if not key:
            raise appier.OperationalError(
                message = "Secret key must be provided",
                code = 400
            )

        # tries to retrieve the account with the provided username, so that
        # the other validation steps may be done as required by login operation
        account = cls.get(
            key = key,
            rules = False,
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

        # "touches" the current account meaning that the last login value will be
        # updated to reflect the current time and then returns the current logged
        # in account to the caller method so that it may used (valid account)
        account.touch_s()
        return account

    @classmethod
    def recover(cls, identifier):
        # verifies if a valid identifier has been provided because that value
        # is required for the proper account recover process to be executed
        if not identifier:
            raise appier.OperationalError(
                message = "An identifier must be provided",
                code = 400
            )

        # creates the keyword based arguments that are going to be used to provide
        # an extra layer of or based filtering to the retrieval process of the account
        # that is going to be performed next
        kwargs = {
            "$or" : [
                dict(username = identifier),
                dict(email = identifier)
            ]
        }
        account = cls.get(
            build = False,
            raise_e = False,
            **kwargs
        )

        # in case no account has been retrieved an error is raised indicating such
        # problem, as that is required for the account recover process
        if not account:
            raise appier.OperationalError(
                message = "No valid account found",
                code = 403
            )

        # runs the recover instance method that should generate a new reset token
        # for the account and send the proper notifications
        return account.recover_s()

    @classmethod
    def reset(cls, reset_token, password, password_confirm):
        account = cls.validate_token(reset_token)
        account.reset_s(password, password_confirm)
        return account

    @classmethod
    def verify(cls, encoded, decoded):
        type, salt, digest, plain = cls.unpack(encoded)
        if plain: return encoded == decoded
        if salt: decoded += salt
        type = type.lower()
        decoded = appier.legacy.bytes(decoded)
        hash = hashlib.new(type, decoded)
        _digest = hash.hexdigest()
        return _digest == digest

    @classmethod
    def generate(cls, password, type = "sha256", salt = "appier"):
        if cls.is_encrypted(password): return password
        if type == "plain" : return password
        if salt: password += salt
        password = appier.legacy.bytes(password)
        hash = hashlib.new(type, password)
        digest = hash.hexdigest()
        if not salt: return "%s:%s" % (type, digest)
        salt = appier.legacy.bytes(salt)
        salt = binascii.hexlify(salt)
        salt = appier.legacy.str(salt)
        return "%s:%s:%s" % (type, salt, digest)

    @classmethod
    def unpack(cls, password):
        count = password.count(":")
        if count == 2: type, salt, digest = password.split(":")
        elif count == 1: type, digest = password.split(":"); salt = None
        else: plain = password; type = "plain"; salt = None; digest = None
        if not type == "plain": plain = None
        if salt: salt = appier.legacy.bytes(salt)
        if salt: salt = binascii.unhexlify(salt)
        if salt: salt = appier.legacy.str(salt)
        return (type, salt, digest, plain)

    @classmethod
    def validate_token(cls, reset_token):
        account = cls.get(reset_token = reset_token, raise_e = False)
        if account: return account
        raise appier.SecurityError(message = "Invalid reset token")

    @classmethod
    def from_session(cls, *args, **kwargs):
        session = appier.get_session()
        if not "username" in session: return None
        return cls.get(
            username = session["username"],
            *args, **kwargs
        )

    @classmethod
    def is_encrypted(cls, password):
        return password.count(":") > 0

    @classmethod
    @appier.operation(
        name = "Create",
        parameters = (
            ("Username", "username", str),
            ("Email", "email", str),
            ("Password", "password", str),
            ("Send Email", "send_email", bool, False)
        ),
        factory = True
    )
    def create_s(cls, username, email, password, send_email):
        account = cls(
            username = username,
            email = email,
            password = password,
            password_confirm = password
        )
        account.save()
        if send_email: account.email_new(password = password)
        return account

    @classmethod
    def _unset_session(cls, prefixes = None, safes = [], method = "delete"):
        prefixes = prefixes or cls.PREFIXES
        session = appier.get_session()
        delete = getattr(session, method)
        if "username" in session: delete("username")
        if "name" in session: delete("name")
        if "email" in session: delete("email")
        if "type" in session: delete("type")
        if "tokens" in session: delete("tokens")
        if "meta" in session: delete("meta")
        if "params" in session: delete("params")
        for key in appier.legacy.keys(session):
            is_removable = False
            for prefix in prefixes:
                is_safe = key in safes
                if is_safe: continue
                is_prefix = key.startswith(prefix)
                if not is_prefix: continue
                is_removable = True
                break
            if not is_removable: continue
            delete(key)

    def pre_create(self):
        base.Base.pre_create(self)
        self.key = self.secret()

    def pre_save(self):
        base.Base.pre_save(self)
        if hasattr(self, "password") and self.password:
            self.password = self.encrypt(self.password)

    def touch_s(self):
        # updates the last login of the account with the current timestamp
        # and saves the account so that this value is persisted
        self.last_login = time.time()
        self.save()

    def recover_s(self):
        self.reset_token = self.secret()
        self.save()
        self.email_recover()
        return self.reset_token

    def reset_s(self, password, password_confirm):
        if not password:
            raise appier.OperationalError(
                message = "No password provided",
                code = 400
            )
        if not password == password_confirm:
            raise appier.OperationalError(
                message = "Invalid password confirmation",
                code = 400
            )
        self.password = password
        self.password_confirm = password_confirm
        self.reset_token = None
        self.save()

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

    @property
    def email_f(self):
        if not self.email: return self.email
        if not self.username: return self.email
        return "%s <%s>" % (self.username, self.email)

    @appier.operation(name = "Generate Key")
    def generate_key_s(self, force = False):
        self = self.reload(rules = False)
        if self.key and not force: return
        self.key = self.secret()
        self.save()

    @appier.operation(name = "Email New")
    def email_new(self, password = None, owner = None):
        owner = owner or appier.get_app()
        account = self.reload(meta = True)
        base.Base.send_email_g(
            owner,
            "admin/email/account/new.html.tpl",
            receivers = [self.email_f],
            subject = "New account",
            title = "New account",
            account = account,
            account_password = password
        )

    @appier.operation(name = "Email Recover")
    def email_recover(self, owner = None):
        owner = owner or appier.get_app()
        account = self.reload(rules = False, meta = True)
        base.Base.send_email_g(
            owner,
            "admin/email/account/recover.html.tpl",
            receivers = [self.email_f],
            subject = "Recover account",
            title = "Recover account",
            account = account
        )

    def _set_session(self, unset = True, safes = [], method = "set"):
        cls = self.__class__
        if unset: cls._unset_session(safes = safes)
        self.session.ensure()
        set = getattr(self.session, method)
        set("username", self.username)
        set("name", self.email)
        set("email", self.email)
        set("type", self.type_s())
        set("tokens", self.tokens())
        set("meta", self.meta)
        set("params", dict())
