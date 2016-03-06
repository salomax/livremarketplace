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

from google.appengine.ext import ndb
from app.marketplace import models as marketplace
from app.product import models as product
from app.exceptions import NotFoundEntityException
from app.exceptions import IllegalStateException

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


class OpenMarketplaceModel(ndb.Model):

    def get_query(self):

        # Get parent marketplace
        marketplaceModel = marketplace.get_marketplace()

        # Get query
        return self.query(ancestor=marketplaceModel.key)


class StockItemModel(OpenMarketplaceModel):
    """ Stock item datastore entity.
    """

    # Product
    product = ndb.KeyProperty(kind=product.ProductModel, required=True)

    # Quantity
    quantity = ndb.IntegerProperty(required=True, default=0)


class StockLogModel(StockItemModel):
    """ Stock item datastore entity.
    """

    # Data criação
    created_date = ndb.DateTimeProperty(auto_now_add=True)


def update_stock(item, calculates):
    """ Add product to stock.
        Calculates the average product cost avaliable in stock.
    """

    # Get query
    query = StockItemModel().get_query()

    # Filter by product
    stock = query.filter(StockItemModel.product == item.product).get()

    # If it does not exists create new one...
    if stock is None:

        # Get market place parent
        marketplaceModel = marketplace.get_marketplace()

        # Create stock item
        stock = StockItemModel(parent=marketplaceModel.key,
                               product=item.product)

    # Calculate the quantity
    stock.quantity = stock.quantity + calculates(item.quantity)

    # Stock can't be less then zero
    if stock.quantity < 0:
        raise IllegalStateException(
            message='messages.stockitem.quantitynotlesszero')

    # Update datastore
    stock.put()

    # Add stock log
    stockLog = StockLogModel(parent=stock.key,
                             product=item.product,
                             quantity=calculates(item.quantity))

    # Update datastore
    stockLog.put()


def add_item_to_stock(item):
    """ Add product to stock.
        Calculates the average product cost avaliable in stock.
    """

    def calculates(a):
        return a

    update_stock(item, calculates)


def remove_item_from_stock(item):
    """ Remove quantity product from stock.
    """

    def calculates(a):
        return -a

    update_stock(item, calculates)


def list():
    """ List all stock items.
    """

    # Get query
    query = StockItemModel().get_query()

    # List all
    items = query.fetch()

    # Returns
    return items


def listLog():
    """ List all logs from stock.
    """

    # List all logs
    items = StockLogModel.query().order(-StockLogModel.created_date).fetch()

    # Returns
    return items    
