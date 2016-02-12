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


from protorpc import messages
from protorpc import message_types

from app.product import messages as product


class PurchaseGetMessage(messages.Message):
  	"""Compras de produtos no estoque. Mensagem a ser trafegada pelo endpoint"""

  	#Id
  	id = messages.IntegerField(1)

	#Fornecedor	
	supplier = messages.StringField(2, required=True)

	#Produto 
	# product = messages.StringField(3, required=True)
	product = messages.MessageField(product.ProductGetMessage, 3, required=True)

	#Qtidade	
	quantity = messages.IntegerField(4, required=True)

	#Data Compra 	
	purchase_date = message_types.DateTimeField(5, required=True)

	#Data Pagamento 	
	payment_date = message_types.DateTimeField(6)

	#Valor Unidade 	
	cost = messages.FloatField(7)

	#Valor Total	
	total_cost = messages.FloatField(8)

	#Cambio	USD
	exchange_dollar = messages.FloatField(9)

	#Valor Unidade USD	
	cost_dollar = messages.FloatField(10)

	#Valor Total USD	
	total_cost_dollar = messages.FloatField(11)
		
	#Frete	
	shipping_cost = messages.FloatField(12)

	#Cód Rastreamento	
	track_code = messages.StringField(13)

	#Descrição Fatura Cartão 
	invoice = messages.StringField(14)

	#Data Recebimento 	
	received_date = message_types.DateTimeField(15)

	#Link da compra
	purchase_link = messages.StringField(16)

	#Data criação
  	created_date = message_types.DateTimeField(17, required=True)

class PurchasePostMessage(messages.Message):
  	"""Compras de produtos para o estoque da loja. Mensagem a ser trafegada pelo endpoint"""

  	#Id
  	id = messages.IntegerField(1)

	#Fornecedor	
	supplier = messages.StringField(2, required=True)

	#Produto 
	# product = messages.StringField(3, required=True)
	product = messages.MessageField(product.ProductKeyMessage, 3, required=True)

	#Qtidade	
	quantity = messages.IntegerField(4, required=True)

	#Data Compra 	
	purchase_date = message_types.DateTimeField(5, required=True)

	#Data Recebimento 	
	received_date = message_types.DateTimeField(6)

	#Valor Unidade 	
	cost = messages.FloatField(7)

	#Valor Total	
	total_cost = messages.FloatField(8)

	#Cambio	USD
	exchange_dollar = messages.FloatField(9)

	#Valor Unidade USD	
	cost_dollar = messages.FloatField(10)

	#Valor Total USD	
	total_cost_dollar = messages.FloatField(11)
		
	#Frete	
	shipping_cost = messages.FloatField(12)

	#Cód Rastreamento	
	track_code = messages.StringField(13)

	#Descrição Fatura Cartão 
	invoice = messages.StringField(14)

	#Data Pagamento 	
	payment_date = message_types.DateTimeField(15)
	
	#Link da compra
	purchase_link = messages.StringField(16)


class PurchaseCollectionMessage(messages.Message):
	"""Coleção de compras."""

	items = messages.MessageField(PurchaseGetMessage, 1, repeated=True)