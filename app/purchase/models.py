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
from app.marketplace import models as marketplace
from app.product import models as product
from app.supplier import models as supplier
from app.stock import models as stock
from google.appengine.ext import ndb

from app.exceptions import NotFoundEntityException

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


class PurchaseModel(ndb.Model):
    """ Purchase model.
    """

    supplier = ndb.LocalStructuredProperty(
        supplier.SupplierModel, keep_keys=True, required=True, repeated=False)

    product = ndb.LocalStructuredProperty(
        product.ProductModel, keep_keys=True, required=True, repeated=False)

    quantity = ndb.IntegerProperty(required=True, default=1)

    purchase_date = ndb.DateTimeProperty(
        required=True, default=datetime.datetime.today())

    received_date = ndb.DateTimeProperty()

    payment_date = ndb.DateTimeProperty(required=True)

    cost = ndb.FloatProperty(required=True)

    total_cost = ndb.FloatProperty(required=True)

    exchange_dollar = ndb.FloatProperty()

    cost_dollar = ndb.FloatProperty()

    total_cost_dollar = ndb.FloatProperty()

    shipping_cost = ndb.FloatProperty()

    track_code = ndb.StringProperty(indexed=False)

    invoice = ndb.StringProperty(indexed=False)

    purchase_link = ndb.StringProperty(indexed=False)

    created_date = ndb.DateTimeProperty(auto_now_add=True)


def get_query_purchase():
    """ Get purchase model query.
    """

    marketplaceModel = marketplace.get_marketplace()

    purchasesQuery = PurchaseModel.query(ancestor=marketplaceModel.key)

    return purchasesQuery

 
def list():
    """ List purchases.
    """

    purchases = get_query_purchase().order(
        -PurchaseModel.purchase_date).fetch()

    return purchases


@ndb.transactional
def put(purchase):
    """ Add or update for purchase.
    """

    marketplaceModel = marketplace.get_marketplace()

    if purchase.id is not None:
        purchaseModel = ndb.Key('PurchaseModel', int(purchase.id),
                                parent=marketplaceModel.key).get()

        stock.remove_item_from_stock(purchaseModel)

    else:
        purchaseModel = PurchaseModel(parent=marketplaceModel.key)

    productModel = ndb.Key('ProductModel', int(purchase.product.id),
                           parent=marketplaceModel.key).get()
    if productModel is None:
        raise NotFoundEntityException("messages.product.notfound")

    purchaseModel.product = productModel

    supplierModel = ndb.Key('SupplierModel', int(purchase.supplier.id),
                            parent=marketplaceModel.key).get()
    if supplierModel is None:
        raise NotFoundEntityException("messages.supplier.notfound")

    purchaseModel.supplier = supplierModel

    purchaseModel.quantity = purchase.quantity
    purchaseModel.purchase_date = purchase.purchase_date
    purchaseModel.received_date = purchase.received_date
    purchaseModel.cost = purchase.cost
    purchaseModel.total_cost = purchase.total_cost
    purchaseModel.exchange_dollar = purchase.exchange_dollar
    purchaseModel.cost_dollar = purchase.cost_dollar
    purchaseModel.total_cost_dollar = purchase.total_cost_dollar
    purchaseModel.shipping_cost = purchase.shipping_cost
    purchaseModel.track_code = purchase.track_code
    purchaseModel.invoice = purchase.invoice
    purchaseModel.payment_date = purchase.payment_date
    purchaseModel.purchase_link = purchase.purchase_link

    purchaseModel.put()

    # Update stock
    stock.add_item_to_stock(purchaseModel)

    return purchaseModel


@ndb.transactional
def delete(id):
    """ Remove purchase.
    """

    marketplaceModel = marketplace.get_marketplace()

    purchase = ndb.Key('PurchaseModel', int(
        id), parent=marketplaceModel.key).get()

    if purchase is None:
        raise NotFoundEntityException("messages.purchase.notfound")

    # Update stock
    stock.remove_item_from_stock(purchase)

    # Delete from datastore
    purchase.key.delete()


def get_stats_by_products():
    """ Get purchases statistics by products
    """

    # Get all purchases
    purchases = list()

    # Init result variable
    stat_purchase_products = []

    # Group by product
    data = sorted(purchases, key=lambda t: t.product.key.id())
    for k, g in groupby(data, key=lambda t: t.product.key.id()):

        # Create variables
        product = None
        sum_quantity = 0
        sum_cost = 0.0
        sum_weighted_cost = 0.0
        index = 0

        # Create group and get product
        for purchase in g:

            # product must be setted one time
            # Avoiding overhead unecessary
            if product is None:
                product = purchase.product.key.get()

            # Sum quantities
            sum_quantity = sum_quantity + purchase.quantity

            # Sum net profits
            sum_cost = sum_cost + purchase.cost

            # Sum weighted
            sum_weighted_cost = sum_weighted_cost + \
                (purchase.quantity * purchase.cost)

            # index++
            index = index + 1

        # Calculate average net profit
        avg_cost = sum_cost / index

        # Calculate weighted average net profit
        weighted_avg_cost = sum_weighted_cost / float(sum_quantity)

        # Create dict with key and value
        stat_purchase_products.append({
            'product': product,
            'sum_quantity': sum_quantity,
            'sum_cost': sum_cost,
            'avg_cost': avg_cost,
            'weighted_avg_cost': weighted_avg_cost
        })

    print stat_purchase_products

    return stat_purchase_products
