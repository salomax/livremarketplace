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
from app.marketplace import models as marketplace

from google.appengine.ext import ndb


class ProductModel(ndb.Model):
	"""Entidade representa um produto comercializado pela loja"""

	#Código de referência do Produto	
	code = ndb.StringProperty(required=False)

	#Nome do Produto	
	name = ndb.StringProperty(required=True)

	#Data criação	
	created_date = ndb.DateTimeProperty(auto_now_add=True)

def list():
	"""Listar os produtos cadastrados na loja do usuário.
	"""

	logging.debug("Listando os produtos cadastrados")

	#Identificando usuário da requisição
	email = user.get_current_user().email()

	logging.debug("Obtendo a entidade da loja para o usuario %s", email)

	#Obtendo marketplace como parent
	marketplaceModel = marketplace.get(email)

	#Realizando query, listando os produtos
	products = ProductModel.query(ancestor=marketplaceModel.key).order(
		ProductModel.name).fetch()

	logging.debug("Foram selecionado(s) %d produtos(s) cadastrados na loja do usuário %s", 
		len(products), email)

	#Retornando
	return products


def put(product):
	"""Inclui ou atualiza um produto.
	"""

	logging.debug("Persistindo um produto na loja")

	#Identificando usuário da requisição
	email = user.get_current_user().email()

	logging.debug("Obtendo a entidade da loja para o usuario %s", email)

	#Obtendo marketplace como parent
	marketplaceModel = marketplace.get(email)

	logging.debug("Loja encontrada com sucesso")

	logging.debug("Criando model para o produto ou selecionando o existente para atualizá-lo")

	if product.id is not None:
		productModel = ndb.Key('ProductModel', int(product.id), 
			parent=marketplaceModel.key).get() 
	else:
		productModel = ProductModel(parent=marketplaceModel.key)

	#Criando model
	productModel.code = product.code
	productModel.name = product.name

	logging.debug("Persistindo produto...")

	#Persistindo
	productModel.put()

	logging.debug("Persistido produto %d com sucesso na loja %s", 
		productModel.key.id(), marketplaceModel.name)

	return productModel

def delete(id):
	"""Remove um produto cadastrado.
	"""

	logging.debug("Removendo o produto %d persistido na loja", id)

	#Identificando usuário da requisição
	email = user.get_current_user().email()

	logging.debug("Obtendo a entidade da loja para o usuario %s", email)

	#Obtendo marketplace como parent
	marketplaceModel = marketplace.get(email)

	logging.debug("Loja encontrada com sucesso")

	#Realizando query, selecionando o produto pelo pai e id
	product = ndb.Key('ProductModel', int(id), parent=marketplaceModel.key).get() 

	if product is None:
		raise IndexError("Produto não encontrado!")

	logging.debug("Produto encontrado com sucesso")

	product.key.delete()

	logging.debug("Produto removido com sucesso")