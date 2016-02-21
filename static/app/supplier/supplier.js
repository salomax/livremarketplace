/******************************************************************************
 * supplier.js
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
 * Objeto global relativo aos fornecedores da loja.
 */
! function($) {

    /*
     * Inserindo o escopo de fornecedor.
     */
    $.supplier = {};

    /*****************************************************************************
     * Controller API REST 
     *****************************************************************************/

    /**
     * Métodos relativos à API REST do recurso fornecedor.
     */
    $.supplier.api = {

        /* 
         * Método destinado à pesquisar pelo nome ou código os fornecedors cadastrados.
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
                        title: messages.supplier.search.dialog.title,
                        message: messages.supplier.search.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar fn erro pelo promise
                    resolve.reject();
                } // Fim fn error

            // Load API e executar serviço
            gapi.client.load('supplier', 'v1', function() {
                var request = gapi.client.supplier.search(_data);
                request.then(success, error);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();

        }, // Fim search

        /**
         *  Método persiste o fornecedor.
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
                    title: messages.supplier.save.dialog.title,
                    message: messages.supplier.save.dialog.success
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
                    title: messages.supplier.save.dialog.title,
                    message: messages.supplier.save.dialog.errormessage
                }).danger();

                console.log(reason.result.error.message);

                // promisse
                resolve.reject();
            };

            // Load API e  executar serviço
            gapi.client.load('supplier', 'v1', function() {
                var request = gapi.client.supplier.save(_data);
                request.then(success, failure);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();
        }, // Fim save

        /**
         *  Método realiza a exclusão do fornecedor.
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
                        title: messages.supplier.delete.dialog.title,
                        message: messages.supplier.delete.dialog.success
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
                        title: messages.supplier.delete.dialog.title,
                        message: messages.supplier.delete.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar promise
                    resolve.reject();
                };

                // Load API e  executar serviço
                gapi.client.load('supplier', 'v1', function() {
                    var request = gapi.client.supplier.delete({ id: _id });
                    request.then(success, failure);
                }, API_ROOT);

                // retornar promise
                return deferred.promise();
            } // Fim delete

    }; // Fim API


    /*****************************************************************************
     * View components
     *****************************************************************************/

    $.supplier.view = {

        /**
         * Método destinado à criar a tabela com os fornecedors.
         */
        bindTable: function(_data) {

            // Construir tabela
            $('table.table-suppliers').bootstrapTable({
                uniqueId: 'id',
                columns: [{
                    field: 'id',
                    visible: false
                }, {
                    field: 'name',
                    title: messages.supplier.name,
                    searchable: true
                }, {
                    title: '',
                    align: 'center',
                    searchable: false,
                    'class': 'col-sm-2',
                    formatter: $.common.view.tableactionbuttons,
                    events: {
                        'click button.delete': function(e, value, row, index) {
                            $.supplier.api.delete(row.id).then(
                                function() {
                                    $('table.table-suppliers').bootstrapTable('remove', {
                                        field: 'id',
                                        values: [row.id]
                                    });
                                });
                        },
                        'click button.update': function(e, value, row, index) {

                            // mostar tab do form
                            $('.nav-tabs a[href="#tab_2"]').tab('show');

                            // Preencher form
                            $('form.supplier-form').populate(row);
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
         * Método destinado à carregar a tabela com os fornecedors.
         */
        loadTable: function() {

            // atualizar barra de progresso
            $('.progress-bar-table').progress(50, messages.progressbar.waitingserver);

            // Load API e  executar serviço
            gapi.client.load('supplier', 'v1', function() {
                var request = gapi.client.supplier.list();
                request.then(
                    function(response) {

                        // atualizar barra de progresso
                        $('.progress-bar-table').progress(75, messages.progressbar.building);

                        // Atachar a lista de compras na tabela
                        $.supplier.view.bindTable(response.result);

                        // atualizar barra de progresso					
                        $('.progress-bar-table').progress(100, messages.progressbar.done);

                    },
                    function(reason) {

                        // atualizar barra de progresso					
                        $('.progress-bar-table').progress(100, messages.progressbar.done);

                        // apresentar mensagem ao usuário
                        $('.modal-dialog-message').modalDialog({
                            title: messages.supplier.list.dialog.title,
                            message: messages.supplier.list.dialog.errormessage
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
    $('span.tab_list').text(messages.supplier.tab.list);
    $('span.tab_save').text(messages.supplier.tab.save);
    $('h3.supplier_save_title').text(messages.supplier.save.title);
    $('small.supplier_save_subtitle').text(messages.supplier.save.subtitle);

    $('label.name').text(messages.supplier.name);
    $('input[name="name"]').attr('placeholder', messages.supplier.form.name.placeholder);
    $('label.email').text(messages.supplier.email);
    $('input[name="email"]').attr('placeholder', messages.supplier.form.email.placeholder);
    $('label.phone').text(messages.supplier.phone);
    $('input[name="phone"]').attr('placeholder', messages.supplier.form.phone.placeholder);
    $('label.location').text(messages.supplier.location);
    $('input[name="location"]').attr('placeholder', messages.supplier.form.location.placeholder);

    $('button.save').text(messages.action.save);

    // Carregar a lista de fornecedors
    $.supplier.view.loadTable();

    // Criar a validação do formulário
    $('form.supplier-form').validate({ // initialize the plugin
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
            name: messages.supplier.form.name.required,
            email: messages.supplier.form.email.valid
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
            $.supplier.api.save(data).then(function(_data) {

                // Zerar o form qdo houver sucesso
                $(form).trigger('reset');

                // Atualizar lista
                var row = $('table.table-suppliers').bootstrapTable(
                    'getRowByUniqueId', _data.result.id);

                // Insere se não existe ou atualiza caso já esteja inserida
                if (row == null) {
                    $('table.table-suppliers').bootstrapTable('insertRow', {
                        index: 0,
                        row: _data.result
                    });
                } else {

                    $('table.table-suppliers').bootstrapTable('updateByUniqueId', {
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
