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

"""Usuário modelo e mensagem
"""

import logging
import endpoints

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types




class UserModel(ndb.Model):
	"""Usuário do serviço. Modelo para persistência
	"""

	created_date = ndb.DateTimeProperty(auto_now_add=True)



class UserMessage(messages.Message):
	"""Usuário do sistema.
	"""

	email = messages.StringField(1)
	created_date = message_types.DateTimeField(2, required=True)



def get_current_user():

	# Obter usuário logado
	current_user = endpoints.get_current_user()

	# Validar usuário
	if current_user is None:
		logging.error('Ao selecionar o usuário, o mesmo não foi informado.')
		raise endpoints.NotFoundException('Usuário não informado.')

	logging.debug('Selecionado usuário %s com sucesso!', current_user.email())

	return current_user



def user_key(email):
	"""Controi um Datastore key para o UserModel entity.
    """
	
	return ndb.Key('UserModel', email)