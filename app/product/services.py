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
from messages import ProductPostMessage
from messages import ProductGetMessage
from messages import ProductCollectionMessage
from messages import ProductSearchMessage
from app import user
from app import oauth
from protorpc import remote
from protorpc import messages
from protorpc import message_types


__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


@endpoints.api(name='product',
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS,
               # ANDROID_AUDIENCE argument is required for Android clients and
               # is not used by other clients
               audiences=oauth.ALLOWED_CLIENT_IDS,
               # Although you can add other scopes,
               # you must always include the email scope if you use OAuth.
               scopes=[endpoints.EMAIL_SCOPE])
class ProductService(remote.Service):
    """ Service for management of products.
    """

    Product_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(
        ProductPostMessage)
    Product_Search_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(
        ProductSearchMessage)

    @endpoints.method(message_types.VoidMessage,
                      ProductCollectionMessage,
                      http_method='GET',
                      name='list')
    def list(self, unused_request):
        """ Return to product list.
        """

        products = models.list()

        items = []
        for ProductModel in products:
            items.append(
                ProductGetMessage(
                    id=ProductModel.key.id(),
                    code=ProductModel.code,
                    name=ProductModel.name,
                    created_date=ProductModel.created_date))

        return ProductCollectionMessage(items=items)

    @endpoints.method(Product_Search_MESSAGE_RESOURCE_CONTAINER,
                      ProductCollectionMessage,
                      http_method='POST',
                      name='search')
    def search(self, request):
        """ Perform a search product.
        """
        products = models.search(request)

        items = []
        for ProductModel in products:
            items.append(
                ProductGetMessage(
                    id=ProductModel.key.id(),
                    code=ProductModel.code,
                    name=ProductModel.name,
                    created_date=ProductModel.created_date))

        return ProductCollectionMessage(items=items)

    @endpoints.method(Product_MESSAGE_RESOURCE_CONTAINER,
                      ProductGetMessage,
                      http_method='POST',
                      name='save')
    def save(self, request):
        """ Add or update a product.
        """

        ProductModel = models.save(request)

        return ProductGetMessage(
            id=ProductModel.key.id(),
            code=ProductModel.code,
            name=ProductModel.name,
            created_date=ProductModel.created_date)

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT64))

    @endpoints.method(ID_RESOURCE,
                      message_types.VoidMessage,
                      path='{id}',
                      http_method='DELETE',
                      name='delete')
    def delete(self, request):
        """ remove a product.
        """

        models.delete(request.id)

        return message_types.VoidMessage()
