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
import endpoints
import logging
import endpoints
import webtest

from test_utils import TestCase

from protorpc.remote import protojson
from protorpc import message_types

from app.customer.services import CustomerService
from app.customer.messages import CustomerPostMessage
from app.customer.messages import CustomerGetMessage
from app.customer.messages import CustomerSearchMessage
from app.customer.messages import CustomerKeyMessage
from app.customer.messages import CustomerCollectionMessage
from app.exceptions import NotFoundEntityException


class CustomerTestCase(TestCase):

    def setUp(self):

        # Call super method
        super(CustomerTestCase, self).setUp()

        #  Create service
        customerService = endpoints.api_server(
            [CustomerService], restricted=False)

        # Create test
        self.testapp = webtest.TestApp(customerService)

    def save(self, request):
        """ Call save endpoint.
        """

        response = self.testapp.post(
            '/_ah/spi/CustomerService.save',
            protojson.encode_message(request),
            content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(CustomerGetMessage, response.body)

    def search(self, request):
        """ Call search endpoint.
        """
        response = self.testapp.post('/_ah/spi/CustomerService.search',
                                     protojson.encode_message(request),
                                     content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(CustomerCollectionMessage, response.body)

    def list(self):
        """ Call list endpoint.
        """

        response = self.testapp.post(
            '/_ah/spi/CustomerService.list',
            content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(CustomerCollectionMessage, response.body)

    def delete(self, id, expect_errors=False):
        """ Call delete endpoint.
        """
        response = self.testapp.post('/_ah/spi/CustomerService.delete',
                                     protojson.encode_message(
                                         CustomerKeyMessage(id=id)), content_type='application/json',
                                     expect_errors=expect_errors)

        if not expect_errors:
            self.assertEqual(response.status, '200 OK')

    def testSave(self):
        """ Save customer.
        """

        request = CustomerPostMessage(
            name='Test',
            email='email@email.com',
            phone='99999999',
            location='Test Location')

        customer = self.save(request)

        self.assertIsNotNone(customer)
        self.assertIsNotNone(customer.id)
        self.assertEqual(customer.name, 'Test')
        self.assertEqual(customer.email, 'email@email.com')
        self.assertEqual(customer.phone, '99999999')
        self.assertEqual(customer.location, 'Test Location')

        request = CustomerPostMessage(
            id=customer.id,
            name='Test123',
            email='email123@email.com',
            phone='123123123',
            location='Test Location 123')

        customer = self.save(request)

        self.assertIsNotNone(customer)
        self.assertIsNotNone(customer.id)
        self.assertEqual(customer.name, 'Test123')
        self.assertEqual(customer.email, 'email123@email.com')
        self.assertEqual(customer.phone, '123123123')
        self.assertEqual(customer.location, 'Test Location 123')

        return customer

    def testSearch(self):
        """ Search a customer.
        """

        self.testSave()

        request = CustomerSearchMessage(name='Test')

        list = self.search(request)

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 1)
        request = CustomerSearchMessage(name='Yyy')

        list = self.search(request)

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 0)

    def testList(self):
        """ List all customers.
        """

        self.testSave()

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) > 0)

    def testDelete(self):
        """ Delete the customer.
        """
        customer = self.testSave()

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 1)
        self.delete(customer.id)

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 0)

        self.assertRaises(NotFoundEntityException, self.delete(
            id=customer.id, expect_errors=True))
