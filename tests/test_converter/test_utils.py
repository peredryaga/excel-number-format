# coding: utf8

from __future__ import division, print_function, unicode_literals

import pytest

from formatcode.converter.errors import ConditionError, PartsCountError
from formatcode.converter.utils import split_tokens
from formatcode.lexer.tokens import (BlockDelimiter, ColorToken, ConditionToken, DateTimeToken, DotDelimiter,
                                     StringSymbol, TimeDeltaToken, ZeroToken)


def test_split_tokens():
    zero = ZeroToken('0')
    dot = DotDelimiter('.')
    delimiter = BlockDelimiter(';')
    condition = ConditionToken('[>100]')
    color = ColorToken('[Blue]')

    assert split_tokens([zero, delimiter, zero], BlockDelimiter) == [[zero], [zero]]
    assert split_tokens([zero, dot, zero], DotDelimiter) == [[zero], [zero]]
    assert split_tokens([color, zero, delimiter, zero], BlockDelimiter) == [[color, zero], [zero]]
    assert split_tokens([condition, zero, delimiter, condition, zero], BlockDelimiter) == [[condition, zero],
                                                                                           [condition, zero]]
