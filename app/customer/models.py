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
CUSTOMER_NAME_INDEX = 'customer_autocomplete_index'
AUTOCOMPLETE_SEARCH_LIMIT = 5

# Index usage
# http://stackoverflow.com/questions/12899083/partial-matching-gae-search-api


def get_name_index():
    """ Customer index by name.
    """
    return search_api.Index(name=CUSTOMER_NAME_INDEX)


class CustomerModel(ndb.Model):
    """ Customer model.
    """

    # Name
    name = ndb.StringProperty(required=True)

    # Email
    email = ndb.StringProperty(required=False)

    # Phone
    phone = ndb.StringProperty(required=False)

    # Location
    location = ndb.StringProperty(required=False)

    # Log date at insert moment
    created_date = ndb.DateTimeProperty(auto_now_add=True)


def update_index(customer):
    """ Update index by customer id.
    """

    # Create partials
    name = ','.join(util.tokenize_autocomplete(customer.name))

    # Create a doc
    document = search_api.Document(
        doc_id=str(customer.key.id()),
        fields=[search_api.TextField(name='name', value=name)])

    # Add doc to index
    get_name_index().put(document)


def remove_index(_id):
    """  Remove index by id.
    """

    # Delete
    get_name_index().delete(str(_id))


def get_customer_query():
    """ Get customer model query.
    """

    # Get user marketplace
    marketplaceModel = marketplace.get_marketplace()

    # Get query, notice marketplace as parent
    query = CustomerModel.query(ancestor=marketplaceModel.key)

    # Return query
    return query


def get(id):
    """ Get customer by its id.
    """

    # Get marketplace
    marketplaceModel = marketplace.get_marketplace()

    # Get customer by id, notice marketplace as parent
    customer = ndb.Key('CustomerModel', int(
        id), parent=marketplaceModel.key).get()

    # Return customer
    return customer


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
    """ Search 
    """

    # Build search by name using index
    search_results = get_name_index().search(search_api.Query(
        query_string="name:{name}".format(name=customer.name),
        options=search_api.QueryOptions(limit=AUTOCOMPLETE_SEARCH_LIMIT)))

    # Transport results do model
    results = []
    for doc in search_results:

        # Get customer model
        customer = get(int(doc.doc_id))

        # Handle if not exists
        if customer is not None:
            results.append(customer)
        else:
            remove_index(doc.doc_id)
            logging.warning(
                'Index %s is not up-to-date to doc %s and it has removed!',
                CUSTOMER_NAME_INDEX, doc.doc_id)

    # Return
    return results


@ndb.transactional
def save(customer):
    """ Add or update a customer in datastore.
    """

    # Get marketplace
    marketplaceModel = marketplace.get_marketplace()

    # Get customer model if exists
    # or instantiate one, instead.
    if customer.id is not None:
        customerModel = ndb.Key('CustomerModel', int(customer.id),
                                parent=marketplaceModel.key).get()
    else:
        customerModel = CustomerModel(parent=marketplaceModel.key)

    # Pass values
    customerModel.name = customer.name
    customerModel.email = customer.email
    customerModel.phone = customer.phone
    customerModel.location = customer.location

    # Persist ir
    customerModel.put()

    logging.debug("Customer id %d saved success to %s",
                  customerModel.key.id(), marketplaceModel.name)

    # Update index
    update_index(customerModel)

    logging.debug("Index updated to customer id %s",
                  customerModel.key.id())

    # Return
    return customerModel


@ndb.transactional
def delete(id):
    """ Remove customer by id.
    """

    # Get marketplace
    marketplaceModel = marketplace.get_marketplace()

    # Get customer
    customer = ndb.Key('CustomerModel', int(
        id), parent=marketplaceModel.key).get()

    # Handle if not exists
    if customer is None:
        raise NotFoundEntityException(message='messages.customer.notfound')

    # Remove from datastore
    customer.key.delete()

    logging.debug("Customer id %s removed success!", id)

    # Update index
    remove_index(id)

    logging.debug("Index updated to customer id %s", id)
