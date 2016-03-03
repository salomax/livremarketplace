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


from protorpc import messages
from protorpc import message_types
from app.product import messages as product
from app.customer import messages as customer

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


class SaleKeyMessage(messages.Message):
    """ Get message for sale key.
    """

    id = messages.IntegerField(1)


class SaleGetMessage(messages.Message):
    """ Get message for sale.
    """

    id = messages.IntegerField(1)

    customer = messages.MessageField(
        customer.CustomerGetMessage, 2, required=True)

    product = messages.MessageField(product.ProductGetMessage, 3, required=True)

    quantity = messages.IntegerField(4, required=True)

    sale_date = message_types.DateTimeField(5, required=True)

    amount = messages.FloatField(6)

    fare = messages.FloatField(7)

    net_total = messages.FloatField(8)

    track_code = messages.StringField(9)

    created_date = message_types.DateTimeField(10, required=True)


class SalePostMessage(messages.Message):
    """ POST message for sale.
    """

    id = messages.IntegerField(1)

    customer = messages.MessageField(
        customer.CustomerKeyMessage, 2, required=True)

    product = messages.MessageField(product.ProductKeyMessage, 3, required=True)

    quantity = messages.IntegerField(4, required=True)

    sale_date = message_types.DateTimeField(5, required=True)

    amount = messages.FloatField(6)

    fare = messages.FloatField(7)

    net_total = messages.FloatField(8)

    track_code = messages.StringField(9)


class SaleCollectionMessage(messages.Message):
    """ Sales collection.
    """

    items = messages.MessageField(SaleGetMessage, 1, repeated=True)
