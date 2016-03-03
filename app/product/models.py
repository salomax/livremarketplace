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
    """ Product model.
    """

    code = ndb.StringProperty(required=True)

    name = ndb.StringProperty(required=True)

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
    """ Get product by id.
    """

    marketplaceModel = marketplace.get_marketplace()

    product = ndb.Key('ProductModel', int(
        id), parent=marketplaceModel.key).get()

    if product is None:
        raise NotFoundEntityException(message='messages.product.notfound')

    return product


def list():
    """ List all products.
    """
    marketplaceModel = marketplace.get_marketplace()

    products = ProductModel.query(ancestor=marketplaceModel.key).order(
        ProductModel.name).fetch()

    return products


def search(product):
    """ Seaching product by some text.
    """

    # get results from index
    search_results = get_autocomplete_index().search(search_api.Query(
        query_string="code:{code} OR name:{name}".format(
            code=product.code, name=product.name),
        options=search_api.QueryOptions(limit=AUTOCOMPLETE_SEARCH_LIMIT)))

    # Getting models
    results = []
    for doc in search_results:
        product = get(int(doc.doc_id))

        if product is not None:
            results.append(product)
        else:
            remove_index(doc.doc_id)
            logging.warning(
                'Index %s is not up-to-date to doc %s and it has removed!',
                PRODUCT_AUTOCOMPLETE_INDEX_NAME, doc.doc_id)

    return results


@ndb.transactional
def put(product):
    """ Add or update product.
    """
    marketplaceModel = marketplace.get_marketplace()

    if product.id is not None:
        productModel = ndb.Key('ProductModel', int(product.id),
                               parent=marketplaceModel.key).get()
    else:
        productModel = ProductModel(parent=marketplaceModel.key)

    productModel.code = product.code
    productModel.name = product.name

    productModel.put()

    update_index(productModel)

    return productModel


@ndb.transactional
def delete(id):
    """ Remove a product.
    """

    marketplaceModel = marketplace.get_marketplace()

    product = ndb.Key('ProductModel', int(
        id), parent=marketplaceModel.key).get()

    if product is None:
        raise NotFoundEntityException(message='messages.product.notfound')

    product.key.delete()

    delete_index(id)
