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

import os
import setuptools

setuptools.setup(
    name="appier-extras",
    version="0.26.0",
    author="Hive Solutions Lda.",
    author_email="development@hive.pt",
    description="Appier Framework Extra Elements",
    license="Apache License, Version 2.0",
    keywords="appier extras framework web json",
    url="http://appier-extras.hive.pt",
    zip_safe=False,
    packages=[
        "appier_extras",
        "appier_extras.parts",
        "appier_extras.parts.admin",
        "appier_extras.parts.admin.models",
        "appier_extras.parts.admin.models.oauth",
        "appier_extras.parts.admin.partials",
        "appier_extras.parts.admin.social",
        "appier_extras.parts.captcha",
        "appier_extras.parts.contentful",
        "appier_extras.parts.contentful.partials",
        "appier_extras.parts.csfr",
        "appier_extras.parts.diag",
        "appier_extras.parts.diag.models",
        "appier_extras.parts.export",
        "appier_extras.parts.loggly",
        "appier_extras.parts.logstash",
        "appier_extras.parts.opbeat",
        "appier_extras.parts.preflight",
        "appier_extras.parts.prismic",
        "appier_extras.parts.prismic.partials",
        "appier_extras.parts.recaptcha",
        "appier_extras.parts.sematext",
        "appier_extras.test",
        "appier_extras.test.admin",
        "appier_extras.test.admin.models",
        "appier_extras.test.admin.models.oauth",
        "appier_extras.test.csfr",
        "appier_extras.test.utils",
        "appier_extras.utils",
    ],
    test_suite="appier_extras.test",
    package_dir={"": os.path.normpath("src")},
    package_data={
        "appier_extras.parts.admin": [
            "static/css/*",
            "static/images/*",
            "static/js/*",
            "templates/admin/*",
            "templates/admin/email/*",
            "templates/admin/email/*/*",
            "templates/fluid/*",
            "templates/fluid/*/*",
            "templates/static/*",
            "templates/static/*/*",
        ],
        "appier_extras.parts.captcha": ["static/fonts/*", "static/patterns/*"],
        "appier_extras.parts.diag": ["templates/*", "templates/*/*"],
    },
    entry_points={"console_scripts": ["markdown = appier_extras.utils.markdown:run"]},
    install_requires=["appier"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
