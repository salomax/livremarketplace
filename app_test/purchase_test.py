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
import datetime

from protorpc.remote import protojson
from protorpc import message_types

from google.appengine.ext import testbed
from google.appengine.api import users
from app.purchase.services import PurchaseService
from app.purchase.messages import PurchasePostMessage
from app.purchase.messages import PurchaseGetMessage
from app.purchase.messages import PurchaseKeyMessage
from app.purchase.messages import PurchaseCollectionMessage
from app.exceptions import NotFoundEntityException


import sys
reload(sys)
sys.setdefaultencoding('utf8')


class PurchaseTestCase(unittest.TestCase):
    """ Integration Test Case for Purchases.
    """

    def setUp(self):
        tb = testbed.Testbed()
        tb.setup_env(current_version_id='testbed.version',
                     ENDPOINTS_AUTH_EMAIL='testmail@gmail.com',
                     ENDPOINTS_AUTH_DOMAIN='TEST_DOMAIN')
        tb.activate()
        tb.init_all_stubs()
        self.testbed = tb
        purchaseService = endpoints.api_server(
            [PurchaseService], restricted=False)
        self.testapp = webtest.TestApp(purchaseService)

    def tearDown(self):
        self.testbed.deactivate()

    def save(self, request):
        """ Call save endpoint.
        """

        response = self.testapp.post(
            '/_ah/spi/PurchaseService.save',
            protojson.encode_message(request),
            content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(PurchaseGetMessage, response.body)

    def list(self):
        """ Call list endpoint.
        """

        response = self.testapp.post(
            '/_ah/spi/PurchaseService.list',
            content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(PurchaseCollectionMessage, response.body)

    def delete(self, id, expect_errors=False):
        """ Call delete endpoint.
        """
        response = self.testapp.post('/_ah/spi/PurchaseService.delete',
                                     protojson.encode_message(
                                         PurchaseKeyMessage(id=id)), content_type='application/json',
                                     expect_errors=expect_errors)

        if not expect_errors:
            self.assertEqual(response.status, '200 OK')

    def testSave(self):
        """ Save purchase.
        """
        request = PurchasePostMessage(
            supplier = None,
            product = None,
            quantity = 1,
            purchase_date = datetime.datetime.now(),
            payment_date = datetime.datetime.now(),
            cost = 1.0,
            total_cost = 1.0 ,
            exchange_dollar = 1.0,
            cost_dollar = 1.0,
            total_cost_dollar = 1.0 ,
            shipping_cost = 1.0,
            track_code = 'TEST',
            invoice = 'TEST',
            received_date = datetime.datetime.now(),
            purchase_link = 'http://something.com')

        purchase = self.save(request)

        self.assertIsNotNone(purchase)
        self.assertIsNotNone(purchase.id)


        purchase = self.save(request)

        self.assertIsNotNone(purchase)
        self.assertIsNotNone(purchase.id)


        return purchase


    def testList(self):
        """ List all purchases.
        """

        self.testSave()

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) > 0)

    def testDelete(self):
        """ Delete the purchase.
        """
        purchase = self.testSave()

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 1)
        self.delete(purchase.id)

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 0)

        self.assertRaises(NotFoundEntityException, self.delete(
            id=purchase.id, expect_errors=True))
