/******************************************************************************
 * customer.js
 *
 * Copyright 2016 Marcos Salomão
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @version     1.0
 * @author      Marcos Salomão (salomao.marcos@gmail.com)
 *****************************************************************************/

/**
 * Objeto global relativo aos clientes da loja.
 */
! function($) {

    /*
     * Inserindo o escopo de cliente.
     */
    $.customer = {};

    /*****************************************************************************
     * Controller API 
     *****************************************************************************/

    /**
     * Métodos relativos à API do recurso cliente.
     */
    $.customer.api = {

        /* 
         * Método destinado à pesquisar pelo nome ou código os clientes cadastrados.
         */
        search: function(_data) {

            // Criar controle promise
            var deferred = $.Deferred();

            // fn sucesso
            var success = function(response) {

                    // Executar fn sucesso pelo promise
                    deferred.resolve(response);

                } // Fim fn sucesso

            // fn error
            var error = function(reason) {

                    // apresentar mensagem ao usuário
                    $('.modal-dialog-message').modalDialog({
                        title: messages.customer.search.dialog.title,
                        message: messages.customer.search.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar fn erro pelo promise
                    resolve.reject();
                } // Fim fn error

            // Load API e executar serviço
            gapi.client.load('customer', 'v1', function() {
                var request = gapi.client.customer.search(_data);
                request.then(success, error);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();

        }, // Fim search

        /**
         *  Método persiste o cliente.
         */
        save: function(_data) {

            // atualizar barra de progresso
            $('.progress-bar-form').progress(50, messages.progressbar.waitingserver);

            // criar controle promise
            var deferred = $.Deferred();

            // fn sucesso
            var success = function(response) {

                // atualizar barra de progresso
                $('.progress-bar-form').progress(100, messages.progressbar.done);


                console.log('saved' + $.i18n.prop('messages.product.save.dialog.title'));

                // apresentar mensagem ao usuário
                $('.modal-dialog-message').modalDialog({
                    title: messages.customer.save.dialog.title,
                    message: messages.customer.save.dialog.success
                }).success();

                // resolve promise
                deferred.resolve(response);
            };

            // fn erro
            var failure = function(reason) {

                // atualizar barra de progresso
                $('.progress-bar-form').progress(100, messages.progressbar.done);

                // apresentar mensagem ao usuário
                $('.modal-dialog-message').modalDialog({
                    title: messages.customer.save.dialog.title,
                    message: messages.customer.save.dialog.errormessage
                }).danger();

                console.log(reason.result.error.message);

                // promisse
                resolve.reject();
            };

            // Load API e  executar serviço
            gapi.client.load('customer', 'v1', function() {
                var request = gapi.client.customer.save(_data);
                request.then(success, failure);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();
        }, // Fim save

        /**
         *  Método realiza a exclusão do cliente.
         */
        delete: function(_id) {

                // atualizar barra de progresso
                $('.progress-bar-table').progress(50, messages.progressbar.waitingserver);

                // Criar controle promise
                var deferred = $.Deferred();

                // fn sucesso
                var success = function(response) {

                    // atualizar barra de progresso
                    $('.progress-bar-table').progress(100, messages.progressbar.done);

                    // apresentar mensagem ao usuário
                    $('.modal-dialog-message').modalDialog({
                        title: messages.customer.delete.dialog.title,
                        message: messages.customer.delete.dialog.success
                    }).success();

                    // Executar promise
                    deferred.resolve();
                };

                // fn erro
                var failure = function(reason) {

                    // atualizar barra de progresso
                    $('.progress-bar-table').progress(100, messages.progressbar.done);

                    // apresentar mensagem ao usuário
                    $('.modal-dialog-message').modalDialog({
                        title: messages.customer.delete.dialog.title,
                        message: messages.customer.delete.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar promise
                    resolve.reject();
                };

                // Load API e  executar serviço
                gapi.client.load('customer', 'v1', function() {
                    var request = gapi.client.customer.delete({ id: _id });
                    request.then(success, failure);
                }, API_ROOT);

                // retornar promise
                return deferred.promise();
            } // Fim delete

    }; // Fim API


    /*****************************************************************************
     * View components
     *****************************************************************************/

    $.customer.view = {

        /**
         * Método destinado à criar a tabela com os clientes.
         */
        bindTable: function(_data) {

            // Construir tabela
            $('table.table-customers').bootstrapTable({
                uniqueId: 'id',
                columns: [{
                    field: 'id',
                    visible: false
                }, {
                    field: 'name',
                    title: messages.customer.name,
                    searchable: true
                }, {
                    title: '',
                    align: 'center',
                    searchable: false,
                    'class': 'col-sm-2',
                    formatter: $.common.view.tableactionbuttons,
                    events: {
                        'click button.delete': function(e, value, row, index) {
                            $.customer.api.delete(row.id).then(
                                function() {
                                    $('table.table-customers').bootstrapTable('remove', {
                                        field: 'id',
                                        values: [row.id]
                                    });
                                });
                        },
                        'click button.update': function(e, value, row, index) {

                            // Preencher form, precisa ser primeiro show tab
                            // senão não atualiza o map 
                            $('form.customer-form').populate(row);

                            // mostar tab do form
                            $('.nav-tabs a[href="#tab_2"]').tab('show');
                        }
                    }
                }],
                pageList: [15],
                data: _data.items,
                pagination: true,
                search: true,
                striped: true
            });

        }, // Fim bindTable

        /**
         * Método destinado à carregar a tabela com os clientes.
         */
        loadTable: function() {

            // atualizar barra de progresso
            $('.progress-bar-table').progress(50, messages.progressbar.waitingserver);

            // Load API e  executar serviço
            gapi.client.load('customer', 'v1', function() {
                var request = gapi.client.customer.list();
                request.then(
                    function(response) {

                        // atualizar barra de progresso
                        $('.progress-bar-table').progress(75, messages.progressbar.building);

                        // Atachar a lista de compras na tabela
                        $.customer.view.bindTable(response.result);

                        // atualizar barra de progresso					
                        $('.progress-bar-table').progress(100, messages.progressbar.done);

                    },
                    function(reason) {

                        // atualizar barra de progresso					
                        $('.progress-bar-table').progress(100, messages.progressbar.done);

                        // apresentar mensagem ao usuário
                        $('.modal-dialog-message').modalDialog({
                            title: messages.customer.list.dialog.title,
                            message: messages.customer.list.dialog.errormessage
                        }).danger();

                        console.log(reason.result.error.message);

                    });

            }, API_ROOT);

        }, // Fim loadTable


    };


}(jQuery);


/**
 * Ação ao carregar a página.
 */
! function($) {

    // Aplicar i18n
    $('span.tab_list').text(messages.customer.tab.list);
    $('span.tab_save').text(messages.customer.tab.save);
    $('h3.customer_save_title').text(messages.customer.save.title);
    $('span.new-item').text(messages.action.new_item);
    $('small.customer_save_subtitle').text(messages.customer.save.subtitle);

    $('label.name').text(messages.customer.name);
    $('input[name="name"]').attr('placeholder', messages.customer.form.name.placeholder);
    $('label.email').text(messages.customer.email);
    $('input[name="email"]').attr('placeholder', messages.customer.form.email.placeholder);
    $('label.phone').text(messages.customer.phone);
    $('input[name="phone"]').attr('placeholder', messages.customer.form.phone.placeholder);
    $('label.location').text(messages.customer.location);
    $('input[name="location"]').attr('placeholder', messages.customer.form.location.placeholder);

    $('button.save').text(messages.action.save);

    $('button.new-item').bind('click', function() {
        $('form.customer-form').trigger('reset');
    });

    // Carregar a lista de clientes
    $.customer.view.loadTable();

    // Criar a validação do formulário
    $('form.customer-form').validate({ // initialize the plugin
        rules: {
            name: {
                required: true,
                minlength: 3
            },
            email : {
                email: true
            }
        },
        messages: {
            name: messages.customer.form.name.required,
            email: messages.customer.form.email.valid
        },

        /**
         * Ação ao submeter o formulário.
         */
        submitHandler: function(form, event) {
            // não submete form
            event.preventDefault();

            // Convert form to JSON Object
            var data = $(form).serializeObject();

            // Submeter ao endpoint
            $.customer.api.save(data).then(function(_data) {

                // Zerar o form qdo houver sucesso
                $(form).trigger('reset');

                // Atualizar lista
                var row = $('table.table-customers').bootstrapTable(
                    'getRowByUniqueId', _data.result.id);

                // Insere se não existe ou atualiza caso já esteja inserida
                if (row == null) {
                    $('table.table-customers').bootstrapTable('insertRow', {
                        index: 0,
                        row: _data.result
                    });
                } else {

                    $('table.table-customers').bootstrapTable('updateByUniqueId', {
                        id: _data.result.id,
                        row: _data.result
                    });
                }

            });

        }

    }); // Fim validate


    $('.nav-tabs-custom').on('shown.bs.tab',
        function(e) {

            if ($(e.target).attr('href') != '#tab_2') return;

            $('.map-canvas').maps({
            	autocomplete : $('input[name="location"]')
            });

        });


}(jQuery);
