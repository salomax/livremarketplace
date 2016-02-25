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
    """Venda. Mensagem GET a ser trafegada pelo endpoint.
    """

    # Id
    id = messages.IntegerField(1)


class SaleGetMessage(messages.Message):
    """Venda. Mensagem GET a ser trafegada pelo endpoint.
    """

    # Id
    id = messages.IntegerField(1)

    # Cliente
    customer = messages.MessageField(
        customer.CustomerGetMessage, 2, required=True)

    # Produto
    product = messages.MessageField(product.ProductGetMessage, 3, required=True)

    # Quantidade
    quantity = messages.IntegerField(4, required=True)

    # Data Venda
    sale_date = message_types.DateTimeField(5, required=True)

    # Valor Total
    amount = messages.FloatField(6)

    # Tarifa Venda
    fare = messages.FloatField(7)

    # Total Líquido
    net_total = messages.FloatField(8)

    # Cód Rastreamento
    track_code = messages.StringField(9)

    # Data criação
    created_date = message_types.DateTimeField(10, required=True)


class SalePostMessage(messages.Message):
    """Venda. Mensagem POST a ser trafegada pelo endpoint.
    """

    # Id
    id = messages.IntegerField(1)

    # Cliente
    customer = messages.MessageField(
        customer.CustomerKeyMessage, 2, required=True)

    # Produto
    product = messages.MessageField(product.ProductKeyMessage, 3, required=True)

    # Quantidade
    quantity = messages.IntegerField(4, required=True)

    # Data Venda
    sale_date = message_types.DateTimeField(5, required=True)

    # Valor Total
    amount = messages.FloatField(6)

    # Tarifa Venda
    fare = messages.FloatField(7)

    # Total Líquido
    net_total = messages.FloatField(8)

    # Cód Rastreamento
    track_code = messages.StringField(9)


class SaleCollectionMessage(messages.Message):
    """Coleção de vendas.
    """

    items = messages.MessageField(SaleGetMessage, 1, repeated=True)
