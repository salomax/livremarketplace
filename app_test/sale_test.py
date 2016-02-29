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


from google.appengine.ext import ndb

from random import randint

import mock
from mock import Mock
from mock import MagicMock
from mock import PropertyMock

from test_utils import TestCase

from app.sale import models as saleModel
from app.product import models as productModel
from app.customer import models as customerModel
from app.exceptions import NotFoundEntityException

from google.appengine.api import apiproxy_stub
from google.appengine.api import apiproxy_stub_map


class SaleTestCase(TestCase):

    def test_sales_statistics_by_products(self):
        """ Unit test to get sales statistics by products.
        """

        # Sales list
        salesList = []
        
        # Mock sale model and products models
        salesMock = [{
            'id': 1,
            'product_id': 1,
            'net_value': 5,
            'quantity': 7
        }, {
            'id': 2,
            'product_id': 2,
            'net_value': 3,
            'quantity': 20
        }, {
            'id': 3,
            'product_id': 1,
            'net_value': 15,
            'quantity': 8
        }, {
            'id': 4,
            'product_id': 3,
            'net_value': 1,
            'quantity': 1
        }, {
            'id': 5,
            'product_id': 2,
            'net_value': 9,
            'quantity': 40
        }]

        # Iterate sales mock
        for x in salesMock:
            
            # Create sale mock
            sale = Mock(spec_set=saleModel.SaleModel())
            sale.key = Mock(spec_set=ndb.Key('SaleModel', x['id']))

            # Create product mock
            sale.product = Mock(spec_set=ndb.Key('ProductModel', x['product_id']))
            sale.product.id = Mock(return_value=x['product_id'])
            sale.product.get = Mock(return_value=sale.product)

            # Net total value
            sale.net_total = x['net_value']
            sale.quantity = x ['quantity']

            # Append to list
            salesList.append(sale)
        
        # Mock list method
        saleModel.list = MagicMock(return_value=salesList)    
        
        # Call report_customers_by_product method
        result = saleModel.get_stats_by_products()

        # Must have lenght == 3
        self.assertEqual(len(result), 3)

        # Verify quantity
        self.assertEqual(15, result[0]['sum_quantity'])
        self.assertEqual(60, result[1]['sum_quantity'])
        self.assertEqual(1, result[2]['sum_quantity'])

        # Verify sum net profit
        self.assertEqual(20, result[0]['sum_net_profit'])
        self.assertEqual(12, result[1]['sum_net_profit'])
        self.assertEqual(1, result[2]['sum_net_profit'])        

        # Verify sum net profit
        self.assertEqual(1.29, round(result[0]['avg_net_profit'], 2))
        self.assertEqual(0.19, round(result[1]['avg_net_profit'], 2))
        self.assertEqual(1, result[2]['avg_net_profit'])  

        # Verify sum net profit
        self.assertEqual(1.33, round(result[0]['weighted_avg_net_profit'], 2))
        self.assertEqual(0.20, round(result[1]['weighted_avg_net_profit'], 2))
        self.assertEqual(1, result[2]['weighted_avg_net_profit'])          


    def test_report_customers_by_products(self):
        """ Unit test to customers grouped by product report.
        """
        # Mock sale model and products models
        salesList = []
        keys = [2, 1, 3, 2, 1]
        for x in keys:
            sale = Mock(spec_set=saleModel.SaleModel())
            sale.product = Mock(spec_set=productModel.ProductModel())
            sale.product.key = Mock(spec_set=ndb.Key('ProductModel', x))
            sale.product.key.id = Mock(return_value=x)
            sale.product.key.get = Mock(return_value=sale.product)
            salesList.append(sale)

        # Mock customers models
        keys = [{'id': '1', 'name': 'Test1'}, {'id': '2', 'name': 'Test2'}]
        for sale in salesList:
            sale.customer = Mock(spec_set=customerModel.CustomerModel())
            customer = keys[randint(0, 1)]
            sale.customer.key = Mock(
                spec_set=ndb.Key('CustomerModel', customer['id']))
            sale.customer.key.id = Mock(return_value=customer['id'])
            sale.customer.key.get = Mock(return_value=customer)
            sale.customer.name = PropertyMock(return_value=customer['name'])

        # Mock fetch method
        mockSale = Mock(spec_set=saleModel.SaleModel())
        mockSale.query = Mock(spec=mockSale.query)
        mockSale.query().fetch = MagicMock(return_value=salesList)

        # Set get_sales_query to return query mocked
        saleModel.get_sales_query = MagicMock(return_value=mockSale.query())

        # Call report_customers_by_product method
        result = saleModel.report_customers_by_products()

        # Must have lenght == 3
        self.assertEqual(len(result), 3)

        # The result must be:
        #   Product 1 => 2 Customers
        #   Product 2 => 2 Customers
        #   Product 3 => 1 Customer
        self.assertEqual(len(result[0]['customers']), 2)
        self.assertEqual(len(result[1]['customers']), 2)
        self.assertEqual(len(result[2]['customers']), 1)

        # And the products must be ordered
        self.assertEqual(result[0]['product'].key.id(), 1)
        self.assertEqual(result[1]['product'].key.id(), 2)
        self.assertEqual(result[2]['product'].key.id(), 3)

    def test_report_products_by_customers(self):
        """ Unit test to products grouped by customers report.
        """
        # Mock sale model and products models
        salesList = []
        keys = [2, 1, 3, 2, 1]
        for x in keys:
            sale = Mock(spec_set=saleModel.SaleModel())
            sale.customer = Mock(spec_set=customerModel.CustomerModel())
            sale.customer.key = Mock(spec_set=ndb.Key('CustomerModel', x))
            sale.customer.key.id = Mock(return_value=x)
            sale.customer.key.get = Mock(return_value=sale.customer)
            salesList.append(sale)

        # Mock products models
        keys = [2, 3, 1]
        for sale in salesList:
            sale.product = Mock(spec_set=productModel.ProductModel())
            key_id = keys[randint(0, 2)]
            sale.product.key = Mock(
                spec_set=ndb.Key('ProductModel', key_id))
            sale.product.key.id = Mock(return_value=key_id)
            sale.product.key.get = Mock(return_value=sale.product)

        # Mock fetch method
        mockSale = Mock(spec_set=saleModel.SaleModel())
        mockSale.query = Mock(spec=mockSale.query)
        mockSale.query().fetch = MagicMock(return_value=salesList)

        # Set get_sales_query to return query mocked
        saleModel.get_sales_query = MagicMock(return_value=mockSale.query())

        # Call report_customers_by_product method
        result = saleModel.report_products_by_customers()

        # Must have lenght == 3
        self.assertEqual(len(result), 3)

        # The result must be:
        #   Customer 1 => 2 Customers
        #   Customer 2 => 2 Customers
        #   Customer 3 => 1 Customer
        self.assertEqual(len(result[0]['products']), 2)
        self.assertEqual(len(result[1]['products']), 2)
        self.assertEqual(len(result[2]['products']), 1)

        # And the customers must be ordered
        self.assertEqual(result[0]['customer'].key.id(), 1)
        self.assertEqual(result[1]['customer'].key.id(), 2)
        self.assertEqual(result[2]['customer'].key.id(), 3)
