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
     * Controller API 
     *****************************************************************************/

    /**
     * Métodos relativos à API do recurso fornecedor.
     */
    $.supplier.api = {


        SERVICE_NAME : 'supplier',
        VERSION : 'v1',

        service : function(method) {
            return ['/', $.supplier.api.SERVICE_NAME, '/', $.supplier.api.VERSION, '/', method].join(''); 
        },

        /* 
         * Método destinado à pesquisar pelo nome ou código os fornecedors cadastrados.
         */
        search: function(_data) {

            // Execute supplier search endpoint 
            return $.api.request({
                path : $.supplier.api.service('search'),
                method : 'POST',
                body : _data,
                dialogError : {
                    title : messages.supplier.search.dialog.title,
                    message : messages.supplier.search.dialog.errormessage
                }
            }); 

        }, // End search()

        /**
         *  Método persiste o fornecedor.
         */
        save: function(_data) {

            // Execute custumers delete endpoint 
            return $.api.request({
                path : $.supplier.api.service('save'),
                method : 'POST',
                body : _data,
                progressBar : $('.progress-bar-form'),
                dialogSuccess : {
                    title : messages.supplier.save.dialog.title,
                    message : messages.supplier.save.dialog.success 
                },
                dialogError : {
                    title : messages.supplier.save.dialog.title,
                    message : messages.supplier.save.dialog.errormessage
                }
            }).then(function(response) {
                $('form.supplier-form').populate(response.result);
                return response;
            });

        }, // End save()

        /**
         *  Método realiza a exclusão do fornecedor.
         */
        delete: function(_id) {

            // Execute custumers delete endpoint 
            return $.api.request({
                path : $.supplier.api.service(_id),
                method : 'DELETE',
                progressBar : $('.progress-bar-table'),
                dialogError : {
                    title : messages.supplier.delete.dialog.title,
                    message : messages.supplier.delete.dialog.errormessage
                }
            });

        }, // End delete()

        list : function(options) {
            return $.api.request($.util.mergeObjects({
                path : $.supplier.api.service('list')
            }, options));    
        } // End list()

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

                            // Preencher form, precisa ser primeiro show tab
                            // senão não atualiza o map 
                            $('form.supplier-form').populate(row);

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
         * Método destinado à carregar a tabela com os fornecedors.
         */
        loadTable: function() {

            $('table').fadeOut();            

            $.supplier.api.list({
                progressBar : $('.progress-bar-table'),
                dialogError : {
                    title : messages.supplier.list.dialog.title,
                    message : messages.supplier.list.dialog.errormessage
                }                
            }).then(function(response) {
                $.supplier.view.bindTable(response.result);
            });

        }, // Fim loadTable

        /**
         * Load page event.
         */
         loadPage : function() {

            // Aplicar i18n
            $('span.tab_list').text(messages.supplier.tab.list);
            $('span.tab_save').text(messages.supplier.tab.save);
            $('h3.supplier_save_title').text(messages.supplier.save.title);
            $('span.new-item').text(messages.action.new_item);
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

         }


    };

}(jQuery);
