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

"""Purchase (compras) modelo, mensagens e métodos
"""

import logging
import datetime

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types

import user



class PurchasePostMessage(messages.Message):
  	"""Purchase (compra) de produto no estoque. Mensagem a ser trafegada pelo endpoint
  	"""

  	name = messages.StringField(1)
  	quantity = messages.IntegerField(2, required=True)


class PurchaseGetMessage(messages.Message):
  	"""Purchase (compra) de produto no estoque. Mensagem a ser trafegada pelo endpoint
  	"""

  	name = messages.StringField(1)
  	quantity = messages.IntegerField(2, required=True)
  	create_date = message_types.DateTimeField(3, required=True)


class PurchaseCollectionGetMessage(messages.Message):
  	"""Lista de Purchases (compras) de produto no estoque. Mensagem a ser trafegada pelo endpoint
  	"""

  	items = messages.MessageField(PurchaseGetMessage, 1, repeated=True)



def get_purchases():
	"""Retorna Purchases (compras) já cadastradas pelo usuário no Datastore.
	"""
	
	return PurchaseCollectionGetMessage(items=[PurchaseGetMessage(name='teste', quantity=1, create_date=datetime.now())])