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
import models
import messages
from app import user
from app import oauth
from protorpc import remote
from protorpc import message_types


__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


@endpoints.api(name='marketplace',
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS,
               # ANDROID_AUDIENCE argument is required for Android clients and
               # is not used by other clients
               audiences=oauth.ALLOWED_CLIENT_IDS,
               # Although you can add other scopes,
               # you must always include the email scope if you use OAuth.
               scopes=[endpoints.EMAIL_SCOPE])
class MarketplaceService(remote.Service):
    """ Service aims to manage the user marketplaces.
    """

    @endpoints.method(message_types.VoidMessage,
                      messages.MarketplaceGetMessage,
                      http_method='GET',
                      name='get')
    def get(self, unused_request):
        """ Get current user marketplace.
        """

        marketplaceModel = models.get(user.get_current_user().email())

        return messages.MarketplaceGetMessage(
            name=marketplaceModel.name,
            created_date=marketplaceModel.created_date)

    MARKETPLACE_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(
        messages.MarketplacePostMessage)

    @endpoints.method(MARKETPLACE_MESSAGE_RESOURCE_CONTAINER,
                      messages.MarketplaceGetMessage,
                      http_method='POST',
                      name='save')
    def save(self, request):
        """ Add or update a marketplace to current user.
        """

        marketplaceModel = models.put(
            email=user.get_current_user().email(), name=request.name)

        return messages.MarketplaceGetMessage(
            name=marketplaceModel.name,
            created_date=marketplaceModel.created_date)
