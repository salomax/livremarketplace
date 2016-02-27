#!/usr/bin/env python
# coding: utf-8
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


import logging
import endpoints
import models
from messages import StockGetMessage
from messages import StockCollectionMessage
from app.product.messages import ProductGetMessage

from app import oauth
from protorpc import remote
from protorpc import messages
from protorpc import message_types

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


@endpoints.api(name='stock',
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS,
               # ANDROID_AUDIENCE argument is required for Android clients and
               # is not used by other clients
               audiences=oauth.ALLOWED_CLIENT_IDS,
               # Although you can add other scopes, you must always include the
               # email scope if you use OAuth.
               scopes=[endpoints.EMAIL_SCOPE])
class StockService(remote.Service):
    """ Endpoint service to manages stock.
    """

    @endpoints.method(message_types.VoidMessage,
                      StockCollectionMessage,
                      http_method='GET',
                      name='list')
    def list(self, unused_request):
        """ Endpoint method aims to list all stock items.
        """

        # List all stock items
        stockItems = models.list()

        # Declarando lista e convertendo model para message
        items = []
        for stockItem in stockItems:
            product = stockItem.product.get()
            items.append(
                StockGetMessage(id=stockItem.key.id(),
                                product=ProductGetMessage(
                                    id=product.key.id(),
                                    code=product.code,
                                    name=product.name,
                                    created_date=product.created_date
                ),
                    quantity=stockItem.quantity))

        # Retornando compras
        return StockCollectionMessage(items=items)

    @endpoints.method(message_types.VoidMessage,
                      StockCollectionMessage,
                      http_method='GET',
                      name='listLog')
    def listLog(self, unused_request):
        """ Endpoint method aims to list all stock items.
        """

        # List all stock items
        stockItems = models.listLog()

        # Declarando lista e convertendo model para message
        items = []
        for stockItem in stockItems:
            product = stockItem.product.get()
            items.append(
                StockGetMessage(id=stockItem.key.id(),
                                product=ProductGetMessage(
                                    id=product.key.id(),
                                    code=product.code,
                                    name=product.name,
                                    created_date=product.created_date
                ),
                    quantity=stockItem.quantity,
                    created_date=stockItem.created_date))

        # Retornando compras
        return StockCollectionMessage(items=items)