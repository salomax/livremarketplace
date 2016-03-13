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
     * Controller API 
     *****************************************************************************/

    /**
     * Métodos relativos à API do recurso venda.
     */
    $.sale.api = {

        SERVICE_NAME : 'sale',
        VERSION : 'v1',

        service : function(method) {
            return ['/', $.sale.api.SERVICE_NAME, '/', $.sale.api.VERSION, '/', method].join(''); 
        },

        /**
         *  Método persiste o fornecedor.
         */
        save: function(_data) {

            return $.api.request({
                path : $.sale.api.service('save'),
                method : 'POST',
                body : _data,
                progressBar : $('.progress-bar-form'),
                dialogSuccess : {
                    title : messages.sale.save.dialog.title,
                    message : messages.sale.save.dialog.success 
                },
                dialogError : {
                    title : messages.sale.save.dialog.title,
                    message : messages.sale.save.dialog.errormessage
                }
            }).then(function(response) {
                $('form.sale-form').populate(response.result);
                return response;
            });

        }, // End save()

        /**
         *  Método realiza a exclusão do fornecedor.
         */
        delete: function(_id) {

            return $.api.request({
                path : $.sale.api.service(_id),
                method : 'DELETE',
                progressBar : $('.progress-bar-table'),
                dialogError : {
                    title : messages.sale.delete.dialog.title,
                    message : messages.sale.delete.dialog.success
                }
            });

        }, // End delete()

        list : function(options) {
            return $.api.request($.util.mergeObjects({
                path : $.sale.api.service('list')
            }, options));    
        } // End list()

    }; // Fim API


    /*****************************************************************************
     * View components
     *****************************************************************************/

    $.sale.view = {

        /**
         * Método destinado à criar a tabela com os fornecedors.
         */
        bindTable : function(_data) {

            // Construir tabela
            $('table.table-sales').bootstrapTable({
                uniqueId: 'id',
                columns: [{
                    field: 'id',
                    visible: false
                }, 
                {
                    field: 'customer.name',
                    'class': 'col-sm-4',
                    title: messages.sale.customer,
                    searchable: true
                }, 
                {
                    field: 'product.name',
                    'class': 'col-sm-4',
                    title: messages.sale.product,
                    searchable: true
                }, 
                {
                    field: 'quantity',
                    'class': 'col-sm-1',
                    align : 'right',
                    title: messages.sale.quantity,
                    searchable: false
                }, 
                {
                    field: 'sale_date',
                    'class': 'col-sm-1',
                    align : 'center',
                    title: messages.sale.sale_date,
                    searchable: true
                }, 
                {
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
                search: false,
                // striped: true
            });
            $('table').fadeIn();

        }, // Fim bindTable

        /**
         * Método destinado à carregar a tabela com os fornecedors.
         */
        loadTable: function() {

            $('table').fadeOut();
            
            // Execute custumers list endpoint 
            var request = $.sale.api.list({
                    progressBar : $('.progress-bar-table'),
                    dialogError : {
                        title : messages.sale.list.dialog.title,
                        message : messages.sale.list.dialog.errormessage
                    }
                }).then(
                    function(response) {

                        // Formatar os campos para a view
                        response.result.items = $.dataFormatter.format({
                                data : response.result.items,
                                format : [
                                    {'sale_date' : $.dataFormatter.dateFormat}
                                ]
                                });

                        // Create table with response result
                        $.sale.view.bindTable(response.result);

                    });

        }, // Fim loadTable

        /**
         * Ação ao carregar a página.
         */
        loadPage : function() {

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
            $('input[name="amount"]').text(messages.sale.form.amount.placeholder);

            $('label.fare').text(messages.sale.fare);
            $('input[name="fare"]').text(messages.sale.form.fare.placeholder);

            $('label.net_total').text(messages.sale.net_total);    
            $('input[name="net_total"]').text(messages.sale.form.net_total.placeholder);
            
            $('button.save').text(messages.action.save);

            // Carregar a lista das vendas
            $.sale.view.loadTable();

            // Criar a validação do formulário
            $('form.sale-form').validate({ // initialize the plugin
                rules: {
                    'customer[name]': {
                        required: true
                    },
                    'product' : {
                        required: true
                    },
                    'quantity' : {
                        required: true
                    },
                    'sale_date' : {
                        required: true
                    },
                    'amount' : {
                        required: true
                    },
                    'net_total' : {
                        required: true
                    }
                },
                messages: {
                    'customer[name]': messages.sale.form.customer.required,
                    'product' : messages.sale.form.product.required ,
                    'quantity' : messages.sale.form.quantity.required ,
                    'sale_date' : messages.sale.form.sale_date.required ,
                    'amount' : messages.sale.form.amount.required ,
                    'net_total' : messages.sale.form.net_total.required 
                },

                /**
                 * Ação ao submeter o formulário.
                 */
                submitHandler: function(form, event) {
                    // não submete form
                    event.preventDefault();

                    // Convert form to JSON Object
                    var data = $(form).serializeObject();

                    // Para se adequar ao padrão RFC3339 os campos data são convertidos
                    data.sale_date = $.toRFC3339(data.sale_date);

                    // Submeter ao endpoint
                    $.sale.api.save(data).then(function(_data) {

                        // Formatar os campos para a view
                        _data.result = $.dataFormatter.format({
                                data : [_data.result],
                                format : [{'sale_date' : $.dataFormatter.dateFormat}]
                            })[0];

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

            // Product autocomplete
            $.getScript('/product/product.js', function() {
                $('.product-select').$elect({
                    search : function(term) {
                        return $.product.api.search({
                                code : term, 
                                name : term});
                    },
                    formatData : function(data) {
                        return { text: '(' + data.code + ') ' + data.name, id: data.id };
                    },
                    getItems : function(response) {
                        return response.result.items;
                    },
                    placeholder: messages.sale.form.product.placeholder
                });
            });            

            // Customer autocomplete
            $.getScript('/customer/customer.js', function() {
                $('.customer-select').$elect({
                    search : function(term) {
                        return $.customer.api.search({
                                name : term});
                    },
                    formatData : function(data) {
                        return { text: data.name, id: data.id };
                    },
                    getItems : function(response) {
                        return response.result.items;
                    },
                    placeholder: messages.sale.form.customer.placeholder
                });
            });   

            // Bind calculate costs
            $('input[name="quantity"], input[name="amount"], input[name="net_total"], input[name="fare"]').bind(
                'keyup paste', function(event) {

                    var target = $(event.target);

                    var quantity = $('input[name="quantity"]');
                    var amount = $('input[name="amount"]');
                    var net_total = $('input[name="net_total"]');
                    var fare = $('input[name="fare"]');

                    switch (event.target.name) {
                        case 'quantity':
                        case 'amount':
                        case 'fare':
                            net_total.val(parseFloat(amount.val() - fare.val()));
                        break;
                        case 'net_total':
                            if (!amount) {
                                amount.val(parseFloat(fare.val() + net_total.val()));
                            } else if (amount) {
                                fare.val(parseFloat(amount.val() - net_total.val()));
                            }                            
                        break;
                    };

                });            

        } // End loadPage()

    } // End $.sale.view

}(jQuery);
