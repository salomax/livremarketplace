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


from protorpc import messages
from protorpc import message_types

class CustomerKeyMessage(messages.Message):
  	"""Cliente da loja. Mensagem GET a ser trafegada pelo endpoint"""

  	#Id
  	id = messages.IntegerField(1)


class CustomerGetMessage(messages.Message):
  	"""Cliente da loja. Mensagem GET a ser trafegada pelo endpoint"""

  	#Id
  	id = messages.IntegerField(1)

	#Nome 
	name = messages.StringField(2, required=True)

	# Email de contato do cliente
	email = messages.StringField(3, required=False)

	# Telefone de contato do cliente
	phone = messages.StringField(4, required=False)

	# Localização
	location = messages.StringField(5, required=False)

	#Data criação
  	created_date = message_types.DateTimeField(6, required=True)


class CustomerPostMessage(messages.Message):
  	"""Cliente da loja. Mensagem POST a ser trafegada pelo endpoint"""
 
  	#Id
  	id = messages.IntegerField(1)

	#Nome 
	name = messages.StringField(2, required=True)

	# Email de contato do cliente
	email = messages.StringField(3, required=False)

	# Telefone de contato do cliente
	phone = messages.StringField(4, required=False)

	# Localização
	location = messages.StringField(5, required=False)


class CustomerSearchMessage(messages.Message):
  	"""Cliente da loja. Mensagem POST de pesquisa a ser trafegada pelo endpoint"""
 
	#Nome 
	name = messages.StringField(2, required=True)


class CustomerCollectionMessage(messages.Message):
	"""Coleção de clientes."""

	items = messages.MessageField(CustomerGetMessage, 1, repeated=True)