# coding: utf8

from __future__ import unicode_literals, print_function
import pytest

from formatcode.lexer.tokens import (ZeroPh, QPh, HashPh, CommaDelimiter, FractionDelimiter, PercentageSymbol, AtSymbol,
                                     AsteriskSymbol, UnderscoreSymbol, StringSymbol, ScientificNotationToken,
                                     ColorToken, ConditionToken, DateTimeToken, TimeDeltaToken, AmPmToken,
                                     LocaleCurrencyToken)
from six.moves import range


def test_zero():
    assert ZeroPh.match('0') == 1
    assert ZeroPh.match('1') is None


def test_q():
    assert QPh.match('?') == 1
    assert QPh.match('1') is None


def test_hash():
    assert HashPh.match('#') == 1
    assert HashPh.match('1') is None


def test_comma():
    assert CommaDelimiter.match(',') == 1
    assert CommaDelimiter.match('1') is None


def test_fraction():
    assert FractionDelimiter.match('.') == 1
    assert FractionDelimiter.match('1') is None


def test_percentage():
    assert PercentageSymbol.match('%') == 1
    assert PercentageSymbol.match('1') is None


def test_at():
    assert AtSymbol.match('@') == 1
    assert AtSymbol.match('1') is None


def test_asterisk():
    assert AsteriskSymbol.match('*') == 1
    assert AsteriskSymbol.match('1') is None


def test_underscore():
    assert UnderscoreSymbol.match('_') == 1
    assert UnderscoreSymbol.match('1') is None


@pytest.mark.parametrize('line', ['$', '+', '-', '/', '(', ')', ':', '!', '^',
                                  '&', "'", '~', '{', '}', '<', '>', '=', ' '])
def test_string_without_escape(line):
    assert StringSymbol.match(line) == 1


@pytest.mark.parametrize('line', [r'\%s' % chr(i) for i in range(33, 256)])
def test_string_with_escape(line):
    assert StringSymbol.match(line) == 2


def test_string_with_quote():
    assert StringSymbol.match('"hello"') == 7
    assert StringSymbol.match('"bye"') == 5
    assert StringSymbol.match('"12345"') == 7
    assert StringSymbol.match('"') is None


@pytest.mark.parametrize('letter', ['E', 'e'])
@pytest.mark.parametrize('sign', ['-', '+'])
@pytest.mark.parametrize('base', ['0', '00', '12', '555'])
def test_scientific_notation(letter, sign, base):
    line = letter + sign + base
    assert ScientificNotationToken.match(line) == len(line)
    assert ScientificNotationToken.match(line + 'test') == len(line)
    assert ScientificNotationToken.match('test' + line) is None


@pytest.mark.parametrize('line', ['Black', 'Green', 'White', 'Blue', 'Magenta', 'Yellow', 'Cyan', 'Red',
                                  'Color1', 'Color14', 'Color39', 'Color56'])
def test_color(line):
    assert ColorToken.match('[%s]' % line) == len(line) + 2
    assert ColorToken.match(line) is None
    assert ColorToken.match('[' + line) is None
    assert ColorToken.match(line + ']') is None


@pytest.mark.parametrize('sign', ['<', '>', '=', '<>', '<=', '>='])
@pytest.mark.parametrize('value', [1, 123, 12345, 123.45, 0.1234])
def test_condition(sign, value):
    assert ConditionToken.match('[%s%s]' % (sign, value)) == len(sign) + len(str(value)) + 2
    assert ConditionToken.match('[%s]' % value) is None
    assert ConditionToken.match('%s' % value) is None


@pytest.mark.parametrize('line', ['yy', 'yyyy', 'm', 'mm', 'mmm', 'mmmm', 'mmmmm',
                                  'd', 'dd', 'ddd', 'dddd', 'h', 'hh', 's', 'ss'])
def test_time(line):
    assert DateTimeToken.match(line) == len(line)
    assert DateTimeToken.match('[%s]' % line) is None

    assert TimeDeltaToken.match(line) is None
    assert TimeDeltaToken.match('[%s]' % line) == len(line) + 2


@pytest.mark.parametrize('line', ['AM/PM', 'A/P'])
def test_am_pm(line):
    assert AmPmToken.match(line) == len(line)


def test_locale_currency():
    assert LocaleCurrencyToken.match('[$USD-409]') == 10
    assert LocaleCurrencyToken.match('[$USD]') == 6
    assert LocaleCurrencyToken.match('[$-409]') == 7
    assert LocaleCurrencyToken.match('[$-f409]') == 8
    assert LocaleCurrencyToken.match('[$-ffffffff]') == 12
    assert LocaleCurrencyToken.match('[$$-ffffffff]') == 13

    assert LocaleCurrencyToken.match('[$$-fffffffff]') is None
    assert LocaleCurrencyToken.match('[-fffffffff]') is None
