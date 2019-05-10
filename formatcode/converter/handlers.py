# coding: utf-8

from __future__ import division, print_function, unicode_literals


class BaseHandler(object):
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
