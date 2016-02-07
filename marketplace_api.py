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

"""Python MarketPlace API """

# Importando sys e ajustando o encode para UTF-8, afim de contemplar acentuação
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import logging
import endpoints

from protorpc import message_types
from protorpc import remote

import app.user as user
import app.marketplace as marketplace
import app.purchase as purchase


WEB_CLIENT_ID = '768767255656-sct9bc9j1s9gvphm3o9g4tkifgo4p075.apps.googleusercontent.com'
#ANDROID_CLIENT_ID = 'replace this with your Android client ID'
#IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

@endpoints.api(name='marketplace', 
               version='v1',
               allowed_client_ids=[ WEB_CLIENT_ID, 
                                    #ANDROID_CLIENT_ID,
                                    #IOS_CLIENT_ID, 
                                    endpoints.API_EXPLORER_CLIENT_ID], # endpoints.API_EXPLORER_CLIENT_ID is needed for testing against the API Explorer in production.
               audiences=[ANDROID_AUDIENCE], # ANDROID_AUDIENCE argument is required for Android clients and is not used by other clients
               scopes=[endpoints.EMAIL_SCOPE]) # Although you can add other scopes, you must always include the email scope if you use OAuth.
class MarketPlaceApi(remote.Service):
  """
  Classe destinada à gerenciar a marketplace (loja) do usuário, suas compras (purchases) e vendas (sales).
  """

  @endpoints.method(message_types.VoidMessage, 
                    marketplace.MarketplaceGetMessage,
                    path='marketplace', 
                    http_method='GET',
                    name='get')
  def get_marketplace(self, unused_request):
    """
    Retorna a marketplace (loja) do usuário.
    """

    logging.debug('Executando endpoint para obter o marketplace do usuário')

    #obter marketplaces (lojas) do usuário 
    marketplaceModel = marketplace.get(user.get_current_user().email())

    #retorna a marketplace (loja) do usuário
    return marketplace.MarketplaceGetMessage(name=marketplaceModel.name, created_date=marketplaceModel.created_date)



  # Resource Container para POSTs
  MARKETPLACE_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(marketplace.MarketplacePostMessage)

  @endpoints.method(MARKETPLACE_MESSAGE_RESOURCE_CONTAINER, 
                    marketplace.MarketplaceGetMessage,
                    path='marketplace', 
                    http_method='POST',
                    name='put')
  def put_marketplace(self, request):
    """
    Atualiza a marketplace (loja) do usuário.
    """

    # Atualizar marketplace (loja) do usuário
    marketplaceModel = marketplace.put(email=user.get_current_user().email(), name=request.name)

    #retorna a marketplace (loja) do usuário
    return marketplace.MarketplaceGetMessage(name=marketplaceModel.name, created_date=marketplaceModel.created_date)   


  @endpoints.method(message_types.VoidMessage, 
                    marketplace.MarketplaceGetMessage,
                    path='marketplace', 
                    http_method='GET',
                    name='get')
  def get_marketplace(self, unused_request):
    """
    Retorna a marketplace (loja) do usuário.
    """

    logging.debug('Executando endpoint para obter o marketplace do usuário')

    #obter marketplaces (lojas) do usuário 
    marketplaceModel = marketplace.get(user.get_current_user().email())

    #retorna a marketplace (loja) do usuário
    return marketplace.MarketplaceGetMessage(name=marketplaceModel.name, created_date=marketplaceModel.created_date)



# TODO Reports

# Creating api server to bind in app.yaml
APPLICATION = endpoints.api_server([MarketPlaceApi])
