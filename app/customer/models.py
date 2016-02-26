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
from app import user
from app import util
from app.exceptions import NotFoundEntityException
from app.marketplace import models as marketplace
from google.appengine.ext import ndb
from google.appengine.api import search as search_api


__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


# Index autocomplete cliente
CUSTOMER_AUTOCOMPLETE_INDEX_NAME = 'customer_autocomplete_index'
AUTOCOMPLETE_SEARCH_LIMIT = 5


def get_autocomplete_index():
    return search_api.Index(name=CUSTOMER_AUTOCOMPLETE_INDEX_NAME)


class CustomerModel(ndb.Model):
    """Entidade representa um cliente da loja"""

    # Nome do cliente
    name = ndb.StringProperty(required=True)

    # Email de contato do cliente
    email = ndb.StringProperty(required=False)

    # Telefone de contato do cliente
    phone = ndb.StringProperty(required=False)

    # Localização
    location = ndb.StringProperty(required=False)

    # Data criação
    created_date = ndb.DateTimeProperty(auto_now_add=True)

# http://stackoverflow.com/questions/12899083/partial-matching-gae-search-api


def update_index(customer):
    name = ','.join(util.tokenize_autocomplete(customer.name))
    document = search_api.Document(
        doc_id=str(customer.key.id()),
        fields=[search_api.TextField(name='name', value=name)])
    get_autocomplete_index().put(document)


def remove_index(_id):
    get_autocomplete_index().remove(str(_id))


def get(id):
    """Selecionar um cliente cadastrado pelo id.
    """
    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    logging.debug("Loja encontrada com sucesso")

    # Realizando query, selecionando o cliente pelo pai e id
    customer = ndb.Key('CustomerModel', int(
        id), parent=marketplaceModel.key).get()

    logging.debug("Cliente encontrado com sucesso")

    return customer


def get_customer_query():
    """Retorna a query do CustomerModel.
    """

    logging.debug("Listando os clientes cadastrados")

    # Identificando usuário da requisição
    email = user.get_current_user().email()

    logging.debug("Obtendo a entidade da loja para o usuario %s", email)

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get(email)

    # Realizando query, listando os clientes
    query = CustomerModel.query(ancestor=marketplaceModel.key)

    return query


def list():
    """Listar os clientes cadastrados na loja do usuário.
    """

    # Realizando query, listando os clientes
    customers = get_customer_query().order(CustomerModel.name).fetch()

    logging.debug("Foram selecionado(s) %d clientes(s) cadastrados",
                  len(customers))

    # Retornando
    return customers


def search(customer):
    """Pesquisa dos clientes cadastrados na loja.
    """

    # Listando os clientes cadastrados
    items = list()

    logging.debug("Realizando a pesquisa indexada de clientes")

    # Realizando a pesquisa
    search_results = get_autocomplete_index().search(search_api.Query(
        query_string="name:{name}".format(name=customer.name),
        options=search_api.QueryOptions(limit=AUTOCOMPLETE_SEARCH_LIMIT)))

    # Convertendo docs para model
    results = []
    for doc in search_results:
        results.append(get(int(doc.doc_id)))

    # Retornando resultado
    return results


@ndb.transactional
def save(customer):
    """Inclui ou atualiza um cliente.
    """

    logging.debug("Persistindo um cliente na loja")

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    logging.debug(
        "Criando model para o cliente ou selecionando o existente")

    if customer.id is not None:
        customerModel = ndb.Key('CustomerModel', int(customer.id),
                                parent=marketplaceModel.key).get()
    else:
        customerModel = CustomerModel(parent=marketplaceModel.key)

    # Criando model
    customerModel.name = customer.name
    customerModel.email = customer.email
    customerModel.phone = customer.phone
    customerModel.location = customer.location

    # Persistindo cliente
    logging.debug("Persistindo cliente...")

    customerModel.put()

    logging.debug("Persistido cliente %d com sucesso na loja %s",
                  customerModel.key.id(), marketplaceModel.name)

    # Atualizando índice
    update_index(customerModel)
    logging.debug("Índice atualizado com sucesso para o cliente %s",
                  customerModel.key.id())

    # Retornando cliente cadastrado com o id
    return customerModel


@ndb.transactional
def delete(id):
    """Remove um cliente cadastrado.
    """

    logging.debug("Removendo o cliente %d persistido na loja", id)

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    logging.debug("Loja encontrada com sucesso")

    # Realizando query, selecionando o cliente pelo pai e id
    customer = ndb.Key('CustomerModel', int(
        id), parent=marketplaceModel.key).get()

    if customer is None:
        raise NotFoundEntityException(message='messages.customer.notfound')

    logging.debug("cliente encontrado com sucesso")

    customer.key.delete()

    logging.debug("cliente removido com sucesso")
