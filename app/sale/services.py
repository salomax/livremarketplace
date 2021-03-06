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


__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


@endpoints.api(name='sale',
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS,
               # ANDROID_AUDIENCE argument is required for Android clients and
               # is not used by other clients
               audiences=oauth.ALLOWED_CLIENT_IDS,
               # Although you can add other scopes, you must always include the
               # email scope if you use OAuth.
               scopes=[endpoints.EMAIL_SCOPE])
class SaleService(remote.Service):
    """ Service for management of sales.
    """

    # Resource Container para POSTs
    Sale_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(
        SalePostMessage)

    @endpoints.method(message_types.VoidMessage,
                      SaleCollectionMessage,
                      http_method='GET',
                      name='list')
    def list(self, unused_request):
        """ Return to the list of clients.
        """

        sales = models.list()

        items = []
        for saleModel in sales:

            # Get entities children 
            customerModel = saleModel.customer.get()
            productModel = saleModel.product.get()
            
            # Add to list
            items.append(
                SaleGetMessage(
                    id=saleModel.key.id(),
                    customer=customer.CustomerGetMessage(
                        id=customerModel.key.id(),
                        name=customerModel.name,
                        email=customerModel.email,
                        phone=customerModel.phone,
                        location=customerModel.location,
                        created_date=customerModel.created_date
                    ),
                    product=product.ProductGetMessage(
                        id=productModel.key.id(),
                        code=productModel.code,
                        name=productModel.name,
                        created_date=productModel.created_date
                    ),
                    quantity=saleModel.quantity,
                    sale_date=saleModel.sale_date,
                    amount=saleModel.amount,
                    fare=saleModel.fare,
                    net_total=saleModel.net_total,
                    track_code=saleModel.track_code,
                    created_date=saleModel.created_date))

        return SaleCollectionMessage(items=items)

    @endpoints.method(Sale_MESSAGE_RESOURCE_CONTAINER,
                      SaleGetMessage,
                      http_method='POST',
                      name='save')
    def save(self, request):
        """ Add or update a sale
        """
        saleModel = models.save(request)

        # Get entities children 
        customerModel = saleModel.customer.get()
        productModel = saleModel.product.get()

        # Retornando compra persistida
        return SaleGetMessage(
            id=saleModel.key.id(),
            customer=customer.CustomerGetMessage(
                id=customerModel.key.id(),
                name=customerModel.name,
                email=customerModel.email,
                phone=customerModel.phone,
                location=customerModel.location,
                created_date=customerModel.created_date
            ),
            product=product.ProductGetMessage(
                id=productModel.key.id(),
                code=productModel.code,
                name=productModel.name,
                created_date=productModel.created_date
            ),
            quantity=saleModel.quantity,
            sale_date=saleModel.sale_date,
            amount=saleModel.amount,
            fare=saleModel.fare,
            net_total=saleModel.net_total,
            track_code=saleModel.track_code,
            created_date=saleModel.created_date)

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT64))

    @endpoints.method(ID_RESOURCE,
                      message_types.VoidMessage,
                      path='{id}',
                      http_method='DELETE',
                      name='delete')
    def delete(self, request):
        """ Remove a sale
        """

        models.delete(request.id)

        return message_types.VoidMessage()
