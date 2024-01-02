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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

from . import admin
from . import captcha
from . import contentful
from . import csfr
from . import diag
from . import export
from . import loggly
from . import logstash
from . import opbeat
from . import preflight
from . import prismic
from . import recaptcha
from . import sematext

from .admin import AdminPart
from .captcha import CaptchaPart
from .contentful import Contentful
from .csfr import CSFRPart, csfr_protect, csfr_ensure
from .diag import DiagPart
from .export import ExportPart
from .loggly import LogglyHandler, LogglyPart
from .logstash import LogstashHandler, LogstashPart
from .opbeat import OpbeatPart
from .preflight import PreflightPart
from .prismic import Prismic
from .recaptcha import ReCaptchaPart, recaptcha_protect, recaptcha_ensure
from .sematext import SematextHandler, SematextPart
