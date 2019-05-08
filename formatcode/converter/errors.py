# coding: utf8

from __future__ import division, print_function, unicode_literals

from formatcode.base.errors import FormatCodeError


class ConverterError(FormatCodeError):
    pass


class ConditionError(ConverterError):
    pass


class PartsCountError(ConverterError):
    pass


class PartTypeError(ConverterError):
    pass
