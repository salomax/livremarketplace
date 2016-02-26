#!/usr/bin/env python
# coding: utf-8
#
# Copyright 2016, Marcos Salomão.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest

import os
import subprocess
import sys
import unittest

from app_test import test_utils

MODULES_TO_TEST = ['product']
NO_DEVAPPSERVER_TEMPLATE = ('Either dev appserver file path %r does not exist '
                            'or dev_appserver.py is not on your PATH.')


def fix_up_path():
    """Changes import path to make all dependencies import correctly.
    Performs the following:
    - Removes the 'google' module from sys.modules, if it exists, since
      this could cause the google.appengine... imports to fail.
    - Follow the symlink that puts dev_appserver.py on the user's path
      to find the App Engine SDK and add the SDK root to the path.
    - Import dev_appserver from the SDK and fix up the path for imports using
      dev_appserver.fix_sys_path.
    - Add the current git project root to the import path.
    """
    # May have namespace conflicts with google.appengine.api...
    # such as google.net.proto
    sys.modules.pop('google', None)

    # Find where dev_appserver.py is installed locally. If dev_appserver.py
    # is not on the path, then 'which' will return None.
    dev_appserver_on_path = test_utils.which('dev_appserver.py')
    if dev_appserver_on_path is None or not os.path.exists(dev_appserver_on_path):
        print >>sys.stderr, NO_DEVAPPSERVER_TEMPLATE % (dev_appserver_on_path,)
        raise SystemExit(1)

    real_path = os.path.realpath(dev_appserver_on_path)
    sys.path.insert(0, os.path.dirname(real_path))
    import dev_appserver
    # Use fix_sys_path to make all App Engine imports work
    dev_appserver.fix_sys_path()

    project_root = subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel']).strip()
    sys.path.insert(0, project_root)


def load_tests(import_location):
    """Loads all tests for modules and adds them to a single test suite.
    Args:
      import_location: String; used to determine how the endpoints_proto_datastore
          package is imported.
    Returns:
      Instance of unittest.TestSuite containing all tests from the modules in
          this library.
    """
    test_modules = ['%s' % name for name in MODULES_TO_TEST]
    endpoints_proto_datastore = __import__(import_location,
                                           fromlist=test_modules, level=1)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    print test_modules

    for module in [getattr(endpoints_proto_datastore, name)
                   for name in test_modules]:
        for name in set(dir(module)):
            try:
                if issubclass(getattr(module, name), unittest.TestCase):
                    test_case = getattr(module, name)
                    tests = loader.loadTestsFromTestCase(test_case)
                    suite.addTests(tests)
            except TypeError:
                pass

    return suite


def main():
    """Fixes up the import path and runs all tests.
    Also makes sure it can import the endpoints_proto_datastore package and passes
    the import location along to load_tests().
    """
    fix_up_path()

    result = unittest.TextTestRunner(verbosity=2).run(load_tests('app_test'))
    sys.exit(not result.wasSuccessful())


if __name__ == '__main__':
    main()
