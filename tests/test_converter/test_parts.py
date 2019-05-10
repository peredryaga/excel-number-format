# coding: utf-8

from __future__ import division, print_function, unicode_literals

import pytest
from six import text_type

from formatcode.converter.errors import ConditionError, DateDigitError, IllegalPartToken
from formatcode.converter.handlers import (DateHandler, DigitHandler, EmptyHandler, StringHandler, TimeDeltaHandler,
                                           UnknownHandler)
from formatcode.converter.parts import NegativePart, PositivePart, StringPart, ZeroPart
from formatcode.lexer.lexer import to_tokens_line


@pytest.mark.parametrize('value', [1234, 1234.1234, 0, u'string', None])
def test_positive_part(value):
    tokens = to_tokens_line('0.0')
    part = PositivePart(tokens=tokens)
    is_positive = isinstance(value, (float, int)) and value > 0

    assert part.handler == DigitHandler
    assert part.check_value(value) is is_positive
    assert part.check_value(text_type(value)) is is_positive

    tokens = to_tokens_line('yy:mm:dd')
    part = PositivePart(tokens=tokens)
    assert part.handler == DateHandler


@pytest.mark.parametrize('value', [1234, 1234.1234, 0, u'string', None])
def test_negative_part(value):
    tokens = to_tokens_line('0.0')
    part = NegativePart(tokens=tokens)
    is_negative = isinstance(value, (float, int)) and value < 0

    assert part.handler == DigitHandler
    assert part.check_value(value) is is_negative
    assert part.check_value(text_type(value)) is is_negative


@pytest.mark.parametrize('value', [1234, 1234.1234, 0, u'string', None])
def test_zero_part(value):
    tokens = to_tokens_line('0.0')
    part = ZeroPart(tokens=tokens)
    is_zero = isinstance(value, (float, int)) and value == 0

    assert part.handler == DigitHandler
    assert part.check_value(value) is is_zero
    assert part.check_value(text_type(value)) is is_zero


@pytest.mark.parametrize('value', [1234, 1234.1234, 0, u'string', None])
def test_string_part(value):
    tokens = to_tokens_line('"hello"')
    part = StringPart(tokens=tokens)
    is_digit = isinstance(value, (float, int))

    assert part.handler == StringHandler
    assert part.check_value(value) is not is_digit
    assert part.check_value(text_type(value)) is not is_digit


def test_handler_detect():
    assert PositivePart(tokens=to_tokens_line('0.0')).handler == DigitHandler
    assert PositivePart(tokens=to_tokens_line('"hello"')).handler == DigitHandler
    assert PositivePart(tokens=to_tokens_line('yy:mm:dd')).handler == DateHandler
    assert PositivePart(tokens=to_tokens_line('[h]:mm')).handler == TimeDeltaHandler
    assert PositivePart(tokens=to_tokens_line('[h]:mm.00')).handler == TimeDeltaHandler
    assert PositivePart(tokens=to_tokens_line('')).handler == EmptyHandler
    assert PositivePart(tokens=None).handler == UnknownHandler

    assert StringPart(tokens=to_tokens_line('"hello"@')).handler == StringHandler


def test_part_validate():
    # DateDigitError
    with pytest.raises(DateDigitError):
        PositivePart(tokens=to_tokens_line('yy.00'))

    with pytest.raises(DateDigitError):
        NegativePart(tokens=to_tokens_line('mm.00'))

    with pytest.raises(DateDigitError):
        ZeroPart(tokens=to_tokens_line('dd.00'))

    # ConditionError
    with pytest.raises(ConditionError):
        ZeroPart(tokens=to_tokens_line('[>100]0.0'))

    with pytest.raises(ConditionError):
        StringPart(tokens=to_tokens_line('[>100]0.0'))

    # IllegalPartToken
    with pytest.raises(IllegalPartToken):
        StringPart(tokens=to_tokens_line('0.0'))

    with pytest.raises(IllegalPartToken):
        PositivePart(tokens=to_tokens_line('@0.0'))

    with pytest.raises(IllegalPartToken):
        NegativePart(tokens=to_tokens_line('@0.0'))

    with pytest.raises(IllegalPartToken):
        ZeroPart(tokens=to_tokens_line('@0.0'))


@pytest.mark.parametrize('symbol,r1,r2,r3', (
        ('<', False, False, True),
        ('<=', False, True, True),
        ('=', False, True, False),
        ('<>', True, False, True),
        ('>=', True, True, False),
        ('>', True, False, False),
))
@pytest.mark.parametrize('part', (PositivePart, NegativePart))
@pytest.mark.parametrize('value', (-100, 0, 100))
def test_condition_checker(symbol, r1, r2, r3, part, value):
    part = part(tokens=to_tokens_line('[%s%s]0.0' % (symbol, value)))
    assert part.check_value(value + 1) is r1
    assert part.check_value(value) is r2
    assert part.check_value(value - 1) is r3
