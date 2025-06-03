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

import json
import time
import base64
import hashlib
import binascii

import appier

from appier_extras import utils

from appier_extras.parts.admin.models import base
from appier_extras.parts.admin.models import role
from appier_extras.parts.admin.partials import authenticable


class Account(base.Base, authenticable.Authenticable):
    ADMIN_TYPE = 1
    USER_TYPE = 2
    ROLE_TYPE = 3

    ACCOUNT_S = {ADMIN_TYPE: "admin", USER_TYPE: "user", ROLE_TYPE: "role"}

    PREFIXES = ["fb.", "tw.", "gg.", "gh.", "live.", "params."]

    ROOT_USERNAME = "root"

    ROOT_PASSWORD = "root"

    ROOT_EMAIL = "root@root.com"

    username = appier.field(index="all", default=True)

    email = appier.field(index="all", immutable=True, meta="email")

    password = appier.field(private=True, meta="secret")

    key = appier.field(safe=True, private=True, meta="secret")

    reset_token = appier.field(safe=True, private=True, meta="secret")

    confirmation_token = appier.field(safe=True, private=True, meta="secret")

    fido2_enabled = appier.field(type=bool, description="FIDO2 Enabled")

    otp_enabled = appier.field(type=bool, description="OTP Enabled")

    otp_secret = appier.field(
        safe=True, private=True, meta="secret", description="OTP Secret"
    )

    facebook_id = appier.field(index="hashed", safe=True, description="Facebook ID")

    github_login = appier.field(index="hashed", safe=True, description="GitHub Login")

    google_id = appier.field(index="hashed", safe=True, description="Google ID")

    live_id = appier.field(index="hashed", safe=True, description="Live ID")

    twitter_username = appier.field(index="hashed", safe=True)

    facebook_token = appier.field(private=True, meta="secret")

    github_token = appier.field(private=True, meta="secret", description="GitHub Token")

    google_token = appier.field(private=True, meta="secret")

    live_token = appier.field(private=True, meta="secret")

    twitter_token = appier.field(private=True, meta="secret")

    type = appier.field(
        type=int, initial=USER_TYPE, safe=True, meta="enum", enum=ACCOUNT_S
    )

    last_login = appier.field(type=int, safe=True, meta="datetime")

    avatar = appier.field(
        type=appier.image(width=400, height=400, format="png"), private=True
    )

    roles = appier.field(type=appier.references("Role", name="id"))

    credentials = appier.field(type=appier.references("Credential", name="id"))

    @classmethod
    def setup(cls):
        super(Account, cls).setup()

        # tries to find the root account (default) in case it's not
        # found returns immediately nothing to be done
        root = cls.find(username="root")
        if root:
            return

        # retrieves the reference to the global logger that is going
        # to be used (should be initialized) and then prints the initial
        # information about the account to be generated
        logger = appier.get_logger()
        logger.info("Generating initial root account for %s model ..." % cls.__name__)

        # creates the structure to be used as the root account description
        # using the default value and then stores the account as it's going
        # to be used as the default root entity (for administration)
        password = appier.conf("ADMIN_PASSWORD", cls.ROOT_PASSWORD)
        account = cls(
            enabled=True,
            username=cls.ROOT_USERNAME,
            email=cls.ROOT_EMAIL,
            password=cls.generate(password),
            type=cls.ADMIN_TYPE,
        )
        account.save(validate=False)

        # tries to retrieve the newly generated account with no rules and then
        # uses it to print information about the newly created account
        account = cls.get(id=account.id, rules=False)
        logger.info("Username: %s" % account.username)
        logger.info("Password: %s" % password)
        logger.info("Secret Key: %s" % account.key)

    @classmethod
    def validate(cls):
        return super(Account, cls).validate() + [
            appier.not_null("username"),
            appier.not_empty("username"),
            appier.is_lower("username"),
            appier.string_gt("username", 3),
            appier.string_lt("username", 64),
            appier.not_duplicate("username", cls._name()),
            appier.not_null("email"),
            appier.not_empty("email"),
            appier.is_lower("email"),
            appier.is_email("email"),
            appier.not_duplicate("email", cls._name()),
            appier.not_empty("password"),
            appier.string_gt("password", 3),
            appier.string_lt("password", 256),
            appier.not_duplicate("key", cls._name()),
            appier.not_null("type"),
            appier.not_empty("password_confirm"),
            appier.string_gt("password_confirm", 3),
            appier.string_lt("password_confirm", 256),
            appier.equals("password_confirm", "password"),
        ]

    @classmethod
    def validate_new(cls):
        return super(Account, cls).validate_new() + [
            appier.not_null("password"),
            appier.not_null("password_confirm"),
        ]

    @classmethod
    def list_names(cls):
        return ["username", "email", "last_login", "type", "enabled"]

    @classmethod
    def extra_names(cls):
        return super(Account, cls).extra_names() + ["password_confirm"]

    @classmethod
    def login(cls, username, password, insensitive=True, touch=True):
        # in case the (case) insensitive option is enabled and the username
        # is defined the value is converted to lower case so that a proper
        # comparison may be used (not case sensitive)
        if insensitive and username:
            username = username.lower()

        # verifies that both the provided username and password are valid
        # and that are correctly and properly defined (required for validation)
        if not username or not password:
            raise appier.OperationalError(
                message="Both username and password must be provided", code=400
            )

        # tries to retrieve the account with the provided username, so that
        # the other validation steps may be done as required by login operation
        account = cls.get(username=username, rules=False, build=False, raise_e=False)
        if not account:
            raise appier.OperationalError(message="No valid account found", code=403)

        # verifies that the retrieved account is currently enabled, because
        # disabled accounts are not considered to be valid ones
        if not account.enabled:
            raise appier.OperationalError(message="Account is not enabled", code=403)

        # retrieves the value of the password for the stored account and then
        # verifies that the value matched the one that has been provided
        _password = account.password
        if not cls.verify(_password, password):
            raise appier.OperationalError(
                message="Invalid or mismatch password", code=403
            )

        # "touches" the current account meaning that the last login value will be
        # updated to reflect the current time and then returns the current logged
        # in account to the caller method so that it may used (valid account)
        if touch:
            account.touch_login_s()
        return account

    @classmethod
    def login_key(cls, key, touch=True):
        # verifies that secret key is provided, is considered valid for domain
        # and that it is correctly and properly defined (required for validation)
        if not key:
            raise appier.OperationalError(
                message="Secret key must be provided", code=400
            )

        # tries to retrieve the account with the provided key, so that
        # the other validation steps may be done as required by login operation
        account = cls.get(key=key, rules=False, build=False, raise_e=False)
        if not account:
            raise appier.OperationalError(message="No valid account found", code=403)

        # verifies that the retrieved account is currently enabled, because
        # disabled accounts are not considered to be valid ones
        if not account.enabled:
            raise appier.OperationalError(message="Account is not enabled", code=403)

        # "touches" the current account meaning that the last login value will be
        # updated to reflect the current time and then returns the current logged
        # in account to the caller method so that it may used (valid account)
        if touch:
            account.touch_login_s()
        return account

    @classmethod
    def login_otp(cls, username, otp_token, touch=True):
        # verifies that OTP token is provided, this value is mandatory to
        # be able to properly validate OTP
        if not otp_token:
            raise appier.OperationalError(
                message="OTP token must be provided", code=400
            )

        # tries to retrieve the account with the provided username, so that
        # the other validation steps may be done as required by login operation
        account = cls.get(username=username, rules=False, build=False, raise_e=False)
        if not account:
            raise appier.OperationalError(message="No valid account found", code=403)

        # verifies that the retrieved account is currently enabled, because
        # disabled accounts are not considered to be valid ones
        if not account.enabled:
            raise appier.OperationalError(message="Account is not enabled", code=403)

        # verifies that the OTP token provided is valid for the current account
        # and if that's not the case raises an exception indicating the problem
        account.verify_otp(otp_token)

        # "touches" the current account meaning that the last login value will be
        # updated to reflect the current time and then returns the current logged
        # in account to the caller method so that it may used (valid account)
        if touch:
            account.touch_login_s()
        return account

    @classmethod
    def login_begin_fido2(cls, username):
        #  tries to retrieve the account with the provided username, so that
        # the other validation steps may be done as required by login operation
        account = cls.get(username=username, rules=False, build=False, raise_e=False)
        if not account:
            raise appier.OperationalError(message="No valid account found", code=403)

        # verifies that the retrieved account is currently enabled, because
        # disabled accounts are not considered to be valid ones
        if not account.enabled:
            raise appier.OperationalError(message="Account is not enabled", code=403)

        fido2_server = cls._get_fido2_server()
        auth_data, state = fido2_server.authenticate_begin(account.credentials_data_n)
        state_json = json.dumps(state)

        auth_data_d = dict(auth_data)
        auth_data_json = json.dumps(auth_data_d, cls=utils.BytesEncoder)

        return state_json, auth_data_json

    @classmethod
    def login_fido2(cls, username, state, response_data, touch=True):
        if not state:
            raise appier.OperationalError(
                message="FIDO2 state must be provided", code=400
            )

        if not response_data:
            raise appier.OperationalError(
                message="FIDO2 response data must be provided", code=400
            )

        # tries to retrieve the account with the provided username, so that
        # the other validation steps may be done as required by login operation
        account = cls.get(username=username, rules=False, build=False, raise_e=False)
        if not account:
            raise appier.OperationalError(message="No valid account found", code=403)

        # verifies that the retrieved account is currently enabled, because
        # disabled accounts are not considered to be valid ones
        if not account.enabled:
            raise appier.OperationalError(message="Account is not enabled", code=403)

        # obtains the FIDO2 server and runs the authentication complete operation
        # using the current session state and the credential data, if the
        # authentication fails an exception is raised
        fido2_server = cls._get_fido2_server()
        fido2_server.authenticate_complete(
            state, account.credentials_data_n, response_data
        )

        # "touches" the current account meaning that the last login value will be
        # updated to reflect the current time and then returns the current logged
        # in account to the caller method so that it may used (valid account)
        if touch:
            account.touch_login_s()
        return account

    @classmethod
    def confirm(cls, confirmation_token, send_email=False):
        # validates the current account and token for confirmation and
        # if that's valid runs the confirm operation and returns the account
        # associated to the caller method
        account = cls.validate_confirmation(confirmation_token)
        account.confirm_s(send_email=send_email)
        return account

    @classmethod
    def recover(cls, identifier, send_email=False):
        # verifies if a valid identifier has been provided because that value
        # is required for the proper account recover process to be executed
        if not identifier:
            raise appier.OperationalError(
                message="An identifier must be provided", code=400
            )

        # creates the keyword based arguments that are going to be used to provide
        # an extra layer of or based filtering to the retrieval process of the account
        # that is going to be performed next
        kwargs = {"$or": [dict(username=identifier), dict(email=identifier)]}
        account = cls.get(build=False, raise_e=False, **kwargs)

        # in case no account has been retrieved an error is raised indicating such
        # problem, as that is required for the account recover process
        if not account:
            raise appier.OperationalError(message="No valid account found", code=403)

        # runs the recover instance method that should generate a new reset token
        # for the account and send the proper notifications
        return account.recover_s(send_email=send_email)

    @classmethod
    def reset(cls, reset_token, password, password_confirm, confirm=True):
        account = cls.validate_reset(reset_token)
        if confirm:
            account.confirm_s()
        account.reset_s(password, password_confirm)
        return account

    @classmethod
    def verify(cls, encoded, decoded):
        type, salt, digest, plain = cls.unpack(encoded)
        if plain:
            return encoded == decoded
        if salt:
            decoded += salt
        type = type.lower()
        decoded = appier.legacy.bytes(decoded)
        hash = hashlib.new(type, decoded)
        _digest = hash.hexdigest()
        return _digest == digest

    @classmethod
    def generate(cls, password, type="sha256", salt="appier"):
        if cls.is_encrypted(password):
            return password
        if type == "plain":
            return password
        if salt:
            password += salt
        password = appier.legacy.bytes(password)
        hash = hashlib.new(type, password)
        digest = hash.hexdigest()
        if not salt:
            return "%s:%s" % (type, digest)
        salt = appier.legacy.bytes(salt)
        salt = binascii.hexlify(salt)
        salt = appier.legacy.str(salt)
        return "%s:%s:%s" % (type, salt, digest)

    @classmethod
    def unpack(cls, password):
        count = password.count(":")
        if count == 2:
            type, salt, digest = password.split(":")
        elif count == 1:
            type, digest = password.split(":")
            salt = None
        else:
            plain = password
            type = "plain"
            salt = None
            digest = None
        if not type == "plain":
            plain = None
        if salt:
            salt = appier.legacy.bytes(salt)
        if salt:
            salt = binascii.unhexlify(salt)
        if salt:
            salt = appier.legacy.str(salt)
        return (type, salt, digest, plain)

    @classmethod
    def validate_reset(cls, reset_token):
        account = cls.get(reset_token=reset_token, raise_e=False)
        if account:
            return account
        raise appier.SecurityError(message="Invalid reset token")

    @classmethod
    def validate_confirmation(cls, confirmation_token):
        account = cls.get(confirmation_token=confirmation_token, raise_e=False)
        if account:
            return account
        raise appier.SecurityError(message="Invalid confirmation token")

    @classmethod
    def from_session(cls, *args, **kwargs):
        session = appier.get_session()
        if not "username" in session:
            return None
        return cls.get(username=session["username"], *args, **kwargs)

    @classmethod
    def is_encrypted(cls, password):
        return password.count(":") > 0

    @classmethod
    @appier.operation(
        name="Create",
        description="""Create a new account with the provided
        username, email and password, in case no password is
        provided a random new one is generated""",
        parameters=(
            ("Username", "username", str),
            ("Email", "email", str),
            ("Password", "password", str, ""),
            ("Send Email", "send_email", bool, False),
        ),
        factory=True,
    )
    def create_s(cls, username, email, password="", send_email=False):
        if not password:
            password = appier.gen_token(limit=16)
        account = cls(
            username=username, email=email, password=password, password_confirm=password
        )
        account.save()
        if send_email:
            account.email_new(password=password)
        return account

    @classmethod
    @appier.operation(
        name="Import JSON",
        parameters=(
            ("JSON File", "file", "file"),
            ("Empty source", "empty", bool, False),
        ),
    )
    def import_json_s(cls, file, empty):
        def callback(item):
            enabled = item["enabled"]
            username = item["username"]
            type = item["type"]
            password = item.get("password", None)
            email = item.get("email", None)
            key = item.get("key", None)
            description = item.get("description", None)
            last_login = item.get("last_login", None)
            avatar = item.get("avatar", None)
            roles = item.get("roles", [])
            account = cls(
                enabled=enabled,
                username=username,
                type=type,
                password=password,
                password_confirm=password,
                email=email,
                key=key,
                description=description,
                last_login=last_login,
                avatar=avatar,
                roles=roles,
            )
            account.save()

        if empty:
            cls.delete_c()
        cls._json_import(file, callback)

    @classmethod
    @appier.operation(
        name="Import CSV",
        parameters=(
            ("CSV File", "file", "file"),
            ("Empty source", "empty", bool, False),
        ),
    )
    def import_csv_s(cls, file, empty=False):
        def callback(line):
            username, password, email, type = line

            if type and type == "admin":
                type = cls.ADMIN_TYPE
            else:
                type = cls.USER_TYPE

            account = cls(
                enabled=True,
                username=username,
                email=email,
                password=password,
                password_confirm=password,
                type=type,
            )
            account.save()

        if empty:
            cls.delete_c()
        cls._csv_import(file, callback)

    @classmethod
    def _build(cls, model, map):
        super(Account, cls)._build(model, map)
        username = model["username"]
        model["avatar_url"] = cls._get_avatar_url_g(username)

    @classmethod
    def _unset_session(cls, prefixes=None, safes=[], method="delete", two_factor=True):
        prefixes = prefixes or cls.PREFIXES
        session = appier.get_session()
        delete = getattr(session, method)
        if "cls" in session:
            delete("cls")
        if "username" in session:
            delete("username")
        if "name" in session:
            delete("name")
        if "email" in session:
            delete("email")
        if "type" in session:
            delete("type")
        if "tokens" in session:
            delete("tokens")
        if "views" in session:
            delete("views")
        if "meta" in session:
            delete("meta")
        if "params" in session:
            delete("params")
        for key in appier.legacy.keys(session):
            is_removable = False
            for prefix in prefixes:
                is_safe = key in safes
                if is_safe:
                    continue
                is_prefix = key.startswith(prefix)
                if not is_prefix:
                    continue
                is_removable = True
                break
            if not is_removable:
                continue
            delete(key)
        if two_factor:
            cls._unset_2fa(method=method)

    @classmethod
    def _unset_2fa(cls, method="delete"):
        session = appier.get_session()
        delete = getattr(session, method)
        if "2fa.timeout" in session:
            delete("2fa.timeout")
        if "2fa.username" in session:
            delete("2fa.username")
        if "2fa.method" in session:
            delete("2fa.method")

    @classmethod
    def _get_avatar_url_g(cls, username, absolute=True, owner=None):
        owner = owner or appier.get_app()
        if not hasattr(owner, "admin_part"):
            return None
        model = None if cls._is_master() else cls._name()
        return owner.url_for(
            "admin.avatar_account", username=username, cls=model, absolute=absolute
        )

    @classmethod
    def _is_master(cls, owner=None):
        owner = owner or appier.get_app()
        admin_part = owner.admin_part
        return cls == admin_part.account_c

    @classmethod
    def _get_fido2_server(cls):
        if hasattr(cls, "_fido2_server") and cls._fido2_server:
            return cls._fido2_server

        _fido2 = appier.import_pip("fido2")

        import fido2.webauthn
        import fido2.server

        owner = owner or appier.get_app()

        base_url = owner.base_url()
        base_domain = appier.legacy.urlparse(base_url).netloc.split(":")[0]

        fido2.webauthn.webauthn_json_mapping.enabled = True
        rp = fido2.webauthn.PublicKeyCredentialRpEntity(
            name=owner.description, id=base_domain
        )
        cls._fido2_server = fido2.server.Fido2Server(rp, verify_origin=lambda _: True)

        return cls._fido2_server

    def pre_validate(self):
        base.Base.pre_validate(self)
        if hasattr(self, "username") and self.username:
            self.username = self.username.lower()
        if hasattr(self, "email") and self.email:
            self.email = self.email.lower()
        if hasattr(self, "roles") and len(self.roles_l) > 0:
            self.type = Account.ROLE_TYPE

    def pre_save(self):
        base.Base.pre_save(self)
        if hasattr(self, "password") and self.password:
            self.password = self.encrypt(self.password)

    def pre_create(self):
        base.Base.pre_create(self)
        if not hasattr(self, "key") or not self.key:
            self.key = self.secret()
        if not hasattr(self, "confirmation_token") or not self.confirmation_token:
            self.confirmation_token = self.secret()
        if not hasattr(self, "avatar") or not self.avatar:
            self._set_avatar_d()

    def confirm_s(self, send_email=False):
        self.confirmation_token = None
        self.enabled = True
        if send_email:
            self.email_confirm()
        self.save()

    def recover_s(self, send_email=False):
        self.reset_token = self.secret()
        self.save()
        if send_email:
            self.email_recover()
        return self.reset_token

    def reset_s(self, password, password_confirm):
        if not password:
            raise appier.OperationalError(message="No password provided", code=400)
        if not password == password_confirm:
            raise appier.OperationalError(
                message="Invalid password confirmation", code=400
            )
        self.password = password
        self.password_confirm = password_confirm
        self.reset_token = None
        self.save()

    def tokens(self):
        """
        Retrieves the complete set of ACL tokens for the current use
        respecting the wild card based selection if there's such use.

        These should consider both dynamic and static role users.

        This method has a critical impact on overall system security.

        :rtype: List
        :return: The ACL tokens list taking into consideration the complete
        aggregated set of roles of the user.
        """

        tokens = set()

        if self.type == Account.ADMIN_TYPE:
            tokens.update(["*"])

        if self.type == Account.USER_TYPE:
            tokens.update(["base", "user"])

        for role in self.roles_s:
            tokens.update(role.tokens_a)

        if "*" in tokens:
            tokens = ["*"]

        tokens = list(tokens)
        tokens.sort()

        return tokens

    def views_l(self):
        """
        Retrieves the complete set of views for the current account,
        these should take into consideration the account's roles.

        Aggregation of the multiple views should be done in a linear
        fashion with the first being the most relevant one.

        :rtype: List
        :return: The list of view maps that should be applied for proper
        context filtering of the user (result set constrain).
        """

        views = []
        for role in self.roles_s:
            view_m = role.view_m(context=self)
            if not view_m:
                continue
            views.append(view_m)
        return views

    def meta_m(self, join=False):
        """
        Merges the metadata dictionary of the current account to the ones
        defined in the complete set of associated roles.

        :type join: bool
        :param join: If the overlapping values between the operations
        should be merged as sequences.
        :rtype: Dictionary
        :return: The final meta-data dictionary that contains the "merged"
        view of the metadata for the account according to the associated
        set of roles.
        """

        meta = dict(self.meta)
        for role in self.roles_s:
            if join:
                self._join_m(role.meta_a, meta)
            else:
                meta.update(role.meta_a)
        return meta

    def secrets_m(self, join=False):
        """
        Merges the secrets dictionary of the current account to the ones
        (secret) defined in the complete set of associated roles.

        :type join: bool
        :param join: If the overlapping values between the operations
        should be merged as sequences.
        :rtype: Dictionary
        :return: The final secrets dictionary that contains the "merged"
        view of the secrets for the account according to the associated
        set of roles.
        """

        secrets = dict(self.secrets)
        for role in self.roles_l:
            if join:
                self._join_m(role.secrets_a, secrets)
            else:
                secrets.update(role.secrets_a)
        return secrets

    def type_s(self, capitalize=False):
        type_s = Account.ACCOUNT_S.get(self.type, None)
        type_s = type_s.capitalize() if capitalize else type_s
        return type_s

    def encrypt(self, value):
        cls = self.__class__
        return cls.generate(value)

    def verify_otp(self, otp_token):
        pyotp = appier.import_pip("pyotp")
        self = self.reload(rules=False)
        totp = pyotp.TOTP(self.otp_secret)
        if not totp.verify(otp_token):
            raise appier.OperationalError(message="Invalid OTP code", code=403)

    def register_begin_fido2(self):
        cls = self.__class__
        fido2_server = cls._get_fido2_server()

        registration_data, state = fido2_server.register_begin(
            dict(
                id=appier.legacy.bytes(self.username, encoding="utf-8"),
                name=self.username,
                displayName=self.username,
            ),
            user_verification="discouraged",
        )
        state_json = json.dumps(state)
        self.session["state"] = state_json

        registration_data_d = dict(registration_data)
        registration_data_json = json.dumps(registration_data_d, cls=utils.BytesEncoder)

        return registration_data_json

    def register_fido2(self, state, credential_data):
        cls = self.__class__

        # obtains the FIDO2 server and runs the registration complete operation
        # using the current session state and the credential data, if the
        # registration fails an exception is raised
        fido2_server = cls._get_fido2_server()
        auth_data = fido2_server.register_complete(state, credential_data)

        # converts the credential data into a Base64 encoded string
        # the strings is structured in the WebAuthn standard format
        credential_id_b64 = appier.legacy.str(
            base64.b64encode(auth_data.credential_data.credential_id)
        )
        credential_data_b64 = appier.legacy.str(
            base64.b64encode(auth_data.credential_data)
        )

        # adds the new credential to the account effectively enabling
        # FIDO2 based authentication for the account
        self.add_credential_s(credential_id_b64, credential_data_b64)

    def _send_avatar(
        self, image="avatar.png", width=None, height=None, strict=False, cache=False
    ):
        admin_part = self.owner.admin_part
        avatar = self.avatar if hasattr(self, "avatar") else None
        if not avatar:
            if strict:
                raise appier.NotFoundError(
                    message="Avatar not found for user '%s'" % self.username
                )
            return self.owner.send_static(
                "images/" + image, static_path=admin_part.static_path
            )
        resized = bool(width or height)
        avatar_data, avatar_etag = (
            utils.resize_image(
                avatar.data, etag=avatar.etag, width=width, height=height
            )
            if resized
            else (avatar.data, avatar.etag)
        )
        return self.owner.send_file(
            avatar_data, content_type=avatar.mime, etag=avatar_etag, cache=cache
        )

    def _set_avatar_d(self, image="avatar.png", mime="image/png"):
        if not hasattr(self.owner, "admin_part"):
            return
        if not self.owner.admin_part:
            return
        if not self.owner.admin_avatar_default:
            return

        admin_part = self.owner.admin_part

        file = open(admin_part.static_path + "/images/" + image, "rb")
        try:
            data = file.read()
        finally:
            file.close()

        file_t = (image, mime, data)
        self.avatar = appier.File(file_t)

    def _get_avatar_url(self, absolute=True, owner=None):
        cls = self.__class__
        return cls._get_avatar_url_g(self.username, absolute=absolute, owner=self.owner)

    def _join_m(self, origin, target):
        for key, value in appier.legacy.iteritems(origin):
            if key in target:
                previous = target[key]
                if isinstance(previous, dict):
                    value = self._join_m(value, previous)
                else:
                    if not isinstance(previous, list):
                        previous = [previous]
                    if not isinstance(value, list):
                        value = [value]
                    for item in value:
                        if item in previous:
                            continue
                        previous.append(item)
                    value = previous
            target[key] = value
        return target

    def _send_otp_qrcode(self, box_size=10, border=0):
        qrcode = appier.import_pip("qrcode")
        code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        code.add_data(self.otp_uri)
        code.make(fit=True)
        image = code.make_image(fill_color="black", back_color="white")
        if hasattr(image, "new_image"):
            image = image.copy()
        buffer = appier.legacy.BytesIO()
        image.save(buffer, format="PNG")
        image_data = buffer.getvalue()
        return self.owner.send_file(image_data, content_type="image/png")

    @appier.operation(name="Touch Login")
    def touch_login_s(self):
        # retrieves the global reference to the account class so that
        # it can be used for the triggering of global operations
        cls = self.__class__

        # updates the last login of the account with the current timestamp
        # and saves the account so that this value is persisted
        self.last_login = int(time.time())
        self.save()

        # triggers the global event indicating that a new account has been
        # touched about a new login operation (allows proper notification)
        cls.trigger_g("touch_login", self)

    @appier.operation(name="Generate Key", level=2)
    def generate_key_s(self, force=False):
        self = self.reload(rules=False)
        if self.key and not force:
            return
        self.key = self.secret()
        self.save()

    @appier.operation(name="Generate OTP", level=2)
    def generate_otp_s(self, force=False):
        pyotp = appier.import_pip("pyotp")
        self = self.reload(rules=False)
        if self.otp_enabled and self.otp_secret and not force:
            return
        self.otp_secret = pyotp.random_base32()
        self.otp_enabled = True
        self.save()

    @appier.operation(name="Mark Unconfirmed", level=2)
    def mark_unconfirmed_s(self):
        self.enabled = False
        self.confirmation_token = self.secret()
        self.save()

    @appier.operation(name="Email New", level=2)
    def email_new(self, password=None):
        account = self.reload(rules=False, meta=True)
        base.Base.send_email_g(
            self.owner,
            "admin/email/account/new.html.tpl",
            receivers=[self.email_f],
            subject="New account",
            title="New account",
            account=account,
            account_password=password,
        )

    @appier.operation(name="Email Confirm", level=2)
    def email_confirm(self):
        account = self.reload(rules=False, meta=True)
        base.Base.send_email_g(
            self.owner,
            "admin/email/account/confirm.html.tpl",
            receivers=[self.email_f],
            subject="Confirm account",
            title="Confirm account",
            account=account,
        )

    @appier.operation(name="Email Recover", level=2)
    def email_recover(self):
        account = self.reload(rules=False, meta=True)
        base.Base.send_email_g(
            self.owner,
            "admin/email/account/recover.html.tpl",
            receivers=[self.email_f],
            subject="Recover account",
            title="Recover account",
            account=account,
        )

    @appier.operation(
        name="Impersonate",
        description="""Impersonating another account can be considered
        illegal under some situation and should be used carefully""",
        level=2,
    )
    def impersonate(self):
        if not self.owner.admin_impersonate:
            raise appier.SecurityError(message="Impersonation is not allowed")
        self._set_account()

    @appier.operation(name="Upload Avatar", parameters=(("Avatar", "avatar", "file"),))
    def upload_avatar_s(self, avatar):
        cls = self.__class__
        if not avatar:
            return
        self.avatar = cls.avatar.type(avatar)
        self.save()

    @appier.operation(name="Add Role(s)", parameters=(("Name", "name", str),))
    def add_role_s(self, name):
        names = [name.strip() for name in name.strip().split(",")]
        for name in names:
            _role = role.Role.get(name=name)
            if _role in self.roles_l:
                continue
            self.roles_l.append(_role)
        self.save()

    @appier.operation(name="Remove Role(s)", parameters=(("Name", "name", str),))
    def remove_role_s(self, name):
        names = [name.strip() for name in name.strip().split(",")]
        for name in names:
            _role = role.Role.get(name=name)
            if not _role in self.roles_l:
                continue
            self.roles_l.remove(_role)
        self.save()

    @appier.operation(
        name="Add Credential",
        parameters=(
            ("Credential ID", "credential_id", str),
            ("Credential Data", "credential_data", str),
        ),
    )
    def add_credential_s(self, credential_id, credential_data):
        from . import credential

        _credential = credential.Credential(
            credential_id=credential_id, credential_data=credential_data, account=self
        )
        _credential.save()

    @appier.operation(
        name="Remove Credential", parameters=(("Credential ID", "credential_id", str),)
    )
    def remove_credential_s(self, credential_id):
        from . import credential

        _credential = credential.Credential.get(credential_id=credential_id)
        _credential.delete()

    @appier.operation(name="Fix Roles", level=2)
    def fix_children_s(self):
        self.roles = [role for role in self.roles if role and hasattr(role, "tokens_a")]
        self.save()

    @appier.operation(
        name="Change Username",
        description="""Changing the username of an account is
        a dangerous operation that may break relations with the
        target account""",
        parameters=(("Username", "username", str),),
        level=2,
    )
    def change_username_s(self, username):
        # retrieves the global reference to the account class so that
        # it can be used for the triggering of global operations
        cls = self.__class__

        # saves the previous username value as it's going to be used
        # in the event payload once there's a trigger operation
        username_p = self.username

        # updates the account's username and then saves the instance
        # so that it reflects the new username
        self.username = username
        self.save()

        # triggers the event that indicates the change in the username
        # so that any listener can act on it
        cls.trigger_g("change_username", self, username_p)

    @appier.operation(
        name="Change Email",
        description="""Changing the email of an account is
        a dangerous operation that may break relations with the
        target account""",
        parameters=(("Email", "email", str),),
        level=2,
    )
    def change_email_s(self, email):
        self.email = email
        self.save(immutables_a=False)

    @appier.link(name="View Avatar", devel=True)
    def view_avatar_url(self, absolute=False):
        cls = self.__class__
        model = None if cls._is_master() else cls._name()
        return self.owner.url_for(
            "admin.avatar_account", username=self.username, cls=model, absolute=absolute
        )

    @appier.link(name="View OTP QR Code", devel=True)
    def view_otp_qrcode_url(self, absolute=False):
        cls = self.__class__
        model = None if cls._is_master() else cls._name()
        return self.owner.url_for(
            "admin.otp_qrcode_account",
            username=self.username,
            cls=model,
            absolute=absolute,
        )

    @classmethod
    @appier.link(name="Export JSON", context=True)
    def export_url(cls, view=None, context=None, absolute=False):
        return appier.get_app().url_for(
            "admin.export_accounts_json", view=view, context=context, absolute=absolute
        )

    @classmethod
    @appier.link(name="Duplicates Report JSON", context=True)
    def duplicates_url(cls, view=None, context=None, absolute=False):
        return appier.get_app().url_for(
            "admin.duplicates_accounts_json",
            view=view,
            context=context,
            absolute=absolute,
        )

    @appier.view(name="Credentials")
    def credentials_v(self, *args, **kwargs):
        kwargs["sort"] = kwargs.get("sort", [("id", 1)])
        return appier.lazy_dict(
            model=self.credentials._target,
            kwargs=kwargs,
            entities=appier.lazy(lambda: self.credentials.find(*args, **kwargs)),
            page=appier.lazy(lambda: self.credentials.paginate(*args, **kwargs)),
        )

    @property
    def confirmed(self):
        return self.enabled

    @property
    def email_f(self):
        if not self.email:
            return self.email
        if not self.username:
            return self.email
        return "%s <%s>" % (self.username, self.email)

    @property
    def roles_l(self):
        return self.roles

    @property
    def roles_s(self):
        return [role for role in self.roles_l if role and hasattr(role, "tokens_a")]

    @property
    def two_factor_enabled(self):
        return bool(self.two_factor_method)

    @property
    def two_factor_method(self):
        if self.fido2_enabled:
            return "fido2"
        if self.otp_enabled:
            return "otp"
        return None

    @property
    def otp_uri(self):
        self = self.reload(rules=False)
        return "otpauth://totp/%s:%s?secret=%s" % (
            self.owner.description,
            self.username,
            self.otp_secret,
        )

    @property
    def credentials_data(self):
        from . import credential

        return credential.Credential.credentials_data_account(self)

    @property
    def credentials_data_n(self):
        _fido2 = appier.import_pip("fido2")
        import fido2.webauthn

        return [
            fido2.webauthn.AttestedCredentialData(credential_data)
            for credential_data in self.credentials_data
        ]

    def _set_session(self, unset=True, safes=[], method="set", two_factor=True):
        cls = self.__class__
        if unset:
            cls._unset_account(safes=safes)
        self.session.ensure()
        set = getattr(self.session, method)
        set("cls", cls.__name__)
        set("username", self.username)
        set("name", self.email)
        set("email", self.email)
        set("type", self.type_s())
        set("tokens", self.tokens())
        set("views", self.views_l())
        set("meta", self.meta)
        set("params", dict())

    def _set_2fa(self, unset=True, method="set"):
        cls = self.__class__
        if unset:
            cls._unset_2fa()
        self.session.ensure()
        set = getattr(self.session, method)
        set("2fa.timeout", time.time() + 60)
        set("2fa.username", self.username)
        set("2fa.method", self.two_factor_method)
