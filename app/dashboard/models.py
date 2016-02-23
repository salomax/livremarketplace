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
import dateutil.relativedelta

from app import user
from app import util
from app.marketplace import models as marketplace
from app.sale import models as salesModel
from app.customer import models as customersModel
from app.purchase import models as purchasesModel

from google.appengine.ext import ndb
from google.appengine.api import search as search_api


def calculate_average_ticket():

	sales = salesModel.list()

	total_revenue = 0
	count = 0
	for sale in sales:
		total_revenue = total_revenue + sale.amount
		count = count + 1

	return total_revenue / count	


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


def cash_flow(n):
	"""Obtêm os totais de compra e venda mensal dos últimos 'n' meses.
	"""
	# Criando dict para os últimos 'n' meses
	list = list_monthly(n)
	
	# Obtendo a data mínima para filtro na query
	date = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=n)

	# Obter a query das compras
	queryPurchases = purchasesModel.get_query_purchase()

	#Realizando query, listando as compras
	purchases = queryPurchases.filter(
		purchasesModel.PurchaseModel.purchase_date > date).fetch(
		projection=[purchasesModel.PurchaseModel.total_cost, purchasesModel.PurchaseModel.payment_date])

	# Realizando o agrupamento com somatória
	for purchase in purchases:
		for i in list:
			if same_period(purchase.payment_date, i['period']):
				i['purchases'] = i['purchases'] + purchase.total_cost


	#Obtendo query das vendas
	salesQuery = salesModel.get_sales_query()

	#Realizando query, listando as vendas
	sales = salesQuery.filter(
		salesModel.SaleModel.sale_date > date).fetch(
		projection=[salesModel.SaleModel.amount, salesModel.SaleModel.sale_date])

	# Realizando o agrupamento com somatória
	for sale in sales:
		for i in list:
			if same_period(sale.sale_date, i['period']):
				i['sales'] = i['sales'] + sale.amount

	#Retornando
	return list

def list_monthly(n):
	"""Criando lista dos últimos "n" meses.
	"""

	now = datetime.datetime.now()
	timeMap = []
	year = now.year
	month = now.month
	for x in range(n):
		timeMap.append({"period" : datetime.datetime(year, month, 1), "purchases": 0.0, "sales": 0.0})
		month = month - 1
		if month < 1:
			year = year - 1
			month = 12

	return timeMap

def same_period(date1, date2):
	""" Verifica se é o mesmo período (ano e mês)
	""" 

	if date1.year == date2.year and date1.month == date2.month:
		return True
	else:
		return False
