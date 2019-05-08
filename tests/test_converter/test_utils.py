# coding: utf8

from __future__ import division, print_function, unicode_literals

import pytest

from formatcode.converter.errors import ConditionError, PartsCountError
from formatcode.converter.parts import (DateFormat, EmptyFormat, FloatFormat, IntegerFormat, StringFormat,
                                        TimeDeltaFormat)
from formatcode.converter.utils import dispatch_part_type, split_tokens_by_parts
from formatcode.lexer.tokens import (BlockDelimiter, ColorToken, ConditionToken, DateTimeToken, DotDelimiter,
                                     StringSymbol, TimeDeltaToken, ZeroToken)


def test_split_tokens_by_parts():
    zero = ZeroToken('0')
    delimiter = BlockDelimiter(';')
    condition = ConditionToken('[>100]')
    color = ColorToken('[Blue]')

    assert list(split_tokens_by_parts([zero, delimiter, zero])) == [[zero], [zero]]
    assert list(split_tokens_by_parts([color, zero, delimiter, zero])) == [[color, zero], [zero]]
    assert list(split_tokens_by_parts([condition, zero, delimiter, condition, zero])) == [[condition, zero],
                                                                                          [condition, zero]]

    with pytest.raises(ConditionError):
        list(split_tokens_by_parts([color, delimiter, zero, delimiter, condition, zero]))

    with pytest.raises(PartsCountError):
        list(split_tokens_by_parts([zero, delimiter, zero, delimiter, zero, delimiter, zero, delimiter, zero]))


def test_dispatch_part_type():
    zero = ZeroToken('0')
    date = DateTimeToken('yy')
    timedelta = TimeDeltaToken('[h]')
    dot = DotDelimiter('.')
    condition = ConditionToken('[>100]')
    color = ColorToken('[Blue]')
    string = StringSymbol('"hello"')

    assert dispatch_part_type([zero, zero]) == IntegerFormat
    assert dispatch_part_type([color, zero, zero]) == IntegerFormat
    assert dispatch_part_type([string, zero, zero]) == IntegerFormat

    assert dispatch_part_type([zero, dot, zero]) == FloatFormat
    assert dispatch_part_type([color, condition, zero, dot, zero]) == FloatFormat
    assert dispatch_part_type([zero, dot, zero, string]) == FloatFormat

    assert dispatch_part_type([string]) == StringFormat
    assert dispatch_part_type([color, string]) == StringFormat

    assert dispatch_part_type([date]) == DateFormat
    assert dispatch_part_type([color, date]) == DateFormat

    assert dispatch_part_type([timedelta]) == TimeDeltaFormat
    assert dispatch_part_type([color, timedelta]) == TimeDeltaFormat
    assert dispatch_part_type([color, timedelta, dot, zero]) == TimeDeltaFormat

    assert dispatch_part_type([]) == EmptyFormat
    assert dispatch_part_type([color]) == EmptyFormat
