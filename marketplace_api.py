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

import endpoints
import app.purchase as purchase

from protorpc import message_types
from protorpc import remote


WEB_CLIENT_ID = '768767255656-sct9bc9j1s9gvphm3o9g4tkifgo4p075.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
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
  Classe com os métodos de compras (purchases) e vendas (sales).
  """

  @endpoints.method(message_types.VoidMessage, 
                    purchase.PurchaseCollection,
                    path='marketplace', 
                    http_method='GET',
                    name='purchase.list')
  def purchase_list(self, unused_request):
    """
    Método lista as compras realizadas pelo usuário.
    """

    # Obter usuário logado
    current_user = endpoints.get_current_user()

    print current_user.user_id()

    # Validar usuário
    #if current_user is None
    #  raise endpoints.NotFoundException('Usuário %s não encontrado.' % email)

    return purchase.get_purchases()


# TODO Reports

# Creating api server to bind in app.yaml
APPLICATION = endpoints.api_server([MarketPlaceApi])
