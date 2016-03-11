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

from app import user
from app import oauth
from messages import TrackingGetMessage
from messages import TrackingGetCollectionMessage

from protorpc import remote
from protorpc import messages
from protorpc import message_types

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


@endpoints.api(name='postal',
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS,
               # ANDROID_AUDIENCE argument is required for Android clients and
               # is not used by other clients
               audiences=oauth.ALLOWED_CLIENT_IDS,
               # Although you can add other scopes,
               # you must always include the email scope if you use OAuth.
               scopes=[endpoints.EMAIL_SCOPE])
class PostalService(remote.Service):
    """ Service for management postal service information.
    """

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        postal_service=messages.StringField(1),
        track_code=messages.StringField(2))

    @endpoints.method(ID_RESOURCE,
                      TrackingGetCollectionMessage,
                      path='{postal_service}/{track_code}',
                      http_method='GET',
                      name='get_tracking_info')
    def get_tracking_info(self, request):
        """ Get tracking information by tracking code.
        """

        tracking_info_list = models.get_tracking_info(request.track_code)

        # Transport model to message
        items = []
        for item in tracking_info_list:
            items.append(
                TrackingGetMessage(date=item.date,
                                   local=item.local,
                                   status=item.status,
                                   details=item.details))

        # Return
        return TrackingGetCollectionMessage(items=items)
