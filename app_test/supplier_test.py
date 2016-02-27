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

from test_utils import TestCase

from protorpc.remote import protojson
from protorpc import message_types

from google.appengine.ext import testbed
from google.appengine.api import users
from app.supplier.services import SupplierService
from app.supplier.messages import SupplierPostMessage
from app.supplier.messages import SupplierGetMessage
from app.supplier.messages import SupplierSearchMessage
from app.supplier.messages import SupplierKeyMessage
from app.supplier.messages import SupplierCollectionMessage
from app.exceptions import NotFoundEntityException

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class SupplierTestCase(TestCase):

    def setUp(self):

        # Call super method
        super(SupplierTestCase, self).setUp()

        #  Create service
        supplierService = endpoints.api_server(
            [SupplierService], restricted=False)

        # Create test
        self.testapp = webtest.TestApp(supplierService)

    def save(self, request):
        """ Call save endpoint.
        """

        response = self.testapp.post(
            '/_ah/spi/SupplierService.save',
            protojson.encode_message(request),
            content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(SupplierGetMessage, response.body)

    def search(self, request):
        """ Call search endpoint.
        """
        response = self.testapp.post('/_ah/spi/SupplierService.search',
                                     protojson.encode_message(request),
                                     content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(SupplierCollectionMessage, response.body)

    def list(self):
        """ Call list endpoint.
        """

        response = self.testapp.post(
            '/_ah/spi/SupplierService.list',
            content_type='application/json')

        self.assertEqual(response.status, '200 OK')

        return protojson.decode_message(SupplierCollectionMessage, response.body)

    def delete(self, id, expect_errors=False):
        """ Call delete endpoint.
        """
        response = self.testapp.post('/_ah/spi/SupplierService.delete',
                                     protojson.encode_message(
                                         SupplierKeyMessage(id=id)), content_type='application/json',
                                     expect_errors=expect_errors)

        if not expect_errors:
            self.assertEqual(response.status, '200 OK')

    def testSave(self):
        """ Save supplier.
        """

        request = SupplierPostMessage(
            name='Test',
            email='email@email.com',
            phone='99999999',
            location='Test Location')

        supplier = self.save(request)

        self.assertIsNotNone(supplier)
        self.assertIsNotNone(supplier.id)
        self.assertEqual(supplier.name, 'Test')
        self.assertEqual(supplier.email, 'email@email.com')
        self.assertEqual(supplier.phone, '99999999')
        self.assertEqual(supplier.location, 'Test Location')

        request = SupplierPostMessage(
            id=supplier.id,
            name='Test123',
            email='email123@email.com',
            phone='123123123',
            location='Test Location 123')

        supplier = self.save(request)

        self.assertIsNotNone(supplier)
        self.assertIsNotNone(supplier.id)
        self.assertEqual(supplier.name, 'Test123')
        self.assertEqual(supplier.email, 'email123@email.com')
        self.assertEqual(supplier.phone, '123123123')
        self.assertEqual(supplier.location, 'Test Location 123')

        return supplier

    def testSearch(self):
        """ Search a supplier.
        """

        self.testSave()

        request = SupplierSearchMessage(name='Test')

        list = self.search(request)

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 1)
        request = SupplierSearchMessage(name='Yyy')

        list = self.search(request)

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 0)

    def testList(self):
        """ List all suppliers.
        """

        self.testSave()

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) > 0)

    def testDelete(self):
        """ Delete the supplier.
        """
        supplier = self.testSave()

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 1)
        self.delete(supplier.id)

        list = self.list()

        self.assertIsNotNone(list)
        self.assertIsNotNone(list.items)
        self.assertTrue(len(list.items) == 0)

        self.assertRaises(NotFoundEntityException, self.delete(
            id=supplier.id, expect_errors=True))
