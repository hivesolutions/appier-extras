#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2018 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import time

import appier

from appier_extras import utils

class Contentful(object):
    """
    Partial (mixin) that adds the Contentful proxy functionality
    to a controller or model that inherits from it.

    Most of the methods are meant to be used directly from the
    template or controller.
    """

    _contentful_cache = None
    """ The cache manager that is going to be used store
    contentful values, this should have a huge performance
    impact while accessing the values """

    @classmethod
    def contentful_clear(cls):
        cache = cls._get_contentful_cache()
        cache.clear()

    @classmethod
    def _contentful_deref(cls, entry, entries):
        # verifies if the current value is not a dictionary
        # and that the sys type is not defined in the entry
        # value, if that's the case this is the termination
        # condition and then returns the current entry as the value
        if not isinstance(entry, dict): return entry
        if not "sys" in entry: return entry

        # retrieves the sys value of the entry and uses it to
        # retrieve the "requested" link type value
        sys = entry["sys"]
        link_type = sys["linkType"]

        # retrieves the includes reference from the global entries
        # dictionary and then gather the items by the requested link type
        includes = entries.get("includes", {})
        items = includes.get(link_type, [])

        # iterates over the complete set of items to try to find the
        # proper reference field (from the complete set of includes)
        for item in items:
            # retrieves the reference to the sys value of the current
            # item, to be used to compare internal information
            _sys = item["sys"]

            # verifies if the current item is the one we're trying
            # to find if not we should skip the current iteration
            if not _sys["id"] == sys["id"]: continue

            # retrieves the complete set of fields from the item, so
            # that they may be dereferenced themselves
            fields = item.get("fields", {})

            # iterates over the complete set of fields to dereference
            # if that's required by the current
            for key, value in appier.legacy.items(fields):
                is_sequence = isinstance(value, (list, tuple))
                if is_sequence: field_value = [
                    cls._contentful_deref(entry, entries) for entry in value
                ]
                else: field_value = cls._contentful_deref(value, entries)
                fields[key] = field_value

            return fields

        return None

    @classmethod
    def _get_contentful_cache(cls, serialize = True, ref = None):
        ref = ref or Contentful
        if ref._contentful_cache: return ref._contentful_cache
        cache_engine = appier.conf("CACHE", "memory")
        cache_engine = appier.conf("CMS_CACHE_ENGINE", cache_engine)
        cache_engine = appier.conf("CONTENTFUL_CACHE_ENGINE", cache_engine)
        cache_engine = cache_engine.capitalize() + "Cache"
        cache_engine = getattr(appier, cache_engine)
        ref._contentful_cache = cache_engine.new(hash = True)
        if serialize: ref._contentful_cache = appier.SerializedCache(cls._contentful_cache)
        return ref._contentful_cache

    def contentful_image(
        self,
        url,
        format = "jpg",
        loading = "progressive",
        width = None,
        height = None,
        *args,
        **kwargs
    ):
        scheme, netloc, path, params, query, fragment = appier.legacy.urlparse(url)

        query = appier.legacy.parse_qs(query)
        query.update(**kwargs)

        if format: query["fm"] = [format]
        if loading: query["fl"] = [loading]
        if height: query["h"] = [str(height)]
        if width: query["w"] = [str(width)]

        query = appier.legacy.urlencode(query, doseq = True)
        image_url = appier.legacy.urlunparse((scheme, netloc, path, params, query, fragment))
        return image_url

    def contentful_value(
        self,
        key,
        default = None,
        locale = None,
        timeout = 86400,
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
        # into the format expected by contentful api
        if locale:
            language, territory = locale.split("_", 1)
            locale = language + "-" + territory.upper()
            kwargs["locale"] = locale

        # prefixes the cache's key with locale when retrieving a value for
        # a specific locale, so that proper context is used for caching
        cache_key = locale + ":" + key if locale else key

        # in case there are named arguments provided, assumes that they must
        # be key value pairs for the filtering of the scope and appends the
        # extra filter string to the cache key
        if kwargs: cache_key += ":" + ",".join("%s=%s" % (key, str(value)) for\
            key, value in appier.legacy.iteritems(kwargs))

        # tries to retrieve the reference to the contentful cache engine
        # (singleton instance) and verifies if the key exists in it, returning
        # immediately the value if that's the case
        contentful_cache = cls._get_contentful_cache()
        if cache_key in contentful_cache: return contentful_cache[cache_key]

        # retrieve the value remotely and sets the value in the cache engine,
        # to avoid further retrievals later on
        value = self._contentful_value(key, default = default, verify = verify, *args, **kwargs)
        contentful_cache.set_item(cache_key, value, expires = time.time() + timeout)
        return value

    def contentful_markdown(
        self,
        key,
        include = 10,
        default = None,
        verify = False,
        encoding = "utf-8",
        options = dict(
            anchors = False,
            blank = False
        ),
        *args,
        **kwargs
    ):
        value = self.contentful_value(
            key,
            include = include,
            default = default,
            verify = verify,
            *args,
            **kwargs
        )
        if not value: return value
        html_b = utils.MarkdownHTML.process_str(
            value,
            options = options
        )
        html_s = html_b.decode(encoding)
        return html_s

    @property
    def contentful_api(self):
        import contentful
        return contentful.API()

    def _contentful_value(
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
        # to obtain the content type and the field id
        content_type, field_id = key.split(".", 1)

        # retrieves the complete set of items that meet the content type
        # criteria and selects the first one, default to an empty dictionary
        # in case no items exist for such content type
        try:
            entries = self.contentful_api.list_entries(
                content_type = content_type,
                include = include,
                *args,
                **kwargs
            ) or dict()
        except BaseException as exception:
            self.logger.warning("Problem while accessing Contentful: %s" % exception)
            return default

        # retrieves the complete set of items and in case there's at least
        # one returns the first one of it otherwise returns an empty dictionary
        items = entries.get("items", [])
        item = items[0] if items else dict()

        # retrieves the complete set of field for the item and tries to retrieve
        # the requested field (by its identifier)
        field = item.get("fields", {})

        # verifies if the requested field exists raising an exception otherwise
        # this should ensure that the value exists in contentful
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
            cls._contentful_deref(entry, entries) for entry in field_value
        ]
        else: field_value = cls._contentful_deref(field_value, entries)

        # returns the final dereferenced value to the caller method
        # this can be both a plain value or a sequence
        return field_value
