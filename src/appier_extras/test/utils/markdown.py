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

import unittest

import appier_extras

class MarkdownDebugTest(unittest.TestCase):

    def test_basic(self):
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

        result = appier_extras.MarkdownDebug.process_str("*\n*\n")
        self.assertEqual(result, b"list,normal,list,normal")

        result = appier_extras.MarkdownDebug.process_str("1.\n2.\n")
        self.assertEqual(result, b"listo,normal,listo,normal")

    def test_image(self):
        result = appier_extras.MarkdownDebug.process_str("![Hello Image](image.jpg)")
        self.assertEqual(result, b"image")

        result = appier_extras.MarkdownDebug.process_str(
            "![Hello Image](image.jpg)",
            options = dict(extended = True)
        )
        self.assertEqual(result, b"image(value=image.jpg)")

    def test_link(self):
        result = appier_extras.MarkdownDebug.process_str("[hello](http://example.com)")
        self.assertEqual(result, b"link")

        result = appier_extras.MarkdownDebug.process_str(
            "[hello](http://example.com)",
            options = dict(extended = True)
        )
        self.assertEqual(result, b"link(value=http://example.com)")

        result = appier_extras.MarkdownDebug.process_str(
            "[hello](http://example.com/page(with_parentheses))",
            options = dict(extended = True)
        )
        if appier_extras.has_regex(): self.assertEqual(result, b"link(value=http://example.com/page(with_parentheses))")
        else: self.assertEqual(result, b"link(value=http://example.com/page(with_parentheses),normal")

        result = appier_extras.MarkdownDebug.process_str(
            "([hello](http://example.com/page))",
            options = dict(extended = True)
        )
        self.assertEqual(result, b"normal,link(value=http://example.com/page),normal")

        result = appier_extras.MarkdownDebug.process_str(
            "[hello[with_parentheses]](http://example.com/page)",
            options = dict(extended = True)
        )
        if appier_extras.has_regex(): self.assertEqual(result, b"link(value=http://example.com/page)")
        else: self.assertEqual(result, b"normal")

        result = appier_extras.MarkdownDebug.process_str(
            "([hellowith_parentheses]](http://example.com/page))",
            options = dict(extended = True)
        )
        self.assertEqual(result, b"normal")

        result = appier_extras.MarkdownDebug.process_str(
            "[![Hello Image](image.jpg)](http://example.com/page)",
            options = dict(extended = True)
        )
        self.assertEqual(result, b"link(value=http://example.com/page)")

    def test_code(self):
        result = appier_extras.MarkdownDebug.process_str("\thello")
        self.assertEqual(result, b"code")

        result = appier_extras.MarkdownDebug.process_str("    hello")
        self.assertEqual(result, b"code")

        result = appier_extras.MarkdownDebug.process_str("    hello\n\tworld")
        self.assertEqual(result, b"code,normal,code")

class MarkdownHTMLTest(unittest.TestCase):

    def test_basic(self):
        result = appier_extras.MarkdownHTML.process_str("hello")
        self.assertEqual(result, b"<p>hello</p>")

        result = appier_extras.MarkdownHTML.process_str("**hello**")
        self.assertEqual(result, b"<strong>hello</strong>")

        result = appier_extras.MarkdownHTML.process_str("hello **world**")
        self.assertEqual(result, b"<p>hello <strong>world</strong></p>")

    def test_list(self):
        result = appier_extras.MarkdownHTML.process_str("* hello")
        self.assertEqual(result, b"<ul><li>hello</li></ul>")

        result = appier_extras.MarkdownHTML.process_str("* hello\n* world")
        self.assertEqual(result, b"<ul><li>hello </li><li>world</li></ul>")

        result = appier_extras.MarkdownHTML.process_str("1. hello")
        self.assertEqual(result, b"<ol><li>hello</li></ol>")

        result = appier_extras.MarkdownHTML.process_str("1. hello\n2. world")
        self.assertEqual(result, b"<ol><li>hello </li><li>world</li></ol>")

        result = appier_extras.MarkdownHTML.process_str("*\n*\n")
        self.assertEqual(result, b"<ul><li> </li><li> </li></ul>")

        result = appier_extras.MarkdownHTML.process_str("1.\n2.\n")
        self.assertEqual(result, b"<ol><li> </li><li> </li></ol>")

    def test_code(self):
        result = appier_extras.MarkdownHTML.process_str("\thello")
        self.assertEqual(result, b"<pre class=\"code language-undefined\">hello</pre>")

        result = appier_extras.MarkdownHTML.process_str("    hello")
        self.assertEqual(result, b"<pre class=\"code language-undefined\">hello</pre>")

        result = appier_extras.MarkdownHTML.process_str("    hello\n\tworld")
        self.assertEqual(result, b"<pre class=\"code language-undefined\">hello\nworld</pre>")
