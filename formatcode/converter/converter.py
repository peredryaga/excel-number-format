# coding: utf-8

from __future__ import division, print_function, unicode_literals

from formatcode.converter.utils import split_tokens
from formatcode.lexer.tokens import BlockDelimiter
from formatcode.converter.errors import PartsCountError
from formatcode.converter.parts import PositivePart, NegativePart, ZeroPart, StringPart
from six.moves import zip_longest

parts_types = (PositivePart, NegativePart, ZeroPart, StringPart)


class FormatCode(object):
    def __init__(self, tokens):
        self.parts = self.parts_from_tokens(tokens)
        self.else_part = self.parts[2]

    def parts_from_tokens(self, tokens):
        """
        :param list tokens: Tokens line
        :rtype: list[formatcode.converter.parts.FormatPart]
        """
        tokens_by_part = split_tokens(tokens, BlockDelimiter)

        if len(tokens_by_part) > len(parts_types):
            # There can be only 4 parts
            raise PartsCountError(tokens)

        parts = [pt(tokens=ts, fc=self) for pt, ts in zip_longest(parts_types, tokens_by_part)]
        return parts

    def format(self, value):
        if value not in (None, ''):
            for part in self.parts:
                if part.checker(value):
                    return part.format(value)
            else:
                return self.else_part.format(value)
        else:
            return value
