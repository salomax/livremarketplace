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
from messages import PurchasePostMessage
from messages import PurchaseGetMessage
from messages import PurchaseCollectionMessage
from app.product import messages as productMessages
from app.supplier import messages as supplierMessages
from app import user
from app import oauth
from protorpc import remote
from protorpc import messages
from protorpc import message_types

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


@endpoints.api(name='purchase',
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS,
               # ANDROID_AUDIENCE argument is required for Android clients and
               # is not used by other clients
               audiences=oauth.ALLOWED_CLIENT_IDS,
               # Although you can add other scopes, you must always include the
               # email scope if you use OAuth.
               scopes=[endpoints.EMAIL_SCOPE])
class PurchaseService(remote.Service):
    """ Service for management of purchases to the stock.
    """

    @endpoints.method(message_types.VoidMessage,
                      PurchaseCollectionMessage,
                      http_method='GET',
                      name='list')
    def list(self, unused_request):
        """ Return the purchases list.
        """

        purchases = models.list()

        items = []
        for purchaseModel in purchases:
            product = purchaseModel.product.get()
            supplier = purchaseModel.supplier.get()
            items.append(
                PurchaseGetMessage(
                    id=purchaseModel.key.id(),
                    supplier=supplierMessages.SupplierGetMessage(
                        id=supplier.key.id(),
                        name=supplier.name,
                        created_date=supplier.created_date
                    ),
                    product=productMessages.ProductGetMessage(
                        id=product.key.id(),
                        code=product.code,
                        name=product.name,
                        created_date=product.created_date
                    ),
                    quantity=purchaseModel.quantity,
                    purchase_date=purchaseModel.purchase_date,
                    received_date=purchaseModel.received_date,
                    cost=purchaseModel.cost,
                    total_cost=purchaseModel.total_cost,
                    exchange_dollar=purchaseModel.exchange_dollar,
                    cost_dollar=purchaseModel.cost_dollar,
                    total_cost_dollar=purchaseModel.total_cost_dollar,
                    shipping_cost=purchaseModel.shipping_cost,
                    track_code=purchaseModel.track_code,
                    invoice=purchaseModel.invoice,
                    payment_date=purchaseModel.payment_date,
                    purchase_link=purchaseModel.purchase_link,
                    created_date=purchaseModel.created_date))

        return PurchaseCollectionMessage(items=items)

    # Resource Container para POSTs
    PURCHASE_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(
        PurchasePostMessage)

    @endpoints.method(PURCHASE_MESSAGE_RESOURCE_CONTAINER,
                      PurchaseGetMessage,
                      http_method='POST',
                      name='save')
    def save(self, request):
        """ Add or update a purchase
        """

        purchaseModel = models.save(request)

        product = purchaseModel.product.get()
        supplier = purchaseModel.supplier.get()

        return PurchaseGetMessage(
            id=purchaseModel.key.id(),
            supplier=supplierMessages.SupplierGetMessage(
                id=supplier.key.id(),
                name=supplier.name,
                created_date=supplier.created_date
            ),
            product=productMessages.ProductGetMessage(
                id=product.key.id(),
                code=product.code,
                name=product.name,
                created_date=product.created_date
            ),
            quantity=purchaseModel.quantity,
            purchase_date=purchaseModel.purchase_date,
            received_date=purchaseModel.received_date,
            cost=purchaseModel.cost,
            total_cost=purchaseModel.total_cost,
            exchange_dollar=purchaseModel.exchange_dollar,
            cost_dollar=purchaseModel.cost_dollar,
            total_cost_dollar=purchaseModel.total_cost_dollar,
            shipping_cost=purchaseModel.shipping_cost,
            track_code=purchaseModel.track_code,
            invoice=purchaseModel.invoice,
            payment_date=purchaseModel.payment_date,
            purchase_link=purchaseModel.purchase_link,
            created_date=purchaseModel.created_date)

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT64))

    @endpoints.method(ID_RESOURCE,
                      message_types.VoidMessage,
                      path='{id}',
                      http_method='DELETE',
                      name='delete')
    def delete(self, request):
        """ Remove a purchase.
        """

        models.delete(request.id)

        return message_types.VoidMessage()
