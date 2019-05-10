# coding: utf-8

from __future__ import division, print_function, unicode_literals

from decimal import Decimal

import pytest

from formatcode.convert.fc import FormatCode
from formatcode.convert.handlers import GeneralHandler, StringHandler, EmptyHandler, UnknownHandler
from formatcode.lexer.lexer import to_tokens_line


@pytest.fixture(scope='module')
def fc_1():
    tokens = to_tokens_line('0.0;\\-0.0;General;"Hello, "@\\!')
    return FormatCode(tokens=tokens)


@pytest.fixture(scope='module')
def fc_2():
    tokens = to_tokens_line('0.0;General;;@')
    return FormatCode(tokens=tokens)


@pytest.fixture(scope='module')
def fc_3():
    tokens = to_tokens_line('0.0;General')
    return FormatCode(tokens=tokens)


def test_general_handler(fc_1, fc_2):
    h = fc_1.else_part.handler
    assert isinstance(h, GeneralHandler)
    assert h.format(Decimal(1234)) == '1234'
    assert h.format(Decimal(-1234)) == '-1234'
    assert h.format(Decimal('1234.1234')) == '1234.1234'
    assert h.format(Decimal('-1234.1234')) == '-1234.1234'

    h = fc_2.neg_part.handler
    assert isinstance(h, GeneralHandler)
    assert h.format(Decimal(-1234)) == '1234'
    assert h.format(Decimal('-1234.1234')) == '1234.1234'
    assert h.format('test') == 'test'


def test_string_handler(fc_1, fc_2):
    h = fc_1.str_part.handler
    assert isinstance(h, StringHandler)
    assert h.format('John') == 'Hello, John!'
    assert h.format('mister') == 'Hello, mister!'

    h = fc_2.str_part.handler
    assert isinstance(h, StringHandler)
    assert h.format('John') == 'John'
    assert h.format('mister') == 'mister'


def test_empty_handler(fc_2):
    h = fc_2.else_part.handler
    assert isinstance(h, EmptyHandler)
    assert h.format('John') == ''
    assert h.format('mister') == ''


def test_unknown_handler(fc_3):
    h = fc_3.else_part.handler
    assert isinstance(h, UnknownHandler)
    assert h.format('John') == '###'
    assert h.format('mister') == '###'

    h = fc_3.str_part.handler
    assert isinstance(h, UnknownHandler)
    assert h.format('John') == 'John'
    assert h.format('mister') == 'mister'
