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


class CustomerKeyMessage(messages.Message):
    """ Endpoint message to customer key.
    """

    # Id
    id = messages.IntegerField(1)


class CustomerGetMessage(messages.Message):
    """ Endpoint messageto get a customer.
    """

    # Id
    id = messages.IntegerField(1)

    # Name
    name = messages.StringField(2, required=True)

    # Email
    email = messages.StringField(3, required=False)

    # Phone
    phone = messages.StringField(4, required=False)

    # Location
    location = messages.StringField(5, required=False)

    # Insert date
    created_date = message_types.DateTimeField(6, required=True)


class CustomerPostMessage(messages.Message):
    """ Endpoint message to post a customer.
    """

    # Id
    id = messages.IntegerField(1)

    # Name
    name = messages.StringField(2, required=True)

    # Email
    email = messages.StringField(3, required=False)

    # Phone
    phone = messages.StringField(4, required=False)

    # Location
    location = messages.StringField(5, required=False)


class CustomerSearchMessage(messages.Message):
    """ Endpoint message to search a customer by name.
    """

    # Name
    name = messages.StringField(1)


class CustomerCollectionMessage(messages.Message):
    """ Endpoint message to get a customers collection.
    """

    # Collection
    items = messages.MessageField(CustomerGetMessage, 1, repeated=True)
