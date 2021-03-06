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
import dateutil.relativedelta
from dateutil.relativedelta import relativedelta

from operator import itemgetter

from app import user
from app import util
from app.marketplace import models as marketplace
from app.sale import models as salesModel
from app.customer import models as customersModel
from app.purchase import models as purchasesModel
from app.exceptions import NotFoundEntityException

from google.appengine.ext import ndb
from google.appengine.api import search as search_api

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


def calculate_average_ticket():
    """ Calculate average ticket sale.
    """

    # Get all sales
    sales = salesModel.list()

    # Init vars
    total_revenue = 0
    count = 0

    # For each sale, sum amounts
    for sale in sales:
        total_revenue = total_revenue + sale.amount
        count = count + 1

    # Avoid division by zero
    if total_revenue == 0 or count == 0:
        return 0.0

    # Calculate average
    return total_revenue / count


def calculate_count_customers():
    """ Count how many customers there are.
    """

    # Return count
    return customersModel.get_customer_query().count()


def calculate_count_sales():
    """ Count how many sales there are.
    """

    # Return count
    return salesModel.get_sales_query().count()


def calculate_total_net_profit():
    """ Calculate total profit.
    """

    logging.debug('Listing sales')
    # get sales stats
    saleStats = salesModel.get_stats_by_products()

    logging.debug('Listing purchases')
    # get purchases stats
    purchaseStats = purchasesModel.get_stats_by_products()

    # The profit margin is the weighted avg
    # from sales, where quantity as weight and
    # (weighted avg net profit - weighted avg unit cost)
    # as the number to calculate avg
    #
    # For instance, if you have 80% sales wich
    # specific product, it will be considered more than
    # the other 20%.

    logging.debug('Calculating net profit')
    sum_net_profit = 0.0
    for sale in saleStats:

        # Search purchase by product
        purchases = [x for x in purchaseStats if x['product'].key.id()
                     == sale['product'].key.id()]

        if len(purchases) == 1:
            purchase = purchases[0]

            # Calculate the diference between net (sale value minus tax)
            # minus product cost
            sum_net_profit = sum_net_profit + (sale['weighted_avg_net_profit'] -
                                               purchase['weighted_avg_cost']
                                               ) * sale['sum_quantity']

        else:
            logging.warning("Product %s didn't find!", sale['product'].name)

    # Return
    return sum_net_profit


def calculate_profit_margin():
    """ Calculate total profit margin.
    """

    logging.debug('Calculatie profit margin')

    # Get revenue
    revenue = calculate_total_revenue()

    # Avoid division by zero
    if revenue == 0:
        return .0

    # Get net total value
    profit = calculate_total_net_profit()

    logging.debug(
        'Calculating profit margin. profit %d over revenue %d',
        profit, revenue)

    # % profit over revenue
    profit_margin = profit / revenue

    # Return
    return profit_margin


def calculate_total_revenue():
    """ Calculate total revenue.
    """

    # Get all sales
    sales = salesModel.list()

    # Init vars
    total_revenue = 0.0

    # For each sale, sum amounts
    for sale in sales:
        total_revenue = total_revenue + sale.amount

    # Return
    return total_revenue


def cash_flow(n):
    """ Get cash flow.
    """

    # Create dict for last 'n' months
    list = list_monthly(n)

    # Get min date to query filter
    date = datetime.datetime.now() - dateutil.relativedelta.relativedelta(
        months=n)

    # Get purchases query
    queryPurchases = purchasesModel.get_query_purchase()

    # Get purchases by date filter
    purchases = queryPurchases.filter(
        purchasesModel.PurchaseModel.purchase_date > date).fetch(
        projection=[purchasesModel.PurchaseModel.total_cost,
                    purchasesModel.PurchaseModel.payment_date])

    # Group by period
    for purchase in purchases:
        for i in list:
            if same_period(purchase.payment_date, i['period']):
                i['purchases'] = round(i['purchases'] + purchase.total_cost, 2)

    # Get sales query
    salesQuery = salesModel.get_sales_query()

    # Get sales by date filter
    sales = salesQuery.filter(
        salesModel.SaleModel.sale_date > date).fetch(
        projection=[salesModel.SaleModel.amount,
                    salesModel.SaleModel.sale_date])

    # Group by period
    for sale in sales:
        for i in list:
            if same_period(sale.sale_date, i['period']):
                i['sales'] = round(i['sales'] + sale.amount, 2)

    # Calculate balance and accumulated balance
    accumulated_balance = 0.0
    for month in list:
        month['balance'] = round(month['sales'] - month['purchases'], 2)
        accumulated_balance = accumulated_balance + month['balance']
        month['accumulated_balance'] = round(accumulated_balance, 2)

    # return list
    return list


def list_monthly(n):
    """ Create dict for last 'n' months to cash flow.
    """

    # Month in advance
    offset = 1
    
    # Init vars
    now = datetime.datetime.now() + relativedelta(months=offset)
    timeMap = []
    year = now.year
    month = now.month

    # Create for each month
    for x in range(n + offset):

        # Create dict
        timeMap.append({"period": datetime.datetime(year, month, 1),
                        "purchases": 0.0,
                        "sales": 0.0,
                        "balance": 0.0,
                        "accumulated_balance": 0.0})

        # Add month
        month = month - 1

        # Handle month < 1, year back
        if month < 1:
            year = year - 1
            month = 12

    # Return
    return timeMap[::-1]


def same_period(date1, date2):
    """ Check if date1 is same year and month than 2.
    """

    # Check year and month
    if date1.year == date2.year and date1.month == date2.month:
        return True
    else:
        return False
