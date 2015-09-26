#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import re
import sys

import xml.sax.saxutils

import appier

class MarkdownParser(object):
    """
    Parser object for the md (markdown) format, should be able to
    parse the normalized standard definition of markdown.

    The parser is based on the original specification published
    under the daring fireball blog, supporting the typical readability
    language features emphasized in the specification.

    This implementation is a heavily simplified version of a good and
    some of the features may not be completely implemented and the
    actual performance of the parser may be low.

    @see: http://daringfireball.net/projects/markdown/syntax
    """

    def __init__(self):
        newline = r"(?P<newline>(\n\n)|(\r\n\r\n))"
        header = r"(?P<header>^(?P<header_index>#+) (?P<header_value>.+)$)"
        list = r"(?P<list>^(?P<list_index>[ \t]*)[\*\+\-] (?P<list_value>[^\r\n]+))"
        listo = r"(?P<listo>^(?P<listo_index>[ \t]*)(?P<listo_number>\d+)\. (?P<listo_value>[^\r\n]+))"
        image = r"(?P<image>\!(?P<image_label>\[.+?\])(?P<image_value>\(.+?\)))"
        link = r"(?P<link>(?P<link_label>\[.+?\])(?P<link_value>\([^ ]+\)))"
        bold = r"(?P<bold>\*\*(?P<bold_value>[^\0]+?)\*\*)"
        italic = r"(?P<italic>\*(?P<italic_value>[^\0]+?)\*)"
        code = r"(?P<code>```(?P<code_name>.*)(?P<code_value>[^\0]+?)```)"
        code_line = r"(?P<code_line>^(    |\t)(?P<code_line_value>[^\r\n]+))"
        code_single = r"(?P<code_single>`?`(?P<code_single_value>[^`]+)``?)"

        self.master = re.compile(
            "|".join([
                newline,
                header,
                list,
                listo,
                image,
                link,
                bold,
                italic,
                code,
                code_line,
                code_single
            ]),
            re.MULTILINE | re.UNICODE
        )
        self.simple = re.compile(
            "|".join([
                image,
                link,
                bold,
                italic,
                code_single
            ]),
            re.MULTILINE | re.UNICODE
        )

    def parse(self, data, regex = None, encoding = "utf-8"):
        regex = regex or self.master

        is_unicode = appier.legacy.is_unicode(data)
        if not is_unicode: data = data.decode(encoding)

        nodes = []
        matches = regex.finditer(data)

        current = 0

        for match in matches:
            name = match.lastgroup
            parts = match.groupdict()

            start, end = match.span()
            if start > current:
                value = data[current:start]
                value = value.replace("\r", "")
                value = value.replace("\n", " ")
                if value: nodes.append(value)

            method = getattr(self, "parse_" + name)
            node = method(parts)
            nodes.append(node)

            current = end

        remaining = data[current:]
        remaining = remaining.replace("\r", "")
        remaining = remaining.replace("\n", " ")
        if remaining: nodes.append(remaining)

        return nodes

    def parse_newline(self, parts):
        node = dict(type = "newline")
        return node

    def parse_header(self, parts):
        index = parts["header_index"]
        value = parts["header_value"]

        if value.endswith(" " + index): value = value.rstrip(" #")
        hash = self._to_id(value)
        value = self.parse(value, regex = self.simple)

        node = dict(
            type = "header",
            level = len(index),
            hash = hash,
            value = value
        )
        return node

    def parse_list(self, parts):
        index = parts["list_index"]
        value = parts["list_value"]
        value = self.parse(value, regex = self.simple)

        node = dict(
            type = "list",
            level = len(index) + 1,
            value = value
        )
        return node

    def parse_listo(self, parts):
        index = parts["listo_index"]
        number = parts["listo_number"]
        value = parts["listo_value"]
        value = self.parse(value, regex = self.simple)

        node = dict(
            type = "listo",
            level = len(index) + 1,
            number = int(number),
            value = value
        )
        return node

    def parse_image(self, parts):
        label = parts["image_label"]
        value = parts["image_value"]

        label = label[1:-1]
        value = value[1:-1]

        node = dict(
            type = "image",
            label = label,
            value = value
        )
        return node

    def parse_link(self, parts):
        label = parts["link_label"]
        value = parts["link_value"]

        original = label + value
        reversed = original[::-1]
        last = reversed.index("(")

        label = original[1:(last + 2) * -1]
        value = original[last * -1:-1]

        label = self.parse(label, regex = self.simple)

        node = dict(
            type = "link",
            label = label,
            value = value
        )
        return node

    def parse_bold(self, parts):
        value = parts["bold_value"]
        value = self.parse(value, regex = self.simple)

        node = dict(
            type = "bold",
            value = value
        )
        return node

    def parse_italic(self, parts):
        value = parts["italic_value"]
        value = self.parse(value, regex = self.simple)

        node = dict(
            type = "italic",
            value = value
        )
        return node

    def parse_code(self, parts):
        name = parts["code_name"]
        value = parts["code_value"]

        node = dict(
            type = "code",
            name = name,
            value = value,
            multiline = True
        )
        return node

    def parse_code_line(self, parts):
        value = parts["code_line_value"]

        node = dict(
            type = "code",
            value = value,
            multiline = True,
            close = False
        )
        return node

    def parse_code_single(self, parts):
        value = parts["code_single_value"]

        node = dict(
            type = "code",
            value = value,
            multiline = False
        )
        return node

    def parse_normal(self, parts):
        return parts["value"]

    def _to_id(self, value):
        value = value.lower()
        value = value.replace(" ", "-")
        return value

class MarkdownGenerator(object):

    def __init__(self, file = None, options = dict(), encoding = "utf-8"):
        self.file = file
        self.options = options or dict()
        self.encoding = encoding
        self.reset()

    @classmethod
    def process(cls, in_file, out_file, parser = MarkdownParser):
        parser = parser()
        generator = cls(file = out_file)
        contents = in_file.read()
        nodes = parser.parse(contents)
        generator.generate(nodes)

    def reset(self):
        pass

    def flush(self):
        pass

    def generate(self, nodes):
        self.reset()
        self._generate(nodes)
        self.flush()

    def emit(self, value):
        if not self.file: return
        value = appier.legacy.UNICODE(value)
        value = value.encode(self.encoding)
        self.file.write(value)

    def _generate(self, nodes):
        for node in nodes:
            is_map = type(node) == dict
            _type = node["type"] if is_map else "normal"
            method = getattr(self, "generate_" + _type)
            method(node)

class MarkdownHTML(MarkdownGenerator):

    def __init__(
        self,
        file = None,
        encoding = "utf-8",
        options = dict(
            anchors = True
        ),
        base_url = ""
    ):
        MarkdownGenerator.__init__(
            self,
            file = file,
            encoding = encoding,
            options = options
        )
        self.base_url = base_url

    def emit(self, value, escape = False):
        if escape: value = self._escape_xml(value)
        MarkdownGenerator.emit(self, value)

    def is_open(self):
        return self.depth > 0

    def open(self, value):
        self.depth += 1
        self.emit(value)

    def close(self, value):
        self.depth -= 1
        if self.depth < 0: raise AssertionError("Invalid depth")
        self.emit(value)

    def reset(self):
        MarkdownGenerator.reset(self)
        self.depth = 0
        self.paragraph = False
        self.code = False
        self.list_item = False
        self.list_level = 0
        self.listo_level = 0

    def flush(self):
        MarkdownGenerator.flush(self)
        self._close_all()

    def generate_newline(self, node):
        self._close_all()
        self.open("<p>")
        self.paragraph = True

    def generate_header(self, node):
        hash = node["hash"]
        level = node["level"]
        value = node["value"]
        achors = self.options.get("anchors", True)
        self._close_all()
        self.open("<h%d id=\"%s\">" % (level, hash))
        self._generate(value)
        if achors: self.emit("<a class=\"anchor\" href=\"#%s\">¶</a>" % hash)
        self.close("</h%d>" % level)

    def generate_list(self, node):
        level = node["level"]
        value = node["value"]
        if self.list_item: self.close("</li>")
        self.list_item = False
        self._ensure_list(level = level)
        self.open("<li>")
        self.list_item = True
        self._generate(value)

    def generate_listo(self, node):
        level = node["level"]
        value = node["value"]
        if self.list_item: self.close("</li>")
        self.list_item = False
        self._ensure_listo(level = level)
        self.open("<li>")
        self.list_item = True
        self._generate(value)

    def generate_image(self, node):
        label = node["label"]
        value = node["value"]
        self.emit("<img src=\"%s\" alt=\"%s\" />" % (value, label))

    def generate_link(self, node):
        label = node["label"]
        value = node["value"]
        value = value if self.is_absolute(value) else self.base_url + value
        self.open("<a href=\"%s\">" % value)
        self._generate(label)
        self.close("</a>")

    def generate_bold(self, node):
        value = node["value"]
        self.open("<strong>")
        self._generate(value)
        self.close("</strong>")

    def generate_italic(self, node):
        value = node["value"]
        self.open("<em>")
        self._generate(value)
        self.close("</em>")

    def generate_code(self, node):
        value = node["value"]
        name = node.get("name", "undefined")
        multiline = node.get("multiline", False)
        close = node.get("close", True)
        tag = "pre" if multiline else "code"
        self._ensure_code(tag, name)
        self.emit(value, escape = True)
        if close: self._close_code(tag)

    def generate_normal(self, node):
        if self.code: self.emit("\n"); return
        if self.is_open(): self.emit(node, escape = True)
        else: self.generate_newline(node); self.emit(node.lstrip())

    def is_absolute(self, url):
        return url.startswith(("http://", "https://"))

    def _ensure_code(self, tag, name):
        if self.code: return
        self.open("<%s class=\"code language-%s\">" % (tag, name))
        self.code = True

    def _ensure_list(self, level = 1):
        if self.list_level == level: return
        self._close_all(exceptions = ("list",))
        delta = level - self.list_level
        if delta < 0: self._close_list(delta * -1); return
        for _index in range(delta): self.open("<ul>")
        self.list_level = level

    def _ensure_listo(self, level = 1):
        if self.listo_level == level: return
        self._close_all(exceptions = ("listo",))
        delta = level - self.listo_level
        if delta < 0: self._close_listo(delta * -1); return
        for _index in range(delta): self.open("<ol>")
        self.listo_level = level

    def _close_all(self, exceptions = ()):
        if not "listo" in exceptions: self._close_listo()
        if not "list" in exceptions: self._close_list()
        if not "code" in exceptions: self._close_code()
        if not "paragraph" in exceptions: self._close_paragraph()

    def _close_paragraph(self):
        if not self.paragraph: return
        self.close("</p>")
        self.paragraph = False

    def _close_code(self, tag = "pre"):
        if not self.code: return
        self.close("</%s>" % tag)
        self.code = False

    def _close_list(self, count = None):
        if self.list_item: self.close("</li>")
        if not count: count = self.list_level
        for _index in range(count): self.close("</ul>")
        self.list_level -= count
        self.list_item = False

    def _close_listo(self, count = None):
        if self.list_item: self.close("</li>")
        if not count: count = self.listo_level
        for _index in range(count): self.close("</ol>")
        self.listo_level -= count
        self.list_item = False

    def _escape_xml(self, value, encoding = "utf-8"):
        value_s = value if appier.legacy.PYTHON_3 else value.encode(encoding)
        escaped = xml.sax.saxutils.escape(value_s)
        return escaped if appier.legacy.PYTHON_3 else escaped.decode(encoding)

def run():
    if len(sys.argv) < 3:
        print("Invalid number of arguments")
        sys.exit(2)

    in_file = open(sys.argv[1], "rb")
    out_file = open(sys.argv[2], "wb")
    try: MarkdownHTML.process(in_file, out_file)
    finally: in_file.close(); out_file.close()

if __name__ == "__main__":
    run()
