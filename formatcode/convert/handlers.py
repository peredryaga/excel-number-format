# coding: utf-8

from __future__ import division, print_function, unicode_literals


class BaseHandler(object):
    def __init__(self, part):
        self.part = part

    def format(self, v):
        return v


class GeneralHandler(BaseHandler):
    pass


class DigitHandler(BaseHandler):
    pass


class StringHandler(BaseHandler):
    pass


class DateHandler(BaseHandler):
    pass


class TimeDeltaHandler(BaseHandler):
    pass


class EmptyHandler(BaseHandler):
    pass


class UnknownHandler(BaseHandler):
    pass
