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
from httplib2 import Http

from google.appengine.api import users
from google.appengine.ext import ndb
from oauth2client.appengine import AppAssertionCredentials

from protorpc import remote
from protorpc import messages
from protorpc import message_types

from app.exceptions import NotFoundEntityException

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


PLUS_ME_SCOPE = 'https://www.googleapis.com/auth/plus.me'


class UserModel(ndb.Model):
    """ App user model.
    """


class UserMessage(messages.Message):

    email = messages.StringField(1)


def get_current_user():

    current_user = endpoints.get_current_user()

    if current_user is None:
        logging.error('Current user is None from email')
        raise NotFoundEntityException('user.notfound')

    logging.debug('User %s retrieved succesful!', current_user.email())

    return current_user


def get_current_user_key():
    """ Get current user Datastore key.
    """

    return user_key(get_current_user().email())


def user_key(email):
    """ Get user Datastore key by email.
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
    """ Service handles user information.
    """

    @endpoints.method(message_types.VoidMessage,
                      UserMessage,
                      http_method='GET',
                      name='get')
    def get(self, request):
        """ Get user data from current user.
        """

        return UserMessage(email=get_current_user().email())
