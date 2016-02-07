#!/usr/bin/env python
#coding: utf-8
#
# Copyright 2016 Google Inc.
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

"""Marketplace modelo, mensagens e métodos"""

import logging
import endpoints
import models
import messages
import os

from app import user

from protorpc import remote
from protorpc import message_types

ALLOWED_CLIENT_IDS = [
    os.environ['WEB_CLIENT_ID'],
    endpoints.API_EXPLORER_CLIENT_ID, # endpoints.API_EXPLORER_CLIENT_ID is needed for testing against the API Explorer in production.
]


def  get(email):
	"""Método retorna um marketplace para o usuário informado através do email. Caso o mesmo não exista, um novo é criado."""

	# Selecionando key do usuário
	user_key = user.user_key(email)

	# Selecionando a marketplace (loja) do usuário
	marketplaceModel = models.MarketplaceModel.query(ancestor=user_key).get()

	# Caso ainda não exista, uma nova marketplace (loja) é criada para o usuário
	if marketplaceModel is None:
		put(email=email, name='Nova Loja', user_key=user_key)

	logging.debug(marketplaceModel)	
		
	# Criando mensagem de retorno para o endpoint
	return marketplaceModel



def  put(email, name, user_key=None):
	"""Método atualiza um marketplace para o usuário informado através do email."""

	# Selecionando key do usuário
	if user_key is None:
		user_key = user.user_key(email)

	logging.debug('Criando/atualizando marketplace (loja) para o usuário %s', email)

	# Selecionando a marketplace (loja) do usuário
	marketplaceModel = models.MarketplaceModel.query(ancestor=user_key).get()

	# Caso exista, obter o atual
	if marketplaceModel is None:
		marketplaceModel = models.MarketplaceModel(parent=user_key)
	
	# Atualizar o nome
	marketplaceModel.name = name

	logging.debug('Persistindo no Datastore...', email)

	# Persistir a entity
	marketplaceModel.put()

	logging.debug('Persistido com sucesso!')	

	# Retornando marketplace (loja) persistida
	return marketplaceModel


@endpoints.api(name='marketplace', 
               version='v1',
               allowed_client_ids=ALLOWED_CLIENT_IDS, 
               audiences=ALLOWED_CLIENT_IDS, # ANDROID_AUDIENCE argument is required for Android clients and is not used by other clients
               scopes=[endpoints.EMAIL_SCOPE]) # Although you can add other scopes, you must always include the email scope if you use OAuth.
class MarketplaceService(remote.Service):
	"""Classe destinada ao gerenciamento da loja do usuário, suas compras, vendas, produtos, etc...
	"""

	@endpoints.method(message_types.VoidMessage, 
                    messages.MarketplaceGetMessage,
                    http_method='GET',
                    name='get')
	def get_marketplace(self, unused_request):
		"""Retornar a loja do usuário.
		"""

		logging.debug('Executando endpoint para obter a marketplace (loja) do usuário')

		#obter marketplaces (lojas) do usuário 
		marketplaceModel = get(user.get_current_user().email())

		#retorna a marketplace (loja) do usuário
		return messages.MarketplaceGetMessage(name=marketplaceModel.name, created_date=marketplaceModel.created_date)

	# Resource Container para POSTs
	MARKETPLACE_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(messages.MarketplacePostMessage)

  	@endpoints.method(MARKETPLACE_MESSAGE_RESOURCE_CONTAINER, 
                    messages.MarketplaceGetMessage,
                    http_method='POST',
                    name='put')
  	def put_marketplace(self, request):
  		"""Atualizar a loja do usuário.
  		"""

  		logging.debug('Executando endpoint para atualizar a marketplace (loja) do usuário')

  		# Atualizar marketplace (loja) do usuário
  		marketplaceModel = put(email=user.get_current_user().email(), name=request.name)

  		#retorna a marketplace (loja) do usuário
  		return messages.MarketplaceGetMessage(name=marketplaceModel.name, created_date=marketplaceModel.created_date)   
