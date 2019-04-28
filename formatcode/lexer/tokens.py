# coding: utf8

from __future__ import unicode_literals, print_function
import re
from formatcode.lexer import locals


class Token(object):
    def __init__(self, value):
        self.value = value

    @classmethod
    def match(cls, line):
        raise NotImplementedError


class SingleSymbolPh(Token):
    symbol = None

    @classmethod
    def match(cls, line):
        if line.startswith(cls.symbol):
            return 1


class DigitPh(SingleSymbolPh):
    pass


class ZeroPh(DigitPh):
    symbol = locals.ZERO


class QPh(DigitPh):
    symbol = locals.QUESTION


class HashPh(DigitPh):
    symbol = locals.HASH


class CommaDelimiter(SingleSymbolPh):
    symbol = locals.COMMA


class FractionDelimiter(SingleSymbolPh):
    symbol = locals.DOT


class PercentageSymbol(SingleSymbolPh):
    symbol = locals.PERCENT


class AtSymbol(SingleSymbolPh):
    symbol = locals.AT


class AsteriskSymbol(SingleSymbolPh):
    symbol = locals.ASTERISK


class UnderscoreSymbol(SingleSymbolPh):
    symbol = locals.UNDERSCORE


class RegexpToken(Token):
    regexp = None

    @classmethod
    def match(cls, line):
        m = cls.regexp.search(line)
        if m:
            return m.end()


class StringSymbol(RegexpToken):
    regexp = re.compile(r'(?P<value>(^[$+\-/():!^&\'~{}<>= ]|(?<=^\\).|"[^"]*"))')


class ScientificNotationToken(RegexpToken):
    regexp = re.compile(r'^(?P<letter>[eE])(?P<sign>[\-+])(?P<base>[0-9]+)')


class ColorToken(RegexpToken):
    regexp = re.compile(r'^\[(?P<color>(Black|Green|White|Blue|Magenta|Yellow|Cyan|Red|'
                        r'Color([1-9]|[1-4][0-9]|5[0-6])))]')


class ConditionToken(RegexpToken):
    regexp = re.compile(r'^\[(?P<sign>(<|>|>=|<=|=|<>))(?P<value>([0-9]+(\.[0-9]+)?))]')


class DateTimeToken(RegexpToken):
    regexp = re.compile(r'^(?P<value>((yy){1,2}|m{1,5}|d{1,4}|h{1,2}|s{1,2}))')


class TimeDeltaToken(RegexpToken):
    regexp = re.compile(r'^\[(?P<value>((yy){1,2}|m{1,5}|d{1,4}|h{1,2}|s{1,2}))]')


class AmPmToken(RegexpToken):
    regexp = re.compile(r'^(?P<value>(AM/PM|A/P))')


class LocaleCurrencyToken(RegexpToken):
    regexp = re.compile(r'^\[(?P<curr>\$[^-]*)(-(?P<locale>[0-9A-Fa-f]{1,8}))?]')
