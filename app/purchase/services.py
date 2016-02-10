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


import logging
import endpoints
import models

from messages import PurchasePostMessage
from messages import PurchaseGetMessage
from messages import PurchaseCollectionMessage

from app import user
from app import oauth

from protorpc import remote
from protorpc import message_types


@endpoints.api(name='purchase', 
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS, 
               audiences=oauth.ALLOWED_CLIENT_IDS, # ANDROID_AUDIENCE argument is required for Android clients and is not used by other clients
               scopes=[endpoints.EMAIL_SCOPE]) # Although you can add other scopes, you must always include the email scope if you use OAuth.
class PurchaseService(remote.Service):
	"""Serviço destinado ao gerenciamento das compras de produtos no estoque.
	"""

	@endpoints.method(message_types.VoidMessage, 
                    PurchaseCollectionMessage,
                    http_method='GET',
                    name='list')
	def list(self, unused_request):
		"""Retornar a lista de compras realizadas pelo usuário.
		"""

		logging.debug('Executando endpoint para obter uma compra de produto no estoque da loja')

		#Obter lista de compras cadastradas para a loja
		purchases = models.list()

		#Declarando lista e convertendo model para message
		items = []
		for purchaseModel in purchases:
			items.append(
				PurchaseGetMessage(
					id = purchaseModel.key.id(),
					supplier = purchaseModel.supplier,
					product = purchaseModel.product,
					quantity = purchaseModel.quantity,
					purchase_date = purchaseModel.purchase_date,
					received_date = purchaseModel.received_date,
					cost = purchaseModel.cost,
					total_cost = purchaseModel.total_cost,
					exchange_dollar = purchaseModel.exchange_dollar,
					cost_dollar = purchaseModel.cost_dollar,
					total_cost_dollar = purchaseModel.total_cost_dollar,
					shipping_cost = purchaseModel.shipping_cost,
					track_code = purchaseModel.track_code,
					invoice = purchaseModel.invoice,
					created_date = purchaseModel.created_date))

		#Retornando compras
		return PurchaseCollectionMessage(items=items)


	# Resource Container para POSTs
	PURCHASE_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(PurchasePostMessage)

	@endpoints.method(PURCHASE_MESSAGE_RESOURCE_CONTAINER,
					  PurchaseGetMessage,
                      http_method='PUT',
                      name='put')
	def put(self, request):
		"""Retornar a loja do usuário.
		"""

		logging.debug('Executando endpoint para incluir/atualizar uma compra de produto no estoque da loja')

		#Cadastrar/atualizar a compra de um produto
		purchaseModel = models.put(request)

		#Retornando compra persistida
		return PurchaseGetMessage(
					id = purchaseModel.key.id(),
					supplier = purchaseModel.supplier,
					product = purchaseModel.product,
					quantity = purchaseModel.quantity,
					purchase_date = purchaseModel.purchase_date,
					received_date = purchaseModel.received_date,
					cost = purchaseModel.cost,
					total_cost = purchaseModel.total_cost,
					exchange_dollar = purchaseModel.exchange_dollar,
					cost_dollar = purchaseModel.cost_dollar,
					total_cost_dollar = purchaseModel.total_cost_dollar,
					shipping_cost = purchaseModel.shipping_cost,
					track_code = purchaseModel.track_code,
					invoice = purchaseModel.invoice,
					created_date = purchaseModel.created_date)