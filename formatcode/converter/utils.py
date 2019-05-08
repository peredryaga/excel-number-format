# coding: utf8

from __future__ import division, print_function, unicode_literals

from collections import defaultdict

from formatcode.converter.errors import ConditionError, PartsCountError, PartTypeError
from formatcode.converter.parts import (DateFormat, EmptyFormat, FloatFormat, IntegerFormat, StringFormat,
                                        TimeDeltaFormat)
from formatcode.lexer.tokens import (BlockDelimiter, ConditionToken, DateTimeToken, DigitToken, DotDelimiter,
                                     StringSymbol, TimeDeltaToken)


def split_tokens_by_parts(tokens):
    counter = 1

    part = []
    for token in tokens:
        if isinstance(token, BlockDelimiter):
            if counter == 4:
                # There can be only 4 parts
                raise PartsCountError(tokens)
            yield part
            counter += 1
            part = []
        else:
            if isinstance(token, ConditionToken) and counter > 2:
                # Only 1 or 2 block can have the condition
                raise ConditionError(tokens)

            part.append(token)
    yield part


def dispatch_part_type(tokens):
    flags = defaultdict(bool)

    for token in tokens:
        for flag in (DigitToken, DateTimeToken, TimeDeltaToken, StringSymbol, DotDelimiter):
            if isinstance(token, flag):
                flags[flag] = True
                break

    if flags[DigitToken] and flags[DateTimeToken]:
        raise PartTypeError(tokens)
    elif flags[TimeDeltaToken]:
        return TimeDeltaFormat
    elif flags[DigitToken]:
        return FloatFormat if flags[DotDelimiter] else IntegerFormat
    elif flags[DateTimeToken]:
        return DateFormat
    elif flags[StringSymbol]:
        return StringFormat
    else:
        return EmptyFormat
