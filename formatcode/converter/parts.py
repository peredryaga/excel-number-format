# coding: utf8

from __future__ import division, print_function, unicode_literals


class FormatPart(object):
    color = None
    condition = None
    currency = None
    language_id = None
    calendar_type = None
    number_system = None

    def check_condition(self, value):
        pass

    def format(self, value):
        pass


class DigitFormat(FormatPart):
    by_thousand = False


class IntegerFormat(FormatPart):
    integer_mask = []

    def get_integer_mask(self, tokens):
        pass


class FloatFormat(IntegerFormat):
    fractional_mask = []

    def get_fractional_mask(self, tokens):
        pass


class StringFormat(FormatPart):
    pass


class DateFormat(FormatPart):
    pass


class TimeDeltaFormat(FormatPart):
    pass


class EmptyFormat(FormatPart):
    pass
