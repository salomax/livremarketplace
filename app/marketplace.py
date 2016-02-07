#!/usr/bin/env python
#coding: utf-8
#
# Copyright 2016 Google Inc.
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

"""Marketplace modelo, mensagens e métodos"""

import logging

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types

import user



class MarketplaceModel(ndb.Model):
	"""Marketplace (loja) do usuário. Modelo para persistência"""

	name = ndb.StringProperty(required=True, indexed=False)
	created_date = ndb.DateTimeProperty(auto_now_add=True)



class MarketplaceGetMessage(messages.Message):
  	"""Marketplace (loja) do usuário. Mensagem a ser trafegada pelo endpoint"""

  	name = messages.StringField(1, required=True)
  	created_date = message_types.DateTimeField(2, required=True)

class MarketplacePostMessage(messages.Message):
  	"""Marketplace (loja) do usuário. Mensagem a ser trafegada pelo endpoint"""

  	name = messages.StringField(1, required=True)



def  get(email):
	"""Método retorna um marketplace para o usuário informado através do email. Caso o mesmo não exista, um novo é criado."""

	# Selecionando key do usuário
	user_key = user.user_key(email)

	# Selecionando a marketplace (loja) do usuário
	marketplaceModel = MarketplaceModel.query(ancestor=user_key).get()

	# Caso ainda não exista, uma nova marketplace (loja) é criada para o usuário
	if marketplaceModel is None:
		put(email=email, name='Nova Loja', user_key=user_key)

	logging.debug(marketplaceModel)	
		
	# Criando mensagem de retorno para o endpoint
	return marketplaceModel



def  put(email, name, user_key=None):
	"""Método atualiza um marketplace para o usuário informado através do email."""

	# Selecionando key do usuário
	if user_key is None:
		user_key = user.user_key(email)

	logging.debug('Criando/atualizando marketplace (loja) para o usuário %s', email)

	# Selecionando a marketplace (loja) do usuário
	marketplaceModel = MarketplaceModel.query(ancestor=user_key).get()

	# Caso exista, obter o atual
	if marketplaceModel is None:
		marketplaceModel = MarketplaceModel(parent=user_key)
	
	# Atualizar o nome
	marketplaceModel.name = name

	logging.debug('Persistindo no Datastore...', email)

	# Persistir a entity
	marketplaceModel.put()

	logging.debug('Persistido com sucesso!')	

	# Retornando marketplace (loja) persistida
	return marketplaceModel