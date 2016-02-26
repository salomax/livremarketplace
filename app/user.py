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
import oauth
from google.appengine.api import users
from google.appengine.ext import ndb
from protorpc import remote
from protorpc import messages
from protorpc import message_types
from oauth2client.appengine import AppAssertionCredentials
from httplib2 import Http


__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


PLUS_ME_SCOPE = 'https://www.googleapis.com/auth/plus.me'


class UserModel(ndb.Model):
    """Usuário do sistema (model).
    """


class UserMessage(messages.Message):
    """Usuário do sistema (message).
    """
    email = messages.StringField(1)


def get_current_user():

    # Obter usuário logado
    current_user = endpoints.get_current_user()

    # Validar usuário
    if current_user is None:
        logging.error('Ao selecionar o usuário, o mesmo não foi informado.')
        raise endpoints.NotFoundException('Usuário não informado.')

    logging.debug('Selecionado usuário %s com sucesso!', current_user.email())

    return current_user


def get_current_user_key():
    """Controi um Datastore key para o UserModel entity a partir do usuário atual.
"""

    return user_key(get_current_user().email())


def user_key(email):
    """Controi um Datastore key para o UserModel entity a partir do email.
"""

    return ndb.Key('UserModel', email)


@endpoints.api(name='user',
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS,
               # ANDROID_AUDIENCE argument is required for Android clients and
               # is not used by other clients
               audiences=oauth.ALLOWED_CLIENT_IDS,
               # Although you can add other scopes, you must always include the
               # email scope if you use OAuth.
               scopes=[endpoints.EMAIL_SCOPE, PLUS_ME_SCOPE])
class UserService(remote.Service):
    """Serviço destinado à obter os dados do usuário.
    """

    @endpoints.method(message_types.VoidMessage,
                      UserMessage,
                      http_method='GET',
                      name='get')
    def get(self, request):

        return UserMessage(email=get_current_user().email())
