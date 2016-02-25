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

from google.appengine.ext import ndb
from google.appengine.api import search as search_api

# Index autocomplete produto
SUPPLIER_AUTOCOMPLETE_INDEX_NAME = 'suplier_autocomplete_index'
AUTOCOMPLETE_SEARCH_LIMIT = 5
def get_autocomplete_index():
	return search_api.Index(name=SUPPLIER_AUTOCOMPLETE_INDEX_NAME)

class SupplierModel(ndb.Model):
	"""Entidade representa um fornecedor da loja"""

	# Nome do fornecedor
	name = ndb.StringProperty(required=True)

	# Email de contato do fornecedor
	email = ndb.StringProperty(required=False)

	# Telefone de contato do fornecedor
	phone = ndb.StringProperty(required=False)

	# Localização
	location = ndb.StringProperty(required=False)

	#Data criação	
	created_date = ndb.DateTimeProperty(auto_now_add=True)

#http://stackoverflow.com/questions/12899083/partial-matching-gae-search-api
def update_index(supplier):
	name = ','.join(util.tokenize_autocomplete(supplier.name))
	document = search_api.Document(
		doc_id=str(supplier.key.id()),
		fields=[search_api.TextField(name='name', value=name)])
	get_autocomplete_index().put(document)


def remove_index(_id):
	get_autocomplete_index().remove(str(_id))


def get(id):
	"""Selecionar um fornecedor cadastrado pelo id.
	"""

	#Obtendo marketplace como parent
	marketplaceModel = marketplace.get_marketplace()

	logging.debug("Loja encontrada com sucesso")

	#Realizando query, selecionando o fornecedor pelo pai e id
	supplier = ndb.Key('SupplierModel', int(id), parent=marketplaceModel.key).get() 

	if supplier is None:
		raise IndexError("Fornecedor não encontrado!")

	logging.debug("Fornecedor encontrado com sucesso")

	return supplier


def list():
	"""Listar os fornecedores cadastrados na loja do usuário.
	"""

	logging.debug("Listando os fornecedores cadastrados")

	#Obtendo marketplace como parent
	marketplaceModel = marketplace.get_marketplace()

	#Realizando query, listando os fornecedores
	suppliers = SupplierModel.query(ancestor=marketplaceModel.key).order(
		SupplierModel.name).fetch()

	logging.debug("Foram selecionado(s) %d fornecedores(s) cadastrados", 
		len(suppliers))

	#Retornando
	return suppliers


def search(supplier):
	"""Pesquisa dos fornecedores cadastrados na loja.
	"""

	# Listando os fornecedores cadastrados	
	items = list()

	logging.debug("Realizando a pesquisa indexada de fornecedores")

	# Realizando a pesquisa
	search_results = get_autocomplete_index().search(search_api.Query(
			query_string="name:{name}".format(name=supplier.name),
			options=search_api.QueryOptions(limit=AUTOCOMPLETE_SEARCH_LIMIT)))

	# Convertendo docs para model
	results = []
	for doc in search_results:
		results.append(get(int(doc.doc_id)))

	# Retornando resultado
	return results

@ndb.transactional
def save(supplier):
	"""Inclui ou atualiza um fornecedor.
	"""

	logging.debug("Persistindo um fornecedor na loja")

	#Obtendo marketplace como parent
	marketplaceModel = marketplace.get_marketplace()

	logging.debug("Loja encontrada com sucesso")

	logging.debug("Criando model para o fornecedor ou selecionando o existente para atualizá-lo")

	if supplier.id is not None:
		supplierModel = ndb.Key('SupplierModel', int(supplier.id), 
			parent=marketplaceModel.key).get() 
	else:
		supplierModel = SupplierModel(parent=marketplaceModel.key)

	#Criando model
	supplierModel.name = supplier.name
	supplierModel.email = supplier.email
	supplierModel.phone = supplier.phone
	supplierModel.location = supplier.location

	#Persistindo fornecedor
	logging.debug("Persistindo fornecedor...")

	supplierModel.put()

	logging.debug("Persistido fornecedor %d com sucesso na loja %s", 
		supplierModel.key.id(), marketplaceModel.name)

	#Atualizando índice
	update_index(supplierModel)
	logging.debug("Índice atualizado com sucesso para o fornecedor %s", 
		supplierModel.key.id())

	#Retornando fornecedor cadastrado com o id
	return supplierModel


@ndb.transactional
def delete(id):
	"""Remove um fornecedor cadastrado.
	"""

	logging.debug("Removendo o fornecedor %d persistido na loja", id)

	#Obtendo marketplace como parent
	marketplaceModel = marketplace.get_marketplace()

	logging.debug("Loja encontrada com sucesso")

	#Realizando query, selecionando o fornecedor pelo pai e id
	supplier = ndb.Key('SupplierModel', int(id), parent=marketplaceModel.key).get() 

	if supplier is None:
		raise IndexError("Fornecedor não encontrado!")

	logging.debug("Fornecedor encontrado com sucesso")

	supplier.key.delete()

	logging.debug("Fornecedor removido com sucesso")