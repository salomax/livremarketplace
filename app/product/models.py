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
from app.exceptions import IntegrityViolationException
from app.marketplace import models as marketplace
from google.appengine.ext import ndb
from google.appengine.api import search as search_api


__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


# Index autocomplete produto
# http://stackoverflow.com/questions/12899083/partial-matching-gae-search-api
PRODUCT_INDEX_NAME = 'product_autocomplete_index'
AUTOCOMPLETE_SEARCH_LIMIT = 5


def get_index():
    return search_api.Index(name=PRODUCT_INDEX_NAME)


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

    get_index().put(document)


def delete_index(_id):
    get_index().delete(str(_id))


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

    results = []

    # handling no terms
    if not product.name and not product.code:
        return results

    # get results from index
    search_results = get_index().search(search_api.Query(
        query_string="code:{code} OR name:{name}".format(
            code=product.code, name=product.name),
        options=search_api.QueryOptions(limit=AUTOCOMPLETE_SEARCH_LIMIT)))

    # Getting models
    for doc in search_results:

        try:

            product = get(int(doc.doc_id))

            results.append(product)

        except NotFoundEntityException:

            delete_index(doc.doc_id)

            logging.warning(
                'Index %s is not up-to-date to doc %s and it has removed!',
                PRODUCT_INDEX_NAME, doc.doc_id)

    return results


@ndb.transactional
def save(product):
    """ Add or update product.
    """

    # Get parent
    marketplaceModel = marketplace.get_marketplace()

    logging.debug("Get user marketplace")

    if product.id is not None:

        # Create product with id
        productModel = ProductModel(
            id=int(product.id), parent=marketplaceModel.key)
    else:

        # Create product with random unique id
        productModel = ProductModel(parent=marketplaceModel.key)

    logging.debug("Created product model")

    # Set attributes
    productModel.code = product.code
    productModel.name = product.name

    logging.debug("Set attributes ok")

    # Perstite it
    productModel.put()

    logging.debug("Product model put successfully")

    # Update index
    update_index(productModel)

    logging.debug("Product model index update successfully")

    # Return product
    return productModel


@ndb.transactional
def delete(id):
    """ Remove a product.
    """

    logging.debug("Removing product %d", id)

    marketplaceModel = marketplace.get_marketplace()

    productKey = ndb.Key('ProductModel', int(
        id), parent=marketplaceModel.key)

    if productKey is None:
        raise NotFoundEntityException(message='messages.product.notfound')

    logging.debug("Product %d found it!", id)

    # Are there purchases this product,
    # if true, is not possible to delete
    from app.purchase import models as purchase
    if purchase.has_purchases_by_product(productKey) == True:
        raise IntegrityViolationException(
            message='messages.product.purchasesintegrityviolation')

    # Are there purchases this product,
    # if true, is not possible to delete
    from app.sale import models as sale
    if sale.has_sales_by_product(productKey) == True:
        raise IntegrityViolationException(
            message='messages.product.salesintegrityviolation')

    logging.debug("Check constraint validation OK")

    # Delete product
    productKey.delete()

    logging.debug("Product removed successfully")

    # Remove from index
    delete_index(id)

    logging.debug("Produc index updated successfully")
