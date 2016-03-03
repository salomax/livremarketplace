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


class SupplierKeyMessage(messages.Message):
    """Mensagem GET do Fornecedor a ser trafegada pelo endpoint.
    """

    # Id
    id = messages.IntegerField(1)


class SupplierGetMessage(messages.Message):
    """ Get message.
    """

    id = messages.IntegerField(1)

    name = messages.StringField(2, required=True)

    email = messages.StringField(3, required=False)

    phone = messages.StringField(4, required=False)

    location = messages.StringField(5, required=False)

    created_date = message_types.DateTimeField(6, required=True)


class SupplierPostMessage(messages.Message):
    """ POST message.
    """

    id = messages.IntegerField(1)

    name = messages.StringField(2, required=True)

    email = messages.StringField(3, required=False)

    phone = messages.StringField(4, required=False)

    location = messages.StringField(5, required=False)


class SupplierSearchMessage(messages.Message):
    """ Message to search.
    """

    name = messages.StringField(2, required=True)


class SupplierCollectionMessage(messages.Message):
    """ Supplier collections.
    """

    items = messages.MessageField(SupplierGetMessage, 1, repeated=True)
