# coding: utf8

from __future__ import unicode_literals, print_function
from formatcode.base.utils import Singleton
from six import add_metaclass


def test_singleton():
    @add_metaclass(Singleton)
    class A(object):
        pass

    @add_metaclass(Singleton)
    class B(object):
        pass

    assert id(A()) == id(A())
    assert id(B()) == id(B())
    assert id(A()) != id(B())
