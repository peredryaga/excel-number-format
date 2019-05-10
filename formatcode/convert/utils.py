# coding: utf-8

from __future__ import division, print_function, unicode_literals


def split_tokens(tokens, separator):
    out = [[]]
    for token in tokens:
        if isinstance(token, separator):
            out.append([])
        else:
            out[-1].append(token)
    return out
