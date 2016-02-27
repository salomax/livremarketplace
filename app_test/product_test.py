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
from app.product.messages import ProductSearchMessage
from app.product.messages import ProductKeyMessage
from app.product.messages import ProductCollectionMessage
from app.exceptions import NotFoundEntityException

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
        productService = endpoints.api_server(
            [ProductService], restricted=False)
        self.testapp = webtest.TestApp(productService)

    def tearDown(self):
        self.testbed.deactivate()

    def save(self, request):
        """ Call save endpoint.
        """

        response = self.testapp.post(
            '/_ah/spi/ProductService.save',
            protojson.encode_message(request),
            content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(ProductGetMessage, response.body)

    def search(self, request):
        """ Call search endpoint.
        """
        response = self.testapp.post('/_ah/spi/ProductService.search',
                                     protojson.encode_message(request),
                                     content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(ProductCollectionMessage, response.body)

    def list(self):
        """ Call list endpoint.
        """

        response = self.testapp.post(
            '/_ah/spi/ProductService.list',
            content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(ProductCollectionMessage, response.body)

    def delete(self, id, expect_errors=False):
        """ Call delete endpoint.
        """
        response = self.testapp.post('/_ah/spi/ProductService.delete',
                                     protojson.encode_message(
                                         ProductKeyMessage(id=id)), content_type='application/json',
                                     expect_errors=expect_errors)

        if not expect_errors:
            self.assertEqual(response.status, '200 OK')

    def testSave(self):
        """ Save product.
        """

        request = ProductPostMessage(name='Test', code='Test')

        product = self.save(request)

        self.assertIsNotNone(product)
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, 'Test')
        self.assertEqual(product.code, 'Test')

        request = ProductPostMessage(
            id=product.id, name='Teste123', code='Teste123')

        product = self.save(request)

        self.assertIsNotNone(product)
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, 'Teste123')
        self.assertEqual(product.code, 'Teste123')

        return product

    def testSearch(self):
        """ Search a product.
        """

        self.testSave()

        request = ProductSearchMessage(name='Test', code='Test')

        list = self.search(request)

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 1)
        request = ProductSearchMessage(name='Yyy', code='Xxx')

        list = self.search(request)

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 0)

    def testList(self):
        """ List all products.
        """

        self.testSave()

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) > 0)

    def testDelete(self):
        """ Delete the product.
        """
        product = self.testSave()

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 1)
        self.delete(product.id)

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 0)

        self.assertRaises(NotFoundEntityException, self.delete(
            id=product.id, expect_errors=True))
