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
from messages import SupplierPostMessage
from messages import SupplierGetMessage
from messages import SupplierCollectionMessage
from messages import SupplierSearchMessage
from app import user
from app import oauth
from protorpc import remote
from protorpc import messages
from protorpc import message_types


__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"


@endpoints.api(name='supplier',
               version='v1',
               allowed_client_ids=oauth.ALLOWED_CLIENT_IDS,
               # ANDROID_AUDIENCE argument is required for Android clients and
               # is not used by other clients
               audiences=oauth.ALLOWED_CLIENT_IDS,
               # Although you can add other scopes, you must always include the
               # email scope if you use OAuth.
               scopes=[endpoints.EMAIL_SCOPE])
class SupplierService(remote.Service):
    """Serviço destinado ao gerenciamento dos fornecedores da loja.
    """

    # Resource Container para POSTs
    Supplier_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(
        SupplierPostMessage)
    Supplier_Search_MESSAGE_RESOURCE_CONTAINER = endpoints.ResourceContainer(
        SupplierSearchMessage)

    @endpoints.method(message_types.VoidMessage,
                      SupplierCollectionMessage,
                      http_method='GET',
                      name='list')
    def list(self, unused_request):
        """Retornar a lista de fornecedores cadastrados.
        """

        logging.debug(
            'Executando endpoint para obter a lista de fornecedores')

        # Obter a lista de fornecedores cadastrados
        suppliers = models.list()

        # Declarando lista e convertendo model para message
        items = []
        for supplierModel in suppliers:
            items.append(
                SupplierGetMessage(
                    id=supplierModel.key.id(),
                    name=supplierModel.name,
                    email=supplierModel.email,
                    phone=supplierModel.phone,
                    location=supplierModel.location,
                    created_date=supplierModel.created_date))

        # Retornando fornecedores
        return SupplierCollectionMessage(items=items)

    @endpoints.method(Supplier_Search_MESSAGE_RESOURCE_CONTAINER,
                      SupplierCollectionMessage,
                      http_method='POST',
                      name='search')
    def search(self, request):
        """Realiza uma pesquisa dos fornecedores cadastrados.
        """
        logging.debug('Executando endpoint de pesquisa de fornecedores')

        # Obter a lista de fornecedores cadastrados
        suppliers = models.search(request)

        # Declarando lista e convertendo model para message
        items = []
        for supplierModel in suppliers:
            items.append(
                SupplierGetMessage(
                    id=supplierModel.key.id(),
                    name=supplierModel.name,
                    email=supplierModel.email,
                    phone=supplierModel.phone,
                    location=supplierModel.location,
                    created_date=supplierModel.created_date))

        # Retornando fornecedores
        return SupplierCollectionMessage(items=items)

    @endpoints.method(Supplier_MESSAGE_RESOURCE_CONTAINER,
                      SupplierGetMessage,
                      http_method='POST',
                      name='save')
    def save(self, request):
        """Inclui ou atualiza um fornecedor.
        """

        logging.debug(
            'Executando endpoint para incluir/atualizar um fornecedor')

        # Cadastrar/atualizar a compra de um fornecedor
        supplierModel = models.save(request)

        # Retornando compra persistida
        return SupplierGetMessage(
            id=supplierModel.key.id(),
            name=supplierModel.name,
            email=supplierModel.email,
            phone=supplierModel.phone,
            location=supplierModel.location,
            created_date=supplierModel.created_date)

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE,
                      message_types.VoidMessage,
                      path='{id}',
                      http_method='DELETE',
                      name='delete')
    def delete(self, request):
        """Remove um fornecedor cadastrado.
        """

        # Removendo Supplier
        models.delete(request.id)

        return message_types.VoidMessage()
