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
from app import user
from google.appengine.ext import ndb

from google.appengine.api import memcache

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


class MarketplaceModel(ndb.Model):
    """Entidade marketplace (loja) do usuário"""

    name = ndb.StringProperty(required=True, indexed=False)
    created_date = ndb.DateTimeProperty(auto_now_add=True)


def get_marketplace():
    """ Get active user marketplace.
    """

    # Identificando usuário da requisição
    email = user.get_current_user().email()

    # Return user active marketplace by email
    return get(email)


def get(email):
    """Método retorna um marketplace para o usuário informado através do email.
       Caso o mesmo não exista, um novo é criado.
    """

    # Set memcache key
    memcache_key = 'email.marktplace.%s' % email

    # Verify if user marktplace is cached
    marketplace_cached = memcache.get(memcache_key)

    # and return cached marketplace
    if marketplace_cached is not None:
        logging.debug("Marketplace cached for %s user. Return it.", email)
        return marketplace_cached

    # else, query or add new one...

    # Create user key as parent
    user_key = user.user_key(email)

    # Select user marketplace
    marketplaceModel = MarketplaceModel.query(ancestor=user_key).get()

    # If not present, create new one
    if marketplaceModel is None:
        marketplaceModel = put(email=email, name='Nova Loja', user_key=user_key)
        logging.debug("Marketplace create sucessfully for %s user", email)

    # Add to memcache
    memcache.add(key=memcache_key, value=marketplaceModel, time=3600 * 24)

    logging.debug("Marketplace cached for %s user", email)

    # Return marketplace
    return marketplaceModel


def put(email, name, user_key=None):
    """Método atualiza um marketplace para o usuário informado através do email.
    """

    # Selecionando key do usuário
    if user_key is None:
        user_key = user.user_key(email)

    logging.debug(
        'Criando/atualizando marketplace (loja) para o usuário %s', email)

    # Selecionando a marketplace (loja) do usuário
    marketplaceModel = MarketplaceModel.query(ancestor=user_key).get()

    # Caso exista, obter o atual
    if marketplaceModel is None:
        marketplaceModel = MarketplaceModel(parent=user_key)

    # Atualizar o nome
    marketplaceModel.name = name

    logging.debug('Persistindo no Datastore...')

    # Persistir a entity
    marketplaceModel.put()

    logging.debug('Persistido com sucesso!')

    # Retornando marketplace (loja) persistida
    return marketplaceModel
