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


# Index autocomplete produto
# http://stackoverflow.com/questions/12899083/partial-matching-gae-search-api
PRODUCT_AUTOCOMPLETE_INDEX_NAME = 'product_autocomplete_index'
AUTOCOMPLETE_SEARCH_LIMIT = 5


def get_autocomplete_index():
    return search_api.Index(name=PRODUCT_AUTOCOMPLETE_INDEX_NAME)


class ProductModel(ndb.Model):
    """Entidade representa um produto comercializado pela loja"""

    # Código de referência do Produto
    code = ndb.StringProperty(required=True)

    # Nome do Produto
    name = ndb.StringProperty(required=True)

    # Data criação
    created_date = ndb.DateTimeProperty(auto_now_add=True)


def update_index(product):
    name = ','.join(util.tokenize_autocomplete(product.name))
    code = ','.join(util.tokenize_autocomplete(product.code))
    document = search_api.Document(
        doc_id=str(product.key.id()),
        fields=[search_api.TextField(name='code', value=code),
                search_api.TextField(name='name', value=name)])
    get_autocomplete_index().put(document)


def delete_index(_id):
    get_autocomplete_index().delete(str(_id))


def get(id):
    """Selecionar um produto cadastrado pelo id.
    """

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    logging.debug("Loja encontrada com sucesso")

    # Realizando query, selecionando o produto pelo pai e id
    product = ndb.Key('ProductModel', int(
        id), parent=marketplaceModel.key).get()

    if product is None:
        raise NotFoundEntityException(message='messages.product.notfound')
        
    logging.debug("Produto encontrado com sucesso")

    return product


def list():
    """Listar os produtos cadastrados na loja do usuário.
    """

    logging.debug("Listando os produtos cadastrados")

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    # Realizando query, listando os produtos
    products = ProductModel.query(ancestor=marketplaceModel.key).order(
        ProductModel.name).fetch()

    logging.debug("Foram selecionado(s) %d produtos(s)",
                  len(products))

    # Retornando
    return products


def search(product):
    """Pesquisa dos produtos cadastrados na loja.
    """

    # Listando os produtos cadastrados
    items = list()

    logging.debug("Realizando a pesquisa indexada de produtos")

    # Realizando a pesquisa
    search_results = get_autocomplete_index().search(search_api.Query(
        query_string="code:{code} OR name:{name}".format(
            code=product.code, name=product.name),
        options=search_api.QueryOptions(limit=AUTOCOMPLETE_SEARCH_LIMIT)))

    # Convertendo docs para model
    results = []
    for doc in search_results:
        results.append(get(int(doc.doc_id)))

    # Retornando resultado
    return results


@ndb.transactional
def put(product):
    """Inclui ou atualiza um produto.
    """

    logging.debug("Persistindo um produto na loja")

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    logging.debug("Loja encontrada com sucesso")

    logging.debug(
        "Criando model para o produto ou selecionando o existente para atualizá-lo")

    if product.id is not None:
        productModel = ndb.Key('ProductModel', int(product.id),
                               parent=marketplaceModel.key).get()
    else:
        productModel = ProductModel(parent=marketplaceModel.key)

    # Criando model
    productModel.code = product.code
    productModel.name = product.name

    # Persistindo produto
    logging.debug("Persistindo produto...")

    productModel.put()

    logging.debug("Persistido produto %d com sucesso na loja %s",
                  productModel.key.id(), marketplaceModel.name)

    # Atualizando índice
    update_index(productModel)
    logging.debug("Índice atualizado com sucesso para o produto %s",
                  productModel.key.id())

    # Retornando produto cadastrado com o id
    return productModel


@ndb.transactional
def delete(id):
    """Remove um produto cadastrado.
    """

    logging.debug("Removendo o produto %d persistido na loja", id)

    # Obtendo marketplace como parent
    marketplaceModel = marketplace.get_marketplace()

    logging.debug("Loja encontrada com sucesso")

    # Realizando query, selecionando o produto pelo pai e id
    product = ndb.Key('ProductModel', int(
        id), parent=marketplaceModel.key).get()

    if product is None:
        raise NotFoundEntityException(message='messages.product.notfound')

    logging.debug("Produto encontrado com sucesso")

    product.key.delete()
    delete_index(id)

    logging.debug("Produto removido com sucesso")
