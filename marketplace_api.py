#!/usr/bin/env python
#coding: utf-8
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
#
__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"

"""Python MarketPlace API """

import sys  
import endpoints
import app.user as user
import app.marketplace.services as marketplace
import app.purchase.services as purchase
import app.product.services as product
import app.supplier.services as supplier
import app.customer.services as customer

# Importando sys e ajustando o encode para UTF-8, afim de contemplar acentuação
reload(sys)  
sys.setdefaultencoding('utf8')


# Creating api server to bind in app.yaml
APPLICATION = endpoints.api_server([
	marketplace.MarketplaceService, 
	purchase.PurchaseService, 
	user.UserService,
	product.ProductService,
	supplier.SupplierService,
	customer.CustomerService])
