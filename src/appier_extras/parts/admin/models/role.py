#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from appier_extras.parts.admin.models import base

class Role(base.Base):

    name = appier.field(
        index = "all",
        default = True
    )
    """ The common name to be used to identify this role,
    this is going to be the primary way of identifying it """

    tokens = appier.field(
        type = list
    )
    """ The set of ACL token that are going to be used to
    control the permission of accounts that use this role """

    view = appier.field(
        type = dict
    )
    """ The filtered view that is going to be applied for
    every filtered operation (data source access) """

    children = appier.field(
        type = appier.references(
            "Role",
            name = "id"
        )
    )
    """ The complete set of child roles that are associated
    with this role, this role should inherit all og the characteristics
    of the child roles (expected behaviour) """

    @classmethod
    def setup(cls):
        super(Role, cls).setup()

        # tries to find the owner role (default) in case it's not
        # found returns immediately nothing to be done
        owner = cls.find(name = "owner")
        if owner: return

        # retrieves the reference to the global logger that is going
        # to be used (should be initialized) and then prints the initial
        # information about the role to be generated
        logger = appier.get_logger()
        logger.info("Generating initial owner role for %s model ..." % cls.__name__)

        # creates the structure to be used as the owner role description
        # using the default value and then stores the role
        role = cls(
            name = "owner",
            description = "Super administrator role",
            tokens = ["*"]
        )
        role.save(validate = False)

    @classmethod
    def validate(cls):
        return super(Role, cls).validate() + [
            appier.not_null("name"),
            appier.not_empty("name"),
            appier.is_lower("name"),
            appier.string_gt("name", 3),
            appier.string_lt("name", 64),
            appier.not_duplicate("name", cls._name()),

            appier.not_null("tokens"),
            appier.not_empty("tokens")
        ]

    @classmethod
    def list_names(cls):
        return ["name", "description"]

    def view_m(self, context = None):
        return self.view

    @property
    def tokens_a(self):
        tokens = set(self.tokens)
        for child in self.children: tokens.update(child.tokens_a)
        return tokens

    @property
    def meta_a(self):
        meta = dict(self.meta)
        for child in self.children:
            for key, value in appier.legacy.iteritems(child.meta):
                if key in meta:
                    previous = meta[key]
                    if not type(previous) == list:
                        previous = [previous]
                    if not value in previous:
                        value = previous + [value]
                    else:
                        value = previous
                meta[key] = value
        return meta

    @appier.operation(
        name = "Duplicate",
        description = """Create a new account with exactly the
        same specification as the current one""",
        parameters = (("Suffix", "suffix", str, "-new"),),
        factory = True
    )
    def duplicate_s(self, suffix = "-new"):
        cls = self.__class__
        role = cls(
            description = self.description,
            meta = self.meta,
            name = self.name + suffix,
            tokens = self.tokens,
            view = self.view
        )
        role.save()
        return role

    @appier.operation(
        name = "Set Parent",
        parameters = (("Name", "name", str),)
    )
    def set_parent_s(self, name):
        cls = self.__class__
        parent = cls.get(name = name)
        if self in parent.children: return
        parent.children.append(self)
        parent.save()

    @appier.operation(
        name = "Add Child",
        parameters = (("Name", "name", str),)
    )
    def add_child_s(self, name):
        cls = self.__class__
        child = cls.get(name = name)
        if child in self.children: return
        self.children.append(child)
        self.save()
