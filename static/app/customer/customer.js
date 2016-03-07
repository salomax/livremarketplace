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

        SERVICE_NAME : 'customer',
        VERSION : 'v1',

        service : function(method) {
            return ['/', $.customer.api.SERVICE_NAME, '/', $.customer.api.VERSION, '/', method].join(''); 
        },

        /* 
         * Método destinado à pesquisar pelo nome ou código os clientes cadastrados.
         */
        search: function(_data) {

            // Execute customers delete endpoint 
            return $.api.request({
                path : $.customer.api.service('search'),
                method : 'POST',
                body : _data,
                dialogError : {
                    title: messages.customer.search.dialog.title,
                    message: messages.customer.search.dialog.errormessage
                }
            });            

        }, // Fim search

        /**
         *  Método persiste o cliente.
         */
        save: function(_data) {

            // Execute custumers delete endpoint 
            return $.api.request({
                path : $.customer.api.service('save'),
                method : 'POST',
                body : _data,
                progressBar : $('.progress-bar-form'),
                dialogSuccess : {
                    title: messages.customer.save.dialog.title,
                    message: messages.customer.save.dialog.success
                },
                dialogError : {
                    title : messages.customer.save.dialog.title,
                    message : messages.customer.save.dialog.errormessage
                }
            }).then(function(response) {
                $('form.customer-form').populate(response.result);
                return response;
            });

        }, // Fim save

        /**
         *  Método realiza a exclusão do cliente.
         */
        delete: function(_id) {

            // Execute custumers delete endpoint 
            return $.api.request({
                path : $.customer.api.service(_id),
                method : 'DELETE',
                progressBar : $('.progress-bar-table'),
                dialogSuccess : {
                    title: messages.customer.delete.dialog.title,
                    message: messages.customer.delete.dialog.success
                },
                dialogError : {
                    title : messages.customer.delete.dialog.title,
                    message : messages.customer.delete.dialog.errormessage
                }
            });

        }, // Fim delete

        list : function(options) {
            return $.api.request($.util.mergeObjects({
                path : $.customer.api.service('list')
            }, options));    
        }

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
                // striped: true
            });

            $('table').fadeIn();

        }, // Fim bindTable

        /**
         * Método destinado à carregar a tabela com os clientes.
         */
        loadTable: function() {

            $('table').fadeOut();            

            // Execute custumers list endpoint 
            var request = $.customer.api.list({
                progressBar : $('.progress-bar-table'),
                dialogError : {
                    title : messages.customer.list.dialog.title,
                    message : messages.customer.list.dialog.errormessage
                }
            }).then(
                function(response) {

                    // Create table with response result
                    $.customer.view.bindTable(response.result);

                });

        }, // Fim loadTable

        /**
         * Load page event.
         */
        loadPage : function() {

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

        } // Fim load page

    }; // Fim $.customer.view

}(jQuery);
