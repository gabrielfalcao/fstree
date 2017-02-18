# -*- coding: utf-8 -*-

from fstree.backends.posix import Posix


def test_posix_supports_path():
    Posix.supports_path('/tmp').should.be.true
    Posix.supports_path('file:///tmp').should.be.true
