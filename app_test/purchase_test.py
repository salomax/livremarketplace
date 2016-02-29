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
import logging
import datetime

from google.appengine.ext import ndb

from protorpc.remote import protojson
from protorpc import message_types

import mock
from mock import Mock
from mock import MagicMock
from mock import PropertyMock

from google.appengine.ext import testbed
from google.appengine.api import users
from app.purchase.services import PurchaseService
from app.purchase.messages import PurchasePostMessage
from app.purchase.messages import PurchaseGetMessage
from app.purchase.messages import PurchaseKeyMessage
from app.purchase.messages import PurchaseCollectionMessage
from app.exceptions import NotFoundEntityException

from app.purchase import models as purchaseModel
from app.product import models as productModel

class PurchaseTestCase(unittest.TestCase):
    """ Test Case for Purchases.
    """

    def test_purchases_statistics_by_products(self):
        """ Unit test to get purchases statistics by products.
        """

        # Sales list
        purchasesList = []
        
        # Mock purchase model and products models
        purchasesMock = [{
            'id': 1,
            'product_id': 1,
            'cost': 5,
            'quantity': 7
        }, {
            'id': 2,
            'product_id': 2,
            'cost': 3,
            'quantity': 20
        }, {
            'id': 3,
            'product_id': 1,
            'cost': 15,
            'quantity': 8
        }, {
            'id': 4,
            'product_id': 3,
            'cost': 1,
            'quantity': 1
        }, {
            'id': 5,
            'product_id': 2,
            'cost': 9,
            'quantity': 40
        }]

        # Iterate purchases mock
        for x in purchasesMock:
            
            # Create purchase mock
            purchase = Mock(spec_set=purchaseModel.PurchaseModel())
            purchase.key = Mock(spec_set=ndb.Key('PurchaseModel', x['id']))

            # Create product mock
            purchase.product = Mock(spec_set=productModel.ProductModel())
            purchase.product.key = Mock(spec_set=ndb.Key('ProductModel', x['product_id']))
            purchase.product.key.id = Mock(return_value=x['product_id'])
            purchase.product.key.get = Mock(return_value=purchase.product)

            # Net total value
            purchase.cost = x['cost']
            purchase.quantity = x ['quantity']

            # Append to list
            purchasesList.append(purchase)
        
        # Mock list method
        purchaseModel.list = MagicMock(return_value=purchasesList)    
        
        # Call report_customers_by_product method
        result = purchaseModel.get_stats_by_products()

        # Must have lenght == 3
        self.assertEqual(len(result), 3)

        # Verify quantity
        self.assertEqual(15, result[0]['sum_quantity'])
        self.assertEqual(60, result[1]['sum_quantity'])
        self.assertEqual(1, result[2]['sum_quantity'])

        # Verify sum cost
        self.assertEqual(20, result[0]['sum_cost'])
        self.assertEqual(12, result[1]['sum_cost'])
        self.assertEqual(1, result[2]['sum_cost'])        

        # Verify sum net profit
        self.assertEqual(10, result[0]['avg_cost'])
        self.assertEqual(6, result[1]['avg_cost'])
        self.assertEqual(1, result[2]['avg_cost'])  

        # Verify sum net profit
        self.assertEqual(10.33, round(result[0]['weighted_avg_cost'], 2))
        self.assertEqual(7, result[1]['weighted_avg_cost'])
        self.assertEqual(1, result[2]['weighted_avg_cost'])    
