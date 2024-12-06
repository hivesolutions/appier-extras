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
import socket
import datetime

import appier

from appier_extras import utils
from appier_extras.parts.admin.models import base


class Event(base.Base):
    name = appier.field(index="all", default=True)

    handler = appier.field(index="all")

    arguments = appier.field(type=dict, meta="longmap")

    @classmethod
    def validate(cls):
        return super(Event, cls).validate() + [
            appier.not_null("name"),
            appier.not_empty("name"),
            appier.not_null("handler"),
            appier.not_empty("handler"),
        ]

    @classmethod
    def list_names(cls):
        return ["name", "handler", "enabled"]

    @classmethod
    def transform(cls, arguments, prefix):
        """
        Runs the transformation process on the provided arguments
        taking into account the filtering prefix, so that if the
        argument name is prefixed by the provided prefix such prefix
        is removed on a new re-set arguments.

        :type arguments: Dictionary
        :param arguments: The dictionary of arguments for which the
        prefix transformation is going to take place.
        :type prefix: String
        :param prefix: The prefix that is going to be used in the
        prefix removal transformation process.
        :rtype: Dictionary
        :return: The new dictionary of arguments with the processed
        values without the associated prefix set.
        """

        arguments = dict(arguments)
        prefix_l = len(prefix)
        for key, value in appier.legacy.items(arguments):
            if not key.startswith(prefix):
                continue
            key_prefix = key[prefix_l:]
            arguments[key_prefix] = value
        return arguments

    @classmethod
    def format(cls, arguments, all=False):
        formatter = utils.SafeFormatter()
        arguments = dict(arguments)
        for key, value in appier.legacy.items(arguments):
            if not appier.legacy.is_string(value, all=all):
                continue
            try:
                value = formatter.format(value, **arguments)
            except Exception:
                value = value
            arguments[key] = value
        return arguments

    @classmethod
    def notify_g(cls, name, handlers=None, permutations=True, arguments={}):
        logger = appier.get_logger()
        logger.debug("Triggering '%s' event ..." % name)
        if permutations:
            names = cls._get_permutations(name)
        else:
            names = (name,)
        kwargs = dict()
        kwargs["name"] = {"$in": names}
        if handlers:
            kwargs["handler"] = {"$in": handlers}
        events = cls.find_e(**kwargs)
        for event in events:
            event.name = name
            event.notify(arguments=arguments)

    @appier.operation(name="Notify")
    def notify(self, arguments={}, delay=True):
        cls = self.__class__
        delay_s = "a delayed" if delay else "an immediate"
        logger = appier.get_logger()
        logger.debug(
            "Notifying handler '%s' for '%s' in %s fashion ..."
            % (self.handler, self.name, delay_s)
        )
        method = getattr(self, "notify_" + self.handler)
        arguments_m = dict(self.arguments)
        arguments_m.update(arguments)
        arguments_m.update(event=self.name, handler=self.handler)
        arguments_m = cls.transform(arguments_m, self.handler + "_")
        arguments_m = cls.format(arguments_m)
        kwargs = dict(arguments=arguments_m)
        if delay:
            self.owner.delay(method, kwargs=kwargs)
        else:
            method(**kwargs)

    @classmethod
    @appier.operation(
        name="Import CSV",
        parameters=(
            ("CSV File", "file", "file"),
            ("Empty source", "empty", bool, False),
        ),
    )
    def import_csv_s(cls, file, empty):
        def callback(line):
            name, handler, arguments = line
            name = name or None
            handler = handler or None
            arguments = json.loads(arguments) if arguments else None
            event = cls(name=name, handler=handler, arguments=arguments)
            event.save()

        if empty:
            cls.delete_c()
        cls._csv_import(file, callback)

    @classmethod
    @appier.link(name="Export CSV")
    def list_csv_url(cls, absolute=False):
        return appier.get_app().url_for("admin.list_events_csv", absolute=absolute)

    @classmethod
    def _retry(cls, callable, count=3):
        result = None
        while True:
            try:
                result = callable()
            except Exception:
                count -= 1
                if count == 0:
                    raise
                else:
                    continue
            break
        return result

    def notify_http(self, arguments={}):
        cls = self.__class__
        url = arguments.get("url", None)
        timeout = arguments.get("timeout", None)
        retries = arguments.get("retries", 3)
        logger = appier.get_logger()
        logger.debug("Running HTTP notification for '%s' ..." % url)
        return cls._retry(
            lambda: appier.post(url, data_j=arguments, timeout=timeout), count=retries
        )

    def notify_mailme(self, arguments={}):
        cls = self.__class__
        appier.ensure_pip("mailme", package="mailme_api")
        import mailme

        retries = arguments.get("retries", 3)
        logger = appier.get_logger()
        logger.debug("Running Mailme notification ...")
        api = mailme.API()
        return cls._retry(lambda: api.send(arguments), count=retries)

    def notify_nexmo(self, arguments={}):
        cls = self.__class__
        appier.ensure_pip("nexmo", package="nexmo_api")
        import nexmo

        sender = arguments["sender"]
        receiver = arguments["receiver"]
        text = arguments["text"]
        retries = arguments.get("retries", 3)
        logger = appier.get_logger()
        logger.debug("Running Nexmo notification for '%s' ..." % receiver)
        api = nexmo.API()
        return cls._retry(lambda: api.send_sms(sender, receiver, text), count=retries)

    @classmethod
    def notify_kafka(cls, arguments={}):
        producer = cls._get_kafka()

        name = arguments["event"]
        params = arguments["params"]
        payload = params.get("payload", dict())

        if "topic" in arguments:
            topic = arguments["topic"]
        else:
            topic = name.split(".")[0]

        data = json.dumps(
            dict(
                name=name,
                origin=appier.get_name(),
                hostname=socket.gethostname(),
                datatype="json",
                timestamp=datetime.datetime.now(),
                payload=payload,
            )
        )
        data_b = appier.legacy.bytes(data, encoding="utf-8", force=True)

        producer.send(topic, data_b)
        producer.flush()

    @appier.operation(name="Duplicate", factory=True)
    def duplicate_s(self):
        cls = self.__class__
        event = cls(name=self.name, handler=self.handler, arguments=self.arguments)
        event.save()
        return event

    @classmethod
    def _get_kafka(cls):
        if hasattr(cls, "_kafka"):
            return cls._kafka

        appier.ensure_pip("kafka", package="kafka-python")
        import kafka

        kafka_server = appier.conf("KAFKA_SERVER", "localhost:9092")
        security_protocol = appier.conf("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT")
        sasl_mechanism = appier.conf("KAFKA_SASL_MECHANISM", None)
        sasl_plain_username = appier.conf("KAFKA_SASL_USERNAME", None)
        sasl_plain_password = appier.conf("KAFKA_SASL_PASSWORD", None)
        client_id = appier.conf("KAFKA_PRODUCER_CLIENT_ID", None)
        compression_type = appier.conf("KAFKA_COMPRESSION_TYPE", None)
        retries = appier.conf("KAFKA_RETRIES", 0, cast=int)
        batch_size = appier.conf("KAFKA_BATCH_SIZE", 16384, cast=int)
        linger_ms = appier.conf("KAFKA_LINGER", 0, cast=int)
        connections_max_idle_ms = appier.conf(
            "KAFKA_CONNECTIONS_MAX_IDLE", 540000, cast=int
        )
        max_request_size = appier.conf("KAFKA_MAX_REQUEST_SIZE", 1048576, cast=int)
        retry_backoff_ms = appier.conf("KAFKA_RETRY_BACKOFF", 100, cast=int)
        request_timeout_ms = appier.conf("KAFKA_REQUEST_TIMEOUT", 30000, cast=int)

        cls._kafka = kafka.KafkaProducer(
            bootstrap_servers=kafka_server,
            security_protocol=security_protocol,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=sasl_plain_username,
            sasl_plain_password=sasl_plain_password,
            client_id=client_id,
            compression_type=compression_type,
            retries=retries,
            batch_size=batch_size,
            linger_ms=linger_ms,
            connections_max_idle_ms=connections_max_idle_ms,
            max_request_size=max_request_size,
            retry_backoff_ms=retry_backoff_ms,
            request_timeout_ms=request_timeout_ms,
        )

        return cls._kafka

    @classmethod
    def _get_permutations(cls, name, wildcard="*"):
        names = [wildcard]
        names_a = name.split(".")[:-1]
        for name_i in range(len(names_a)):
            name_join = ".".join([n for n in names_a[0 : name_i + 1]])
            names.append("%s.%s" % (name_join, wildcard))
        names.append(name)
        return names
