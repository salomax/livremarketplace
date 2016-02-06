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

""" Usuário modelo e mensagem """

from datetime import datetime
from protorpc import messages
from protorpc import message_types

class UserMessage(messages.Message):
  """Usuário do sistema."""

  user_id = messages.IntegerField(2, required=True)
  email = messages.StringField(1)
  date_created = message_types.DateTimeField(3, required=True)
