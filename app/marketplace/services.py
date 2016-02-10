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

"""Módulo destinado aos serviços da loja
"""

import logging
import endpoints
import models
import messages

from app import user
from app import oauth

from protorpc import remote
from protorpc import message_types


@endpoints.api(name='marketplace', 
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS, 
               audiences=oauth.ALLOWED_CLIENT_IDS, # ANDROID_AUDIENCE argument is required for Android clients and is not used by other clients
               scopes=[endpoints.EMAIL_SCOPE]) # Although you can add other scopes, you must always include the email scope if you use OAuth.
class MarketplaceService(remote.Service):
	"""Serviço destinado ao gerenciamento da loja.
	"""

	@endpoints.method(message_types.VoidMessage, 
                    messages.MarketplaceGetMessage,
                    http_method='GET',
                    name='get')
	def get(self, unused_request):
		"""Retornar a loja do usuário.
		"""

		logging.debug('Executando endpoint para obter a marketplace (loja) do usuário')

		#obter marketplaces (lojas) do usuário 
		marketplaceModel = models.get(user.get_current_user().email())

		#retorna a marketplace (loja) do usuário
		return messages.MarketplaceGetMessage(name=marketplaceModel.name, created_date=marketplaceModel.created_date)


	# Resource Container para POSTs
	MARKETPLACE_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(messages.MarketplacePostMessage)

	@endpoints.method(MARKETPLACE_MESSAGE_RESOURCE_CONTAINER, 
                    messages.MarketplaceGetMessage,
                    http_method='POST',
                    name='put')
	def put(self, request):
		"""Atualizar a loja do usuário.
		"""

		logging.debug('Executando endpoint para atualizar a marketplace (loja) do usuário')

		# Atualizar marketplace (loja) do usuário
		marketplaceModel = models.put(email=user.get_current_user().email(), name=request.name)

		#retorna a marketplace (loja) do usuário
		return messages.MarketplaceGetMessage(name=marketplaceModel.name, created_date=marketplaceModel.created_date)   
