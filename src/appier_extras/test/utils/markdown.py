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

import unittest

import appier_extras

class MarkdownTest(unittest.TestCase):

    def test_simple(self):
        result = appier_extras.MarkdownDebug.process_str("hello")
        self.assertEqual(result, b"normal")

        result = appier_extras.MarkdownDebug.process_str("**hello**")
        self.assertEqual(result, b"bold")

        result = appier_extras.MarkdownDebug.process_str("hello **world**")
        self.assertEqual(result, b"normal,bold")

    def test_list(self):
        result = appier_extras.MarkdownDebug.process_str("* hello")
        self.assertEqual(result, b"list")

        result = appier_extras.MarkdownDebug.process_str("* hello\n* world")
        self.assertEqual(result, b"list,normal,list")

        result = appier_extras.MarkdownDebug.process_str("1. hello")
        self.assertEqual(result, b"listo")

        result = appier_extras.MarkdownDebug.process_str("1. hello\n2. world")
        self.assertEqual(result, b"listo,normal,listo")

    def test_link(self):
        result = appier_extras.MarkdownDebug.process_str("[hello](http://example.com)")
        self.assertEqual(result, b"link")

        result = appier_extras.MarkdownDebug.process_str(
            "[hello](http://example.com)",
            options = dict(extended = True)
        )
        self.assertEqual(result, b"link(value=http://example.com)")

        result = appier_extras.MarkdownDebug.process_str(
            "[hello](http://example.com/page(with_paratenses))",
            options = dict(extended = True)
        )
        if appier_extras.has_regex(): self.assertEqual(result, b"link(value=http://example.com/page(with_paratenses))")
        else: self.assertEqual(result, b"link(value=http://example.com/page(with_paratenses),normal")

        result = appier_extras.MarkdownDebug.process_str(
            "([hello](http://example.com/page))",
            options = dict(extended = True)
        )
        self.assertEqual(result, b"normal,link(value=http://example.com/page),normal")
