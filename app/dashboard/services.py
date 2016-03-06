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
import endpoints
import models
from messages import IntGetMessage
from messages import FloatGetMessage
from messages import CashFlowGetMessage
from messages import CashFlowCollectionMessage
from app import user
from app import oauth
from protorpc import remote
from protorpc import messages
from protorpc import message_types

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


@endpoints.api(name='dashboard',
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS,
               # ANDROID_AUDIENCE argument is required for Android clients and
               # is not used by other clients
               audiences=oauth.ALLOWED_CLIENT_IDS,
               # Although you can add other scopes,
               # you must always include the email scope
               # if you use OAuth
               scopes=[endpoints.EMAIL_SCOPE])
class DashboardService(remote.Service):
    """ Service for the monitoring of indicators.
    """

    @endpoints.method(message_types.VoidMessage,
                      IntGetMessage,
                      http_method='GET',
                      name='count_customers')
    def count_customers(self, unused_request):
        """ Count how many customers there are.
        """

        count_customers = models.calculate_count_customers()

        return IntGetMessage(value=count_customers)

    @endpoints.method(message_types.VoidMessage,
                      IntGetMessage,
                      http_method='GET',
                      name='count_sales')
    def count_sales(self, unused_request):
        """ Count how many sales there are.
        """

        count_sales = models.calculate_count_sales()

        return IntGetMessage(value=count_sales)

    @endpoints.method(message_types.VoidMessage,
                      FloatGetMessage,
                      http_method='GET',
                      name='average_ticket')
    def average_ticket(self, unused_request):
        """ Calculate average ticket sale.
        """

        average_ticket = models.calculate_average_ticket()

        return FloatGetMessage(value=average_ticket)

    @endpoints.method(message_types.VoidMessage,
                      FloatGetMessage,
                      http_method='GET',
                      name='profit_margin')
    def profit_margin(self, unused_request):
        """ Calculate total profit.
        """

        profit_margin = models.calculate_profit_margin()

        return FloatGetMessage(value=profit_margin)

    @endpoints.method(message_types.VoidMessage,
                      FloatGetMessage,
                      http_method='GET',
                      name='revenue')
    def revenue(self, unused_request):
        """ Calculate revenue.
        """

        total_revenue = models.calculate_total_revenue()

        return FloatGetMessage(value=total_revenue)

    @endpoints.method(message_types.VoidMessage,
                      FloatGetMessage,
                      http_method='GET',
                      name='net_profit')
    def net_profit(self, unused_request):
        """ Calculate net profit.
        """

        net_profit = models.calculate_total_net_profit()

        return FloatGetMessage(value=net_profit)

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        count=messages.IntegerField(1, variant=messages.Variant.INT64))

    @endpoints.method(ID_RESOURCE,
                      CashFlowCollectionMessage,
                      path='{count}',
                      http_method='GET',
                      name='cash_flow')
    def cash_flow(self, request):
        """ Calculate cash flow.
        """

        cash_flow = models.cash_flow(request.count)

        items = []
        for model in cash_flow:
            items.append(
                CashFlowGetMessage(
                    period=model['period'],
                    purchases=model['purchases'],
                    sales=model['sales'],
                    balance=model['balance'],
                    accumulated_balance=model['accumulated_balance']))

        return CashFlowCollectionMessage(items=items)
