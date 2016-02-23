#!/usr/bin/env python
#coding: utf-8
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
#
__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"

import logging
import datetime

from app import user
from app import util
from app.marketplace import models as marketplace
from app.sale import models as salesModel
from app.customer import models as customersModel

from google.appengine.ext import ndb
from google.appengine.api import search as search_api

from app.purchase import models as purchase


def calculate_count_customers():
	"""Retornar a quantidade total de clientes.
	"""

	return customersModel.get_customer_query().count()


def calculate_count_sales():
	"""Retornar a quantidade total de vendas.
	"""

	return salesModel.get_sales_query().count()


def calculate_profit_margin():
	"""Calcula o valor médio da margem de lucro
	"""

	revenue = calculate_total_revenue()
	net_profit = calculate_total_net_profit()

	return net_profit / revenue


def calculate_total_revenue():
	"""Calcula o faturamento total.
	"""

	sales = salesModel.list()

	total_revenue = 0
	for sale in sales:
		total_revenue = total_revenue + sale.amount

	return total_revenue


def calculate_total_net_profit():
	"""Calcula o lucro líquido total.
	"""

	sales = salesModel.list()

	total_net_profit = 0
	for sale in sales:
		total_net_profit = total_net_profit + sale.net_total

	return total_net_profit


def cash_flow():
	"""Obtêm os totais de compra e venda mensal do último ano.
	"""

	logging.debug("Carregando as compras")

	#Identificando usuário da requisição
	email = user.get_current_user().email()

	logging.debug("Obtendo a entidade da loja para o usuario %s", email)

	#Obtendo marketplace como parent
	marketplaceModel = marketplace.get(email)

	#Realizando query, listando as compras
	queryPurchases = purchase.PurchaseModel.query(ancestor=marketplaceModel.key)

	# Criando map dos últimos 12 meses
	list = list_monthly(12)
	
	last_year = datetime.datetime.now()
	last_year = last_year.replace(year = last_year.year - 1)

	purchases = queryPurchases.filter(
		purchase.PurchaseModel.purchase_date > last_year).order(
		-purchase.PurchaseModel.purchase_date).fetch(
		projection=[purchase.PurchaseModel.total_cost, purchase.PurchaseModel.payment_date])



	#Retornando
	return      [{"period": datetime.datetime.now(), "purchases": 3407.0, "sales": 3660.0},
       			{"period": datetime.datetime.now(), "purchases": 3351.0, "sales": 3629.0},
       			{"period": datetime.datetime.now(), "purchases": 3269.0, "sales": 2618.0}]

def list_monthly(n):
	"""Criando lista dos últimos "n" meses.
	"""

	now = datetime.datetime.now()
	timeMap = []
	year = now.year
	month = now.month
	for x in range(12):
		timeMap.append(datetime.date(year, month, 1))
		month = month - 1
		if month < 1:
			year = year - 1
			month = 12

	return timeMap
