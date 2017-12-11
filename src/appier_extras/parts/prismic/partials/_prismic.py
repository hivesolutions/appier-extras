#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

class Prismic(object):
    """
    Partial (mixin) that adds the Prismic CMS proxy functionality
    to a controller or model that inherits from it.

    Most of the methods are meant to be used directly from the
    template or controller.
    """

    _prismic_cache = None
    """ The cache manager that is going to be used store
    prismic values, this should have a huge performance
    impact while accessing the values """

    @classmethod
    def prismic_clear(cls):
        cache = cls._get_prismic_cache()
        cache.clear()

    @classmethod
    def _get_prismic_cache(cls):
        if cls._prismic_cache: return cls._prismic_cache
        cache_engine = appier.conf("CACHE", "memory")
        cache_engine = appier.conf("CMS_CACHE_ENGINE", cache_engine)
        cache_engine = appier.conf("PRISMIC_CACHE_ENGINE", cache_engine)
        cache_engine = cache_engine.capitalize() + "Cache"
        cache_engine = getattr(appier, cache_engine)
        cls._prismic_cache = cache_engine()
        return cls._prismic_cache

    def prismic_value(
        self,
        key,
        default = None,
        locale = None,
        expires = 3600,
        verify = False,
        *args,
        **kwargs
    ):
        # retrieves the reference to the parent class value to be used
        # to access class level methods
        cls = self.__class__

        # tries to retrieve the provided locale value and in case it
        # fails uses the locale associated with the current request
        # as a fallback (optimistic approach)
        locale = locale or self.request.locale

        # in case e the locale value is provided it must be normalized
        # into the format expected by prismic api
        if locale:
            language, territory = locale.split("_", 1)
            locale = language + "-" + territory.upper()
            kwargs["lang"] = locale

        # prefixes the cache's key with locale when retrieving a value for
        # a specific locale, so that proper context is used for caching
        cache_key = locale + ":" + key if locale else key

        # tries to retrieve the reference to the prismic cache engine
        # (singleton instance) and verifies if the key exists in it, returning
        # immediately the value if that's the case
        prismic_cache = cls._get_prismic_cache()
        if cache_key in prismic_cache: return prismic_cache[cache_key]

        # retrieve the value remotely and sets the value in the cache engine,
        # to avoid further retrievals later on
        value = self._prismic_value(key, default = default, verify = verify, *args, **kwargs)
        prismic_cache.set_item(key, value, expires = expires)
        return value

    @property
    def prismic_api(self):
        import prismic
        return prismic.API()

    def _prismic_value(
        self,
        key,
        include = 10,
        default = None,
        verify = False,
        *args,
        **kwargs
    ):
        # retrieves the reference to the parent class value to be used
        # to access class level methods
        cls = self.__class__

        # runs a series of assertions for the provided key, raising exceptions
        # in case one of the pre-conditions is not met
        appier.verify(
            "." in key,
            message = "Malformed key '%s', must include both content type and key" % key,
            code = 400
        )

        # splits the provided key around the dot value (namespace oriented)
        # to obtain the document type and the field id
        document_type, field_id = key.split(".", 1)

        # retrieves the complete set of items that meet the document type
        # criteria and selects the first one, default to an empty dictionary
        # in case no items exist for such content type
        try:
            entries = self.prismic_api.search_documents(
                q = "[[at(document.type,\"%s\")]]" % document_type,
                *args,
                **kwargs
            ) or dict()
        except:
            self.logger.warning("Problem while accessing prismic")
            return default

        # retrieves the complete set of items and in case there's at least
        # one returns the first one of it otherwise returns an empty dictionary
        items = entries.get("items", [])
        item = items[0] if items else dict()

        # retrieves the complete set of field for the item and tries to retrieve
        # the requested field (by its identifier)
        field = item.get("fields", {})

        # verifies if the requested field exists raising an exception otherwise
        # this should ensure that the value exists in prismic
        if verify:
            appier.verify(
                field_id in field,
                message = "'%s' not found" % field_id,
                exception = appier.NotFoundError
            )

        # retrieves the value of the field requested with the provided identifier
        # defaulting to the provided default value in case it does not exists
        field_value = field.get(field_id, default)

        # tries to determine if the value of the field is a link one (wither
        # a dictionary or a list) if that's not the case returns immediately
        is_link = isinstance(field_value, (dict, list, tuple))
        if not is_link: return field_value

        # determines if the provided field value is a sequence or a dictionary
        # and converts the the value from the link accordingly
        is_sequence = isinstance(field_value, (list, tuple))
        if is_sequence: field_value = [
            cls._prismic_deref(entry, entries) for entry in field_value
        ]
        else: field_value = cls._prismic_deref(field_value, entries)

        # returns the final dereferenced value to the caller method
        # this can be both a plain value or a sequence
        return field_value
