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
from app.purchase.services import PurchaseService
from app.purchase.messages import PurchasePostMessage
from app.purchase.messages import PurchaseGetMessage
from app.purchase.messages import PurchaseSearchMessage
from app.purchase.messages import PurchaseKeyMessage
from app.purchase.messages import PurchaseCollectionMessage
from app.exceptions import NotFoundEntityException

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class PurchaseTestCase(unittest.TestCase):

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

    def search(self, request):
        """ Call search endpoint.
        """
        response = self.testapp.post('/_ah/spi/PurchaseService.search',
                                     protojson.encode_message(request),
                                     content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(PurchaseCollectionMessage, response.body)

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

    # Fornecedor
    supplier = messages.MessageField(
        supplier.SupplierGetMessage, 2, required=True)

    # Produto
    product = messages.MessageField(
        product.ProductGetMessage, 3, required=True)

    # Qtidade
    quantity = messages.IntegerField(4, required=True)

    # Data Compra
    purchase_date = message_types.DateTimeField(5, required=True)

    # Data Pagamento
    payment_date = message_types.DateTimeField(6, required=True)

    # Valor Unidade
    cost = messages.FloatField(7)

    # Valor Total
    total_cost = messages.FloatField(8)

    # Cambio    USD
    exchange_dollar = messages.FloatField(9)

    # Valor Unidade USD
    cost_dollar = messages.FloatField(10)

    # Valor Total USD
    total_cost_dollar = messages.FloatField(11)

    # Frete
    shipping_cost = messages.FloatField(12)

    # Cód Rastreamento
    track_code = messages.StringField(13)

    # Descrição Fatura Cartão
    invoice = messages.StringField(14)

    # Data Recebimento
    received_date = message_types.DateTimeField(15)

    # Link da compra
        purchase_link = messages.StringField(16)
        created_date = message_types.DateTimeField(17, required=True)


        purchase = self.save(request)

        self.assertIsNotNone(purchase)
        self.assertIsNotNone(purchase.id)
        self.assertEqual(purchase.name, 'Test')
        self.assertEqual(purchase.email, 'email@email.com')
        self.assertEqual(purchase.phone, '99999999')
        self.assertEqual(purchase.location, 'Test Location')

        request = PurchasePostMessage(
            id=purchase.id,
            name='Test123',
            email='email123@email.com',
            phone='123123123',
            location='Test Location 123')

        purchase = self.save(request)

        self.assertIsNotNone(purchase)
        self.assertIsNotNone(purchase.id)
        self.assertEqual(purchase.name, 'Test123')
        self.assertEqual(purchase.email, 'email123@email.com')
        self.assertEqual(purchase.phone, '123123123')
        self.assertEqual(purchase.location, 'Test Location 123')

        return purchase

    def testSearch(self):
        """ Search a purchase.
        """

        self.testSave()

        request = PurchaseSearchMessage(name='Test')

        list = self.search(request)

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 1)
        request = PurchaseSearchMessage(name='Yyy')

        list = self.search(request)

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 0)

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
