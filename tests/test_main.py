# -*- coding: utf-8 -*-
'''
pyCA tests for schedule handling
'''

import sys
import unittest

from pyca import __main__, agentstate, capture, ingest, schedule, ui, utils
from tests.tools import should_fail, ShouldFailException

if sys.version_info.major > 2:
    try:
        from importlib import reload
    except ImportError:
        from imp import reload


class TestPycaMain(unittest.TestCase):

    def test_help(self):
        sys.argv = ['pyca', '-h']
        try:
            __main__.main()
        except BaseException as e:
            assert e.code == 0
        sys.argv = ['pyca', 'too', 'many', 'arguments']
        try:
            __main__.main()
        except BaseException as e:
            assert e.code == 2
        sys.argv = ['pyca', 'fail']
        try:
            __main__.main()
        except BaseException as e:
            assert e.code == 3

    def test_run(self):
        for mod in (agentstate, capture, ingest, schedule):
            mod.run = should_fail
            sys.argv = ['pyca', mod.__name__.split('.')[-1]]
            try:
                __main__.main()
                assert False
            except ShouldFailException:
                assert True

        # Test ui start
        ui.app.run = should_fail
        sys.argv = ['pyca', 'ui']
        try:
            __main__.main()
            assert False
        except ShouldFailException:
            assert True

        # Test run all
        for mod in (agentstate, capture, ingest, schedule):
            mod.run = lambda: True
        sys.argv = ['pyca', 'run']
        try:
            __main__.main()
        except:
            assert False

        for mod in (agentstate, capture, ingest, schedule):
            reload(mod)

    def test_sigterm(self):
        try:
            __main__.sigterm_handler(0, 0)
        except BaseException as e:
            assert e.code == 0
            assert utils.terminate()