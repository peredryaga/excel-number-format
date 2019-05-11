# coding: utf-8

from __future__ import division, print_function, unicode_literals

from abc import ABC
from decimal import Decimal

from six import text_type

from formatcode.convert.errors import IllegalPartToken
from formatcode.convert.utils import split_tokens
from formatcode.lexer.tokens import (AtSymbol, CommaDelimiter, DigitToken, DotDelimiter, LocaleCurrencyToken,
                                     PercentageSymbol, SlashSymbol, StringSymbol)


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
    by_thousand = False
    round_base = None
    fraction_divisor = None
    fraction_divisor_size = None
    divisor = 1.0

    def __init__(self, *args, **kwargs):
        super(DigitHandler, self).__init__(*args, **kwargs)
        self.left = []
        self.right = []

    def split_format(self):
        if DotDelimiter in self.part.unique_tokens:
            return split_tokens(self.tokens, DotDelimiter)
        elif SlashSymbol in self.part.unique_tokens:
            index = self.part.token_types.index(SlashSymbol)
            left = self.tokens[:index]
            right = self.tokens[index:]

            while left:
                token = left[-1]
                if isinstance(token, StringSymbol) and ' ' in token.value:
                    break
                else:
                    right.insert(0, left.pop())
            return left, right
        else:
            return self.tokens, []

    def get_last_digit_token_idx(self):
        for idx, token in enumerate(reversed(self.tokens), 1):
            if isinstance(token, DigitToken):
                return len(self.tokens) - idx
        else:
            return 0

    def configure(self):
        if PercentageSymbol in self.part.unique_tokens:
            self.divisor /= 100

        if CommaDelimiter in self.part.unique_tokens:
            if SlashSymbol not in self.part.unique_tokens:
                last_digit_token_idx = self.get_last_digit_token_idx()
                for token_type in self.part.token_types[last_digit_token_idx + 1:]:
                    if token_type == CommaDelimiter:
                        self.divisor *= 1000
                    else:
                        break
                self.by_thousand = CommaDelimiter in self.part.token_types[:last_digit_token_idx]
            else:
                self.by_thousand = True

        self.left, self.right = self.split_format()

        if self.right:
            n = 0
            has_fraction = False

            for token in self.right:
                if isinstance(token, DigitToken):
                    if self.fraction_divisor is not None:
                        raise IllegalPartToken(self.tokens)
                    n += 1
                elif isinstance(token, SlashSymbol):
                    n = 0
                    has_fraction = True

                    if token.value is not None:
                        self.fraction_divisor = token.value

            if has_fraction:
                if self.fraction_divisor is None:
                    self.fraction_divisor_size = n
            else:
                self.round_base = n
        else:
            self.round_base = 0


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
