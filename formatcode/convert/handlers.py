# coding: utf-8

from __future__ import division, print_function, unicode_literals
from abc import ABC, abstractmethod
from decimal import Decimal
from six import text_type
from formatcode.lexer.tokens import AtSymbol, LocaleCurrencyToken


class BaseHandler(ABC):
    def __init__(self, part):
        """
        :type part: formatcode.convert.parts.FormatPart
        """
        self.part = part
        self.fc = self.part.fc
        self.tokens = self.part.tokens

    def configure(self):
        pass

    def format(self, v):
        return v


class GeneralHandler(BaseHandler):
    remove_sign = False

    def configure(self):
        if self.fc.neg_part == self.part:
            self.remove_sign = True

    def format(self, v):
        if isinstance(v, Decimal):
            if self.remove_sign:
                v = abs(v)
            return text_type(v)
        else:
            return v


class DigitHandler(BaseHandler):
    pass


class StringHandler(BaseHandler):
    def format(self, v):
        line = []
        for token in self.tokens:
            if isinstance(token, AtSymbol):
                line.append(v)
            elif isinstance(token, LocaleCurrencyToken):
                line.append(self.part.currency)
            else:
                line.append(token.value)
        return ''.join(line)


class DateHandler(BaseHandler):
    pass


class TimeDeltaHandler(BaseHandler):
    pass


class EmptyHandler(BaseHandler):
    def format(self, v):
        return self.part.currency


class UnknownHandler(BaseHandler):
    def format(self, v):
        if self.fc.str_part == self.part:
            return v
        else:
            return '###'
