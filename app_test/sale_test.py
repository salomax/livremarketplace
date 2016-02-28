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

