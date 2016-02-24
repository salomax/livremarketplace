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

from messages import CustomerPostMessage
from messages import CustomerGetMessage
from messages import CustomerCollectionMessage
from messages import CustomerSearchMessage

from app import user
from app import oauth

from protorpc import remote
from protorpc import messages
from protorpc import message_types


@endpoints.api(name='customer', 
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS, 
               audiences=oauth.ALLOWED_CLIENT_IDS, # ANDROID_AUDIENCE argument is required for Android clients and is not used by other clients
               scopes=[endpoints.EMAIL_SCOPE]) # Although you can add other scopes, you must always include the email scope if you use OAuth.
class CustomerService(remote.Service):
	"""Serviço destinado ao gerenciamento dos clientes da loja.
	"""

	# Resource Container para POSTs
	Customer_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(CustomerPostMessage)
	Customer_Search_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(CustomerSearchMessage)
	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage, id=messages.IntegerField(1, variant=messages.Variant.INT32))

	@endpoints.method(ID_RESOURCE, 
                    CustomerGetMessage,
                    http_method='GET',
                    path='{id}',
                    name='get')
	def get(self, request):
		"""Retornar o cliente cadastrado a partir de um id.
		"""

		logging.debug('Executando endpoint para obter o clientes cadastrado')

		#Obter a lista de clientes cadastrados
		customerModel = models.get(request.id)
		
		logging.debug('Cliente selecionado com sucesso, retornando endpoint')

		#Retornando cliente
		return CustomerGetMessage(
					id = customerModel.key.id(),
					name = customerModel.name,
					email = customerModel.email,
					phone = customerModel.phone,
					location = customerModel.location,
					created_date = customerModel.created_date)


	@endpoints.method(message_types.VoidMessage, 
                    CustomerCollectionMessage,
                    http_method='GET',
                    name='list')
	def list(self, unused_request):
		"""Retornar a lista de clientes cadastrados.
		"""

		logging.debug('Executando endpoint para obter a lista de clientes cadastrados')

		#Obter a lista de clientes cadastrados
		customers = models.list()

		#Declarando lista e convertendo model para message
		items = []
		for customerModel in customers:
			items.append(
				CustomerGetMessage(
					id = customerModel.key.id(),
					name = customerModel.name,
					email = customerModel.email,
					phone = customerModel.phone,
					location = customerModel.location,
					created_date = customerModel.created_date))

		#Retornando clientes
		return CustomerCollectionMessage(items=items)

	@endpoints.method(Customer_Search_MESSAGE_RESOURCE_CONTAINER,
					  CustomerCollectionMessage,
                      http_method='POST',
                      name='search')
	def search(self, request):

		"""Realiza uma pesquisa dos clientes cadastrados.
		"""
		logging.debug('Executando endpoint de pesquisa de clientes')

		#Obter a lista de clientes cadastrados
		customers = models.search(request)

		#Declarando lista e convertendo model para message
		items = []
		for customerModel in customers:
			items.append(
				CustomerGetMessage(
					id = customerModel.key.id(),
					name = customerModel.name,
					email = customerModel.email,
					phone = customerModel.phone,
					location = customerModel.location,
					created_date = customerModel.created_date))

		#Retornando clientes
		return CustomerCollectionMessage(items=items)


	@endpoints.method(Customer_MESSAGE_RESOURCE_CONTAINER,
					  CustomerGetMessage,
                      http_method='POST',
                      name='save')
	def save(self, request):
		"""Inclui ou atualiza um cliente.
		"""

		logging.debug('Executando endpoint para incluir/atualizar um cliente')

		#Cadastrar/atualizar a compra de um cliente
		customerModel = models.save(request)

		#Retornando compra persistida
		return CustomerGetMessage(
					id = customerModel.key.id(),
					name = customerModel.name,
					email = customerModel.email,
					phone = customerModel.phone,
					location = customerModel.location,
					created_date = customerModel.created_date)


	@endpoints.method(ID_RESOURCE,
					  message_types.VoidMessage,
					  path='{id}',
                      http_method='DELETE',
                      name='delete')
	def delete(self, request):
		"""Remove um cliente cadastrado.
		"""

		#Removendo Customer
		models.delete(request.id)

		return message_types.VoidMessage()