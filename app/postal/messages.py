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


from protorpc import messages
from protorpc import message_types

__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


class TrackingGetMessage(messages.Message):
    """ Tracking package information GET endpoint message.
    """

    date = messages.StringField(1, required=True)
    local = messages.StringField(2, required=True)
    status = messages.StringField(3, required=True)
    details = messages.StringField(4, required=True)

class TrackingGetCollectionMessage(messages.Message):
    """ Endpoint message to TrackingGetMessage collection.
    """

    # Collection
    items = messages.MessageField(TrackingGetMessage, 1, repeated=True)