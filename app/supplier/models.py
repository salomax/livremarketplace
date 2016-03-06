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
SUPPLIER_AUTOCOMPLETE_INDEX_NAME = 'suplier_autocomplete_index'
AUTOCOMPLETE_SEARCH_LIMIT = 5


def get_autocomplete_index():
    return search_api.Index(name=SUPPLIER_AUTOCOMPLETE_INDEX_NAME)


class SupplierModel(ndb.Model):
    """ Supplier model.
    """

    # Name
    name = ndb.StringProperty(required=True)

    # Email
    email = ndb.StringProperty(required=False)

    # Phone
    phone = ndb.StringProperty(required=False)

    # Location
    location = ndb.StringProperty(required=False)

    # Insert date
    created_date = ndb.DateTimeProperty(auto_now_add=True)


def update_index(supplier):
    name = ','.join(util.tokenize_autocomplete(supplier.name))
    document = search_api.Document(
        doc_id=str(supplier.key.id()),
        fields=[search_api.TextField(name='name', value=name)])
    get_autocomplete_index().put(document)


def remove_index(_id):
    get_autocomplete_index().delete(str(_id))


def get(id):
    """ Select supplier by id.
    """

    marketplaceModel = marketplace.get_marketplace()

    supplier = ndb.Key('SupplierModel', int(
        id), parent=marketplaceModel.key).get()

    return supplier


def list():
    """ List suppliers.
    """

    marketplaceModel = marketplace.get_marketplace()

    suppliers = SupplierModel.query(ancestor=marketplaceModel.key).order(
        SupplierModel.name).fetch()

    return suppliers


def search(supplier):
    """ Search supplier by name.
    """

    results = []

    if not supplier.name:
        return results

    search_results = get_autocomplete_index().search(search_api.Query(
        query_string="name:{name}".format(name=supplier.name),
        options=search_api.QueryOptions(limit=AUTOCOMPLETE_SEARCH_LIMIT)))

    for doc in search_results:
        supplier = get(int(doc.doc_id))

        if supplier is not None:
            results.append(supplier)
        else:
            remove_index(doc.doc_id)
            logging.warning(
                'Index %s is not up-to-date to doc %s and it has removed!',
                SUPPLIER_AUTOCOMPLETE_INDEX_NAME, doc.doc_id)

    return results


@ndb.transactional
def save(supplier):
    """Inclui ou atualiza um fornecedor.
    """

    # Get parent
    marketplaceModel = marketplace.get_marketplace()

    logging.debug("Get user marketplace")

    if supplier.id is not None:

        # Create supplier with id
        supplierModel = SupplierModel(
            id=int(supplier.id), parent=marketplaceModel.key)

    else:

        # Create supplier with random unique id
        supplierModel = SupplierModel(parent=marketplaceModel.key)

    logging.debug("Supplier model created")

    # Set attributes
    supplierModel.name = supplier.name
    supplierModel.email = supplier.email
    supplierModel.phone = supplier.phone
    supplierModel.location = supplier.location

    logging.debug("Set attributes ok")

    # Perstite it
    supplierModel.put()

    logging.debug("Supplier %d persisted successfully",
                  supplierModel.key.id())

    # Update index
    update_index(supplierModel)

    logging.debug("Index updated to supplier %s",
                  supplierModel.key.id())

    # Return it
    return supplierModel


@ndb.transactional
def delete(id):
    """ Remove supplier by id.
    """

    logging.debug("Removing supplier %d", id)

    marketplaceModel = marketplace.get_marketplace()

    supplierKey = ndb.Key('SupplierModel', int(
        id), parent=marketplaceModel.key)

    if supplierKey is None:
        raise NotFoundEntityException(message='messages.supplier.notfound')

    logging.debug("Supplier %d found it!", id)

    # Are there purchases um this supplier,
    # if true, is not possible to delete
    from app.purchase import models as purchase
    if purchase.has_purchases_by_supplier(supplierKey) == True:
        raise IntegrityViolationException(
            message='messages.supplier.purchasesintegrityviolation')

    logging.debug("Check constraint validation OK")

    # Delete supplier
    supplierKey.delete()

    logging.debug("Supplier removed successfully")

    remove_index(id)

    logging.debug("Supplier index updated successfully")
