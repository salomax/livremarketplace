/******************************************************************************
 * sale.js
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
 * Objeto global relativo às vendas.
 */
! function($) {

    /*
     * Inserindo o escopo de vendas.
     */
    $.sale = {};

    /*****************************************************************************
     * Controller API REST 
     *****************************************************************************/

    /**
     * Métodos relativos à API REST do recurso venda.
     */
    $.sale.api = {

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
                    title: messages.sale.save.dialog.title,
                    message: messages.sale.save.dialog.success
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
                    title: messages.sale.save.dialog.title,
                    message: messages.sale.save.dialog.errormessage
                }).danger();

                console.log(reason.result.error.message);

                // promisse
                resolve.reject();
            };

            // Load API e  executar serviço
            gapi.client.load('sale', 'v1', function() {
                var request = gapi.client.sale.save(_data);
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
                        title: messages.sale.delete.dialog.title,
                        message: messages.sale.delete.dialog.success
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
                        title: messages.sale.delete.dialog.title,
                        message: messages.sale.delete.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar promise
                    resolve.reject();
                };

                // Load API e  executar serviço
                gapi.client.load('sale', 'v1', function() {
                    var request = gapi.client.sale.delete({ id: _id });
                    request.then(success, failure);
                }, API_ROOT);

                // retornar promise
                return deferred.promise();
            } // Fim delete

    }; // Fim API


    /*****************************************************************************
     * View components
     *****************************************************************************/

    $.sale.view = {

        /**
         * Método destinado à criar a tabela com os fornecedors.
         */
        bindTable: function(_data) {

            // Construir tabela
            $('table.table-sales').bootstrapTable({
                uniqueId: 'id',
                columns: [{
                    field: 'id',
                    visible: false
                }, {
                    field: 'quantity',
                    title: messages.sale.quantity,
                    searchable: true
                }, {
                    title: '',
                    align: 'center',
                    searchable: false,
                    'class': 'col-sm-2',
                    formatter: $.common.view.tableactionbuttons,
                    events: {
                        'click button.delete': function(e, value, row, index) {
                            $.sale.api.delete(row.id).then(
                                function() {
                                    $('table.table-sales').bootstrapTable('remove', {
                                        field: 'id',
                                        values: [row.id]
                                    });
                                });
                        },
                        'click button.update': function(e, value, row, index) {

                            // Preencher form, precisa ser primeiro show tab
                            // senão não atualiza o map 
                            $('form.sale-form').populate(row);

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
         * Método destinado à carregar a tabela com os fornecedors.
         */
        loadTable: function() {

            // atualizar barra de progresso
            $('.progress-bar-table').progress(50, messages.progressbar.waitingserver);

            // Load API e  executar serviço
            gapi.client.load('sale', 'v1', function() {
                var request = gapi.client.sale.list();
                request.then(
                    function(response) {

                        // atualizar barra de progresso
                        $('.progress-bar-table').progress(75, messages.progressbar.building);

                        // Atachar a lista de compras na tabela
                        $.sale.view.bindTable(response.result);

                        // atualizar barra de progresso					
                        $('.progress-bar-table').progress(100, messages.progressbar.done);

                    },
                    function(reason) {

                        // atualizar barra de progresso					
                        $('.progress-bar-table').progress(100, messages.progressbar.done);

                        // apresentar mensagem ao usuário
                        $('.modal-dialog-message').modalDialog({
                            title: messages.sale.list.dialog.title,
                            message: messages.sale.list.dialog.errormessage
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
    $('span.tab_list').text(messages.sale.tab.list);
    $('span.tab_save').text(messages.sale.tab.save);
    $('h3.sale_save_title').text(messages.sale.save.title);
    $('span.new-item').text(messages.action.new_item);
    $('small.sale_save_subtitle').text(messages.sale.save.subtitle);

    $('label.customer').text(messages.sale.customer);
    $('input[name="customer[name]"]').attr('placeholder', messages.sale.form.customer.placeholder);

    $('label.product').text(messages.sale.product);
    $('input[name="product[name]"]').attr('placeholder', messages.sale.form.product.placeholder);

    $('label.quantity').text(messages.sale.quantity);
    $('input[name="quantity"]').attr('placeholder', messages.sale.form.quantity.placeholder);
    
    $('label.sale_date').text(messages.sale.sale_date);

    $('label.track_code').text(messages.sale.track_code);
    $('input[name="track_code"]').text(messages.sale.form.track_code.placeholder);

    $('label.amount').text(messages.sale.amount);
    $('label.fare').text(messages.sale.sale_date);
    $('label.net_total').text(messages.sale.sale_date);
    
    

    $('button.save').text(messages.action.save);

    $('button.new-item').bind('click', function() {
        $('form.sale-form').trigger('reset');
    });

    // Carregar a lista das vendas
    $.sale.view.loadTable();

    // Criar a validação do formulário
    $('form.sale-form').validate({ // initialize the plugin
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
            name: messages.sale.form.name.required,
            email: messages.sale.form.email.valid
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
            $.sale.api.save(data).then(function(_data) {

                // Zerar o form qdo houver sucesso
                $(form).trigger('reset');

                // Atualizar lista
                var row = $('table.table-sales').bootstrapTable(
                    'getRowByUniqueId', _data.result.id);

                // Insere se não existe ou atualiza caso já esteja inserida
                if (row == null) {
                    $('table.table-sales').bootstrapTable('insertRow', {
                        index: 0,
                        row: _data.result
                    });
                } else {

                    $('table.table-sales').bootstrapTable('updateByUniqueId', {
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
