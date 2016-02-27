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
from app.supplier import messages as supplier

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


class StockGetMessage(messages.Message):
    """ Endpoint message.
    """

    # Id
    id = messages.IntegerField(1)

    # Produto
    product = messages.MessageField(
        product.ProductGetMessage, 2, required=True)

    # Qtidade
    quantity = messages.IntegerField(3, required=True)

    # Data criação
    created_date = message_types.DateTimeField(4)


class StockCollectionMessage(messages.Message):
    """ Endpoint message.
    """

    items = messages.MessageField(StockGetMessage, 1, repeated=True)
