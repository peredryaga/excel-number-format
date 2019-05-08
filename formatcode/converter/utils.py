# coding: utf8

from __future__ import division, print_function, unicode_literals
from formatcode.lexer.tokens import BlockDelimiter, ConditionToken
from formatcode.converter.errors import ConditionError


def split_tokens_by_parts(tokens):
    parts = [[]]

    for token in tokens:
        if isinstance(token, BlockDelimiter):
            parts.append([])
        else:
            if isinstance(token, ConditionToken) and len(parts) > 2:
                # Only 1 or 2 block can have the condition
                raise ConditionError(tokens)

            parts[-1].append(token)
    return parts
