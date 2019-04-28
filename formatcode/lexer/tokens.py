# coding: utf8

from __future__ import unicode_literals, print_function
import re


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


class RegexpToken(Token):
    regexp = None

    @classmethod
    def match(cls, line):
        m = cls.regexp.search(line)
        if m:
            return m.end()


class DigitPh(SingleSymbolPh):
    pass


class ZeroPh(DigitPh):
    symbol = '0'


class QPh(DigitPh):
    symbol = '?'


class HashPh(DigitPh):
    symbol = '#'


class CommaDelimiter(SingleSymbolPh):
    symbol = ','


class FractionDelimiter(SingleSymbolPh):
    symbol = '.'


class PercentageSymbol(SingleSymbolPh):
    symbol = '%'


class AtSymbol(SingleSymbolPh):
    symbol = '@'


class AsteriskSymbol(SingleSymbolPh):
    symbol = '*'


class UnderscoreSymbol(SingleSymbolPh):
    symbol = '_'


class StringSymbol(RegexpToken):
    regexp = re.compile(r'(?P<str>(^[$+\-/():!^&\'~{}<>= ]|(?<=^\\).|"[^"]*"))')


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
