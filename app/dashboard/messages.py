#!/usr/bin/env python
#coding: utf-8
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
#
__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


from protorpc import messages
from protorpc import message_types

class IntGetMessage(messages.Message):
  	"""Mensagem GET a ser trafegada pelo endpoint representando um valor do tipo ponto flutuante."""

	# Valor 
	value = messages.IntegerField(1, required=True)


class FloatGetMessage(messages.Message):
  	"""Mensagem GET a ser trafegada pelo endpoint representando um valor do tipo ponto flutuante."""

	# Valor 
	value = messages.FloatField(1, required=True)


class CashFlowGetMessage(messages.Message):
  	"""Mensagem GET a ser trafegada pelo endpoint representando o fluxo de caixa"""

	# período
	period = message_types.DateTimeField(1, required=True)

	# compras
	purchases = messages.FloatField(2, required=False)

	# vendas
	sales = messages.FloatField(3, required=False)


class CashFlowCollectionMessage(messages.Message):
	"""Coleção de fluxo de caixa."""

	items = messages.MessageField(CashFlowGetMessage, 1, repeated=True)