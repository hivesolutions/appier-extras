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

import math

SIZE_UNITS_LIST = (
    "B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"
)
""" The size units list that contains the complete set of
units indexed by the depth they represent """

SIZE_UNITS_LIST_S = (
    "B", "K", "M", "G", "T", "P", "E", "Z", "Y"
)
""" The simplified size units list that contains the complete set of
units indexed by the depth they represent """

SIZE_UNIT_COEFFICIENT = 1024
""" The size unit coefficient as an integer value, this is
going to be used in each of the size steps as divisor """

DEFAULT_MINIMUM = 1024
""" The default minimum value meaning that this is the
maximum value that one integer value may have for the
size rounding operation to be performed """

DEFAULT_PLACES = 3
""" The default number of places (digits) that are going
to be used for the string representation in the round
based conversion of size units to be performed """

def size_round_unit(
    size_value,
    minimum = DEFAULT_MINIMUM,
    places = DEFAULT_PLACES,
    reduce = True,
    space = False,
    justify = False,
    simplified = False,
    depth = 0
):
    """
    Rounds the size unit, returning a string representation
    of the value with a good rounding precision.
    This method should be used to round data sizing units.

    Note that using the places parameter it's possible to control
    the number of digits (including decimal places) of the
    number that is going to be "generated".

    :type size_value: int/float
    :param size_value: The current size value (in bytes).
    :type minimum: int
    :param minimum: The minimum value to be used.
    :type places: int
    :param places: The target number of digits to be used for
    describing the value to be used for output, this is going
    to be used to calculate the proper number of decimal places.
    :type reduce: bool
    :param reduce: If the final string value should be reduced
    meaning that right decimal zeros should be removed as they
    represent an extra unused value.
    :type space: bool
    :param space: If a space character must be used dividing
    the value from the unit symbol.
    :type justify: bool
    :param justify: If the size string value should be (right)
    justified important for properly aligned values in a table.
    :type simplified: bool
    :param simplified: If the simplified version of the units
    should be used instead of the longer one.
    :type depth: int
    :param depth: The current iteration depth value.
    :rtype: String
    :return: The string representation of the data size
    value in a simplified manner (unit).
    """

    # in case the current size value is acceptable (less than
    # the minimum) this is the final iteration and the final
    # string representation is going to be created
    if size_value < minimum:
        # calculates the maximum size of the string that is going
        # to represent the base size value as the number of places
        # plus one (representing the decimal separator character)
        size_s = places + 1

        # calculates the target number of decimal places taking
        # into account the size (in digits) of the current size
        # value, this may never be a negative number
        log_value = size_value and math.log10(size_value)
        digits = int(log_value) + 1
        places = places - digits
        places = places if places > 0 else 0

        # creates the proper format string that is going to
        # be used in the creation of the proper float value
        # according to the calculated number of places
        format = "%%.%df" % places

        # rounds the size value, then converts the rounded
        # size value into a string based representation
        size_value = round(size_value, places)
        size_value_s = format % size_value

        # forces the reduce flag when the depth is zero, meaning
        # that an integer value will never be decimal, this is
        # required to avoid strange results for depth zero
        reduce = reduce or depth == 0

        # in case the dot value is not present in the size value
        # string adds it to the end otherwise an issue may occur
        # while removing extra padding characters for reduce
        if reduce and not "." in size_value_s: size_value_s += "."

        # strips the value from zero appended to the right and
        # then strips the value also from a possible decimal
        # point value that may be included in it, this is only
        # performed in case the reduce flag is enabled
        if reduce: size_value_s = size_value_s.rstrip("0")
        if reduce: size_value_s = size_value_s.rstrip(".")

        # in case the justify flag is set runs the justification
        # process on the size value taking into account the maximum
        # size of the associated size string
        if justify: size_value_s = size_value_s.rjust(size_s)

        # retrieves the size unit (string mode) for the current
        # depth according to the provided map
        if simplified: size_unit = SIZE_UNITS_LIST_S[depth]
        else: size_unit = SIZE_UNITS_LIST[depth]

        # retrieves the appropriate separator based
        # on the value of the space flag
        separator = space and " " or ""

        # creates the size value string appending the rounded
        # size value string and the size unit and returns it
        # to the caller method as the size value string
        size_value_string = size_value_s + separator + size_unit
        return size_value_string

    # otherwise the value is not acceptable and a new iteration
    # must be ran with one less depth of size value
    else:
        # re-calculates the new size value, increments the depth
        # and runs the size round unit again with the new values
        new_size_value = float(size_value) / SIZE_UNIT_COEFFICIENT
        new_depth = depth + 1
        return size_round_unit(
            new_size_value,
            minimum = minimum,
            places = places,
            reduce = reduce,
            space = space,
            justify = justify,
            simplified = simplified,
            depth = new_depth
        )
