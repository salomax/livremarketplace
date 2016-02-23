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

from messages import SalePostMessage
from messages import SaleGetMessage
from messages import SaleCollectionMessage

from app.product import messages as product
from app.customer import messages as customer

from app import user
from app import oauth

from protorpc import remote
from protorpc import messages
from protorpc import message_types


@endpoints.api(name='sale', 
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS, 
               audiences=oauth.ALLOWED_CLIENT_IDS, # ANDROID_AUDIENCE argument is required for Android clients and is not used by other clients
               scopes=[endpoints.EMAIL_SCOPE]) # Although you can add other scopes, you must always include the email scope if you use OAuth.
class SaleService(remote.Service):
	"""Serviço destinado ao gerenciamento das vendas.
	"""

	# Resource Container para POSTs
	Sale_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(SalePostMessage)

	@endpoints.method(message_types.VoidMessage, 
                    SaleCollectionMessage,
                    http_method='GET',
                    name='list')
	def list(self, unused_request):
		"""Retornar a lista de clientes cadastrados.
		"""

		logging.debug('Executando endpoint para obter a lista de clientes cadastrados')

		#Obter a lista de clientes cadastrados
		sales = models.list()

		#Declarando lista e convertendo model para message
		items = []
		for saleModel in sales:
			items.append(
				SaleGetMessage(
					id = saleModel.key.id(),
					customer = customer.CustomerGetMessage(
							id = saleModel.customer.key.id(),
							name = saleModel.customer.name,
							email = saleModel.customer.email,
							phone = saleModel.customer.phone,
							location = saleModel.customer.location,
							created_date = saleModel.customer.created_date
						),
					product = product.ProductGetMessage(
							id = saleModel.product.key.id(),
							code = saleModel.product.code,
							name = saleModel.product.name,
							created_date = saleModel.product.created_date
						),
					quantity = saleModel.quantity,
					sale_date = saleModel.sale_date,
					amount = saleModel.amount,
					fare = saleModel.fare,
					net_total = saleModel.net_total,
					track_code = saleModel.track_code,			
					created_date = saleModel.created_date))

		#Retornando clientes
		return SaleCollectionMessage(items=items)

	@endpoints.method(Sale_MESSAGE_RESOURCE_CONTAINER,
					  SaleGetMessage,
                      http_method='POST',
                      name='save')
	def save(self, request):
		"""Inclui ou atualiza uma venda.
		"""

		logging.debug('Executando endpoint para incluir/atualizar uma venda')

		#Cadastrar/atualizar a compra de um cliente
		saleModel = models.save(request)

		#Retornando compra persistida
		return SaleGetMessage(
					id = saleModel.key.id(),
					customer = customer.CustomerGetMessage(
							id = saleModel.customer.key.id(),
							name = saleModel.customer.name,
							email = saleModel.customer.email,
							phone = saleModel.customer.phone,
							location = saleModel.customer.location,
							created_date = saleModel.customer.created_date
						),
					product = product.ProductGetMessage(
							id = saleModel.product.key.id(),
							code = saleModel.product.code,
							name = saleModel.product.name,
							created_date = saleModel.product.created_date
						),
					quantity = saleModel.quantity,
					sale_date = saleModel.sale_date,
					amount = saleModel.amount,
					fare = saleModel.fare,
					net_total = saleModel.net_total,
					track_code = saleModel.track_code,			
					created_date = saleModel.created_date)

	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage, id=messages.IntegerField(1, variant=messages.Variant.INT32))
	
	@endpoints.method(ID_RESOURCE,
					  message_types.VoidMessage,
					  path='{id}',
                      http_method='DELETE',
                      name='delete')
	def delete(self, request):
		"""Remove um cliente cadastrado.
		"""

		#Removendo Sale
		models.delete(request.id)

		return message_types.VoidMessage()