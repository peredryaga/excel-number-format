# coding: utf-8

from __future__ import division, print_function, unicode_literals

from abc import ABC, abstractmethod
from decimal import Decimal
from operator import eq, ge, gt, le, lt, ne

from six import iteritems

from formatcode.base.utils import cached_property, is_digit
from formatcode.convert.errors import ConditionError, DateDigitError, IllegalPartToken
from formatcode.convert.handlers import (DateHandler, DigitHandler, EmptyHandler, StringHandler, TimeDeltaHandler,
                                         UnknownHandler)
from formatcode.lexer.tokens import (AtSymbol, ConditionToken, DateTimeToken, DigitToken, StringSymbol, TimeDeltaToken)


class FormatPart(ABC):
    color = None
    number_system = None

    def __init__(self, tokens=None, fc=None):
        self.tokens = tokens
        self.fc = fc

        self.token_types = [t.__class__ for t in self.tokens or []]
        self.validate()

        self.handler = self.handler_class(part=self)

    @abstractmethod
    def get_handler(self):
        pass

    @abstractmethod
    def get_checker(self):
        pass

    def get_token_by_type(self, token_type):
        return self.tokens[self.token_types.index(token_type)]

    @cached_property
    def checker(self):
        return self.get_checker()

    def check_value(self, v):
        return self.checker(v)

    def validate(self):
        pass

    @property
    def handler_class(self):
        if self.tokens is None:
            return UnknownHandler
        elif self.tokens:
            return self.get_handler()
        else:
            return EmptyHandler

    def format(self, value):
        pass


class DigitPart(FormatPart):
    handlers = {
        TimeDeltaToken: TimeDeltaHandler,
        DateTimeToken: DateHandler
    }

    def validate(self):
        super(DigitPart, self).validate()

        if DateTimeToken in self.token_types \
                and TimeDeltaToken not in self.token_types \
                and any(isinstance(t, DigitToken) for t in self.tokens):
            raise DateDigitError(self.tokens)
        elif AtSymbol in self.token_types:
            raise IllegalPartToken(self.tokens)

    def get_handler(self):
        for token_type, handler in iteritems(self.handlers):
            if token_type in self.token_types:
                return handler
        else:
            return DigitHandler

    @staticmethod
    def clean(value):
        return Decimal(value)

    def check_value(self, v):
        try:
            v = self.clean(v)
        except:
            return False

        return self.checker(v)


class ConditionFreePart(FormatPart):
    def validate(self):
        super(ConditionFreePart, self).validate()

        if ConditionToken in self.token_types:
            raise ConditionError(self.tokens)


class ConditionPart(DigitPart):
    functions = {
        '<': lt,
        '<=': le,
        '=': eq,
        '<>': ne,
        '>=': ge,
        '>': gt,
    }

    def __init__(self, *args, **kwargs):
        super(ConditionPart, self).__init__(*args, **kwargs)
        self.checker = self.get_condition_checker() or self.get_checker()

    def get_condition_checker(self):
        if ConditionToken in self.token_types:
            token = self.get_token_by_type(ConditionToken)
            return lambda v: self.functions[token.op](v, token.value)


class PositivePart(ConditionPart):
    def get_checker(self):
        if self.fc and self.fc.else_part.tokens is None:
            return lambda v: v >= 0
        else:
            return lambda v: v > 0


class NegativePart(ConditionPart):
    def get_checker(self):
        return lambda v: v < 0


class ZeroPart(ConditionFreePart, DigitPart):
    def get_checker(self):
        return lambda v: v == 0


class StringPart(ConditionFreePart):
    def validate(self):
        super(StringPart, self).validate()

        if set(self.token_types) - {StringSymbol, AtSymbol}:
            raise IllegalPartToken(self.tokens)

    def get_checker(self):
        return lambda v: not is_digit(v)

    def get_handler(self):
        return StringHandler
