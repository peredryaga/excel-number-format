# coding: utf8

from __future__ import division, print_function, unicode_literals
from formatcode.converter.utils import split_tokens_by_parts
from formatcode.lexer.tokens import ZeroToken, BlockDelimiter, ColorToken, ConditionToken
from formatcode.converter.errors import ConditionError, PartsCountError
import pytest


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
