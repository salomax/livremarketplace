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

import datetime

from google.appengine.ext import ndb

from app import datastore
from app.supplier import models
from app.product import models


class PurchaseModel(ndb.Model):
	"""Entidade representa a compra de um produto pela loja"""

	#Fornecedor	
	supplier = ndb.StructuredProperty(SupplierModel, required=True, repeated=False)
	
	#Produto 
	product = ndb.StructuredProperty(ProductModel, required=True, repeated=False)

	#Qtidade	
	quantity = ndb.IntegerProperty(required=True, default=1)

	#Data Compra 	
	purchase_date = ndb.DateProperty(required=True, default=datetime.datetime.today())

	#Data Recebimento 	
	received_date = ndb.DateProperty()

	#Valor Unidade USD	
	cust_product_dollar = datastore.CurrencyProperty()

	#Valor Total USD	
	total_cust_product_dollar = datastore.CurrencyProperty()

	#Valor Unidade 	
	cust_product = datastore.CurrencyProperty()

	#Valor Total	
	total_cust_product = datastore.CurrencyProperty()

	#Cambio	
	
	
	#Frete	
	#Cód Rastreamento	
	#Fatura Cartão 

