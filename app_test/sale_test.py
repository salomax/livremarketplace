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


from itertools import cycle

import mock
from mock import Mock
from mock import MagicMock

from test_utils import TestCase

from app.sale import models as saleModel
from app.product import models as productModel
from app.exceptions import NotFoundEntityException

from google.appengine.api import apiproxy_stub
from google.appengine.api import apiproxy_stub_map


class SaleTestCase(TestCase):

    @mock.patch.object('app.product.models.ProductModel', autospec=True)
    @mock.patch('app.sale.models.SaleModel', autospec=True)
    def test_report_customers_by_product(self, _productModel,_saleModel):
        """ Unit test to customers grouped by product report. 
        """

        # Mock some inexistent product
        saleModel.productModel.get = MagicMock(return_value=None)

        # Verify exception
        self.assertRaises(NotFoundEntityException,
                          saleModel.report_customers_by_product, 1)

        # Mock some valid product
        saleModel.productModel.get = MagicMock(return_value=_productModel)

        # Mock Sale Model        
        sale = _saleModel
        sale.key.id = Mock()
        sale.key.id.side_effect = [1, 2, 3, 4, 5]

        # Mock product Model child        
        sale.product = _productModel
        sale.product.key.id = Mock(side_effect=[2, 1, 3 ,2, 1])
        # Important test must be unsorted

        # Create list to set query result
        salesList = []
        for x in range(5):
            # Mock product Model child        
            sale.product = _productModel
            sale.product.key.id = Mock()
            sale.product.key.id.return_value = x
            salesList.append(sale)

        # Mock fetch method        
        _saleModel.query().filter().fetch = MagicMock(return_value=salesList)

        # Set get_sales_query to return query mocked
        saleModel.get_sales_query = MagicMock(return_value=_saleModel.query())

        # Call report_customers_by_product method
        result = saleModel.report_customers_by_product(product_id=1)

        # The result must be:
        # Product 1 => 2 Customers
        # Product 2 => 2 Customers
        # Product 3 => 1 Customer

        print result


       