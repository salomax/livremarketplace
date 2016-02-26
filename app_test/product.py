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


import os
import unittest
import webtest
import endpoints
import logging

from protorpc.remote import protojson
from protorpc import message_types

from google.appengine.ext import testbed
from google.appengine.api import users

from app.product.services import ProductService
from app.product.messages import ProductPostMessage
from app.product.messages import ProductGetMessage

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class ProductTestCase(unittest.TestCase):

    def setUp(self):
        tb = testbed.Testbed()
        tb.setup_env(current_version_id='testbed.version',
            ENDPOINTS_AUTH_EMAIL='testmail@gmail.com',
            ENDPOINTS_AUTH_DOMAIN='TEST_DOMAIN')
        tb.activate()
        tb.init_all_stubs()
        self.testbed = tb

    def tearDown(self):
        self.testbed.deactivate()

    def testSaveProduct(self):
        """ Save product unit test.
        """
        print users.get_current_user()

        productService = endpoints.api_server(
            [ProductService], restricted=False)

        testapp = webtest.TestApp(productService)

        request = ProductPostMessage(name="Test", code="Test")

        print protojson.encode_message(request)

        response = testapp.post('/_ah/spi/ProductService.save',
                     protojson.encode_message(request),
                     content_type='application/json')

        r = protojson.decode_message(ProductGetMessage, response.body)

        self.assertEqual(r.name, "Test")
