# coding: utf-8

from __future__ import division, print_function, unicode_literals
from abc import ABC, abstractmethod
from decimal import Decimal
from six import text_type
from formatcode.lexer.tokens import AtSymbol


class BaseHandler(ABC):
    def __init__(self, part):
        """
        :type part: formatcode.convert.parts.FormatPart
        """
        self.part = part
        self.tokens = self.part.tokens

    # @abstractmethod
    def configure(self):
        pass

    def format(self, v):
        return v


class GeneralHandler(BaseHandler):
    remove_sign = False

    def configure(self):
        if self.part.fc.neg_part == self.part and self.part.fc.else_part.tokens is None:
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
            else:
                line.append(token.value)
        return ''.join(line)


class DateHandler(BaseHandler):
    pass


class TimeDeltaHandler(BaseHandler):
    pass


class EmptyHandler(BaseHandler):
    pass


class UnknownHandler(BaseHandler):
    pass
