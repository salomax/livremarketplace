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
import datetime
from itertools import groupby

from app import user
from app import util

from app.product import models as productModel
from app.customer import models as customer
from app.marketplace import models as marketplace
from app.exceptions import NotFoundEntityException

from google.appengine.ext import ndb
from google.appengine.api import search as search_api


__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


class SaleModel(ndb.Model):
    """Entidade representa uma venda realizada.
    """

    # Cliente
    customer = ndb.KeyProperty(
        kind='CustomerModel', indexed=True, required=True)

    # Produto
    product = ndb.KeyProperty(
        kind='ProductModel', indexed=True, required=True)

    # Quantidade
    quantity = ndb.IntegerProperty(required=True, default=1)

    # Data Venda
    sale_date = ndb.DateTimeProperty(
        required=True, default=datetime.datetime.today())

    # Valor Total
    amount = ndb.FloatProperty(required=True)

    # Tarifa Venda
    fare = ndb.FloatProperty(required=False)

    # Total Líquido
    net_total = ndb.FloatProperty(required=True)

    # Cód Rastreamento
    track_code = ndb.StringProperty(indexed=False)

    # Data criação
    created_date = ndb.DateTimeProperty(auto_now_add=True)


def get(id):
    """Selecionar uma venda pelo id.
    """

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    # Realizando query, selecionando a venda pelo pai e id
    sale = ndb.Key('SaleModel', int(id), parent=marketplaceModel.key).get()

    if sale is None:
        raise IndexError("Venda não encontrada!")

    logging.debug("Venda encontrado com sucesso")

    return customer


def get_sales_query():
    """ Retorna a query.
    """

    logging.debug("Listando os clientes cadastrados")

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    # Retorna query
    return SaleModel.query(ancestor=marketplaceModel.key)


def list():
    """Listar as vendas realizadas.
    """
    # Realizando query, listando os clientes
    sales = get_sales_query().fetch()

    logging.debug("Foram selecionada(s) %d venda(s)", len(sales))

    # Retornando
    return sales


@ndb.transactional
def save(sale):
    """Incluir ou atualizar uma venda.
    """

    logging.debug("Persistindo uma venda na loja")

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    logging.debug("Loja encontrada com sucesso")

    logging.debug(
        "Criando model para o cliente ou selecionando o existente")

    if sale.id is not None:
        saleModel = ndb.Key('SaleModel', int(sale.id),
                            parent=marketplaceModel.key).get()
    else:
        saleModel = SaleModel(parent=marketplaceModel.key)

    # Selecionando produto
    productModel = ndb.Key('ProductModel', int(sale.product.id),
                           parent=marketplaceModel.key)
    if productModel is None:
        raise IndexError("Produto com o id %d não encontrado!",
                         sale.product.id)

    # Selecionando cliente
    customerModel = ndb.Key('CustomerModel', int(sale.customer.id),
                            parent=marketplaceModel.key)

    if customerModel is None:
        raise IndexError("Cliente com o id %d não encontrado!",
                         sale.customer.id)

    saleModel.product = productModel
    saleModel.customer = customerModel
    saleModel.quantity = sale.quantity
    saleModel.sale_date = sale.sale_date
    saleModel.amount = sale.amount
    saleModel.fare = sale.fare
    saleModel.net_total = sale.net_total
    saleModel.track_code = sale.track_code

    logging.debug("Persistindo venda...")

    saleModel.put()

    logging.debug("Persistida venda %d com sucesso na loja %s",
                  saleModel.key.id(), marketplaceModel.name)

    # Retornando cliente cadastrado com o id
    return saleModel


@ndb.transactional
def delete(id):
    """Remove uma venda realizada.
    """

    logging.debug("Removendo a venda %d persistida na loja", id)

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    logging.debug("Loja encontrada com sucesso")

    # Realizando query, selecionando o cliente pelo pai e id
    sale = ndb.Key('SaleModel', int(id), parent=marketplaceModel.key).get()

    if sale is None:
        raise IndexError("Venda não encontrada!")

    logging.debug("Venda encontrada com sucesso")

    sale.key.delete()

    logging.debug("Venda removida com sucesso")


def report_customers_by_products():
    """ List customers have ever bought at once.
        The result is grouped by product.
    """

    # List all sales
    sales = get_sales_query().fetch()

    # Create result variable
    result = []

    # Group by products
    data = sorted(sales, key=lambda t: t.product.key.id())
    for k, g in groupby(data, key=lambda t: t.product.key.id()):

        # Create variables
        customers = []
        product = None

        # Create group and get product
        for sale in g:
            # product must be setted one time
            # Avoiding overhead unecessary
            if product is None:
                product = sale.product.key.get()
            customers.append(sale.customer.key.get())

        # Create dict with key and value
        result.append({
            'product': product,
            'customers': customers
        })

    # Return
    return result


def report_products_by_customers():
    """ List products grouped by its customers.
    """

    # List all sales
    sales = get_sales_query().fetch()

    # Create result variable
    result = []

    # Group by customers
    data = sorted(sales, key=lambda t: t.customer.key.id())
    for k, g in groupby(data, key=lambda t: t.customer.key.id()):

        # Create variables
        products = []
        customer = None

        # Create group and get customer
        for sale in g:
            # customer must be setted one time
            # Avoiding overhead unecessary
            if customer is None:
                customer = sale.customer.key.get()
            products.append(sale.product.key.get())

        # Create dict with key and value
        result.append({
            'customer': customer,
            'products': products
        })

    # Return
    return result


def get_stats_by_products():
    """ Get sales statistics
    """

    # Get all sales
    sales = list()

    # Init result variable
    stats_sales_products = []

    # Group by product
    data = sorted(sales, key=lambda t: t.product.id())
    for k, g in groupby(data, key=lambda t: t.product.id()):

        # Create variables
        product = None
        sum_quantity = 0
        sum_net_profit = 0.0
        sum_weighted_net_profit = 0.0
        sum_unit_net_profit = 0.0
        index = 0

        # Create group and get product
        for sale in g:

            # product must be setted one time
            # Avoiding overhead unecessary
            if product is None:
                product = sale.product.get()

            # Sum quantities
            sum_quantity = sum_quantity + sale.quantity

            # Sum net profits
            sum_net_profit = sum_net_profit + sale.net_total

            # Sum unit net profit
            sum_unit_net_profit = sum_unit_net_profit + \
                (sale.net_total / float(sale.quantity))

            # Sum weighted net profit
            sum_weighted_net_profit = sum_weighted_net_profit + sale.net_total

            # index++
            index = index + 1

        # Calculate average net profit
        avg_net_profit = sum_unit_net_profit / index

        # Calculate weighted average net profit
        weighted_avg_net_profit = sum_weighted_net_profit / float(sum_quantity)

        # Create dict with key and value
        stats_sales_products.append({
            'product': product,
            'sum_quantity': sum_quantity,
            'sum_net_profit': sum_net_profit,
            'avg_net_profit': avg_net_profit,
            'weighted_avg_net_profit': weighted_avg_net_profit
        })

    return stats_sales_products
