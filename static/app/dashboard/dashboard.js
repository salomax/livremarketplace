/******************************************************************************
 * dashboard.js
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
 * Objeto global relativo ao dashboard da loja.
 */
! function($) {

    /*
     * Inserindo o escopo do dashboard.
     */
    $.dashboard = {};

    /*****************************************************************************
     * Controller API 
     *****************************************************************************/

    /**
     * Métodos relativos à API do recurso produto.
     */
    $.dashboard.api = {

        /* 
         * Método destinado à obtenção dos dados do fluxo de caixa.
         */
        cashFlow: function(_data) {

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
                        title: messages.product.search.dialog.title,
                        message: messages.product.search.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar fn erro pelo promise
                    resolve.reject();
                } // Fim fn error

            // Load API e executar serviço
            gapi.client.load('dashboard', 'v1', function() {
                var request = gapi.client.dashboard.cash_flow(_data);
                request.then(success, error);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();

        }, // Fim cash flow

        /** 
         * Método destinado à obtenção do faturamento total.
         */
        revenue: function() {

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
                        title: messages.product.search.dialog.title,
                        message: messages.product.search.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar fn erro pelo promise
                    resolve.reject();
                } // Fim fn error

            // Load API e executar serviço
            gapi.client.load('dashboard', 'v1', function() {
                var request = gapi.client.dashboard.revenue();
                request.then(success, error);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();

        }, // Fim revenue

        /** 
         * Método destinado à obtenção do lucro líquido.
         */
        netProfit: function() {

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
                        title: messages.product.search.dialog.title,
                        message: messages.product.search.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar fn erro pelo promise
                    resolve.reject();
                } // Fim fn error

            // Load API e executar serviço
            gapi.client.load('dashboard', 'v1', function() {
                var request = gapi.client.dashboard.net_profit();
                request.then(success, error);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();

        }, // Fim netProfit

        /** 
         * Método destinado à obtenção da margem líquida.
         */
        profitMargin: function() {

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
                        title: messages.product.search.dialog.title,
                        message: messages.product.search.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar fn erro pelo promise
                    resolve.reject();
                } // Fim fn error

            // Load API e executar serviço
            gapi.client.load('dashboard', 'v1', function() {
                var request = gapi.client.dashboard.profit_margin();
                request.then(success, error);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();

        }, // Fim profitMargin

        /** 
         * Método destinado à obtenção do ticket médio.
         */
        averageTicket: function() {

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
                        title: messages.product.search.dialog.title,
                        message: messages.product.search.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar fn erro pelo promise
                    resolve.reject();
                } // Fim fn error

            // Load API e executar serviço
            gapi.client.load('dashboard', 'v1', function() {
                var request = gapi.client.dashboard.average_ticket();
                request.then(success, error);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();

        }, // Fim average_ticket

        /** 
         * Método destinado à obtenção do totalizador de vendas.
         */
        countSales: function() {

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
                        title: messages.product.search.dialog.title,
                        message: messages.product.search.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar fn erro pelo promise
                    resolve.reject();
                } // Fim fn error

            // Load API e executar serviço
            gapi.client.load('dashboard', 'v1', function() {
                var request = gapi.client.dashboard.count_sales();
                request.then(success, error);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();

        }, // Fim count_sales

       /** 
         * Método destinado à obtenção do totalizador de clientes.
         */
        countCustomers: function() {

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
                        title: messages.product.search.dialog.title,
                        message: messages.product.search.dialog.errormessage
                    }).danger();

                    console.log(reason.result.error.message);

                    // Executar fn erro pelo promise
                    resolve.reject();
                } // Fim fn error

            // Load API e executar serviço
            gapi.client.load('dashboard', 'v1', function() {
                var request = gapi.client.dashboard.count_customers();
                request.then(success, error);
            }, API_ROOT);

            // retornar promise
            return deferred.promise();

        }, // Fim count_customers

    }; // Fim $.dashboard.api

}(jQuery);


/**
 * Bloco de execução startup da página.
 */
! function() {

    var LOADING_CLASS = 'glyphicon glyphicon-refresh glyphicon-refresh-animate';
    var LOADING = '<span class="' + LOADING_CLASS + '"></span> ' + messages.dashboard.loading;

    var showCashFlowChart = function(count) {

        $('#cash_flow-chart').html(LOADING);

        // Carregar informações do fluxo de caixa a partir do 'n'
        $.dashboard.api.cashFlow({ 'count': count }).then(
            function(response) {
                
                $('#cash_flow-chart').empty();

                // Formatar o período para suportar o Morris Chart
                response.result.items = $.dataFormatter.format({
                    data: response.result.items,
                    format: [{
                        'period': function(value) {
                            return moment(value).format('YYYY-MM');
                        }
                    }]
                });

                // Criar gráfico
                Morris.Bar({
                    element: 'cash_flow-chart',
                    resize: true,
                    data: response.result.items,
                    barColors: ['#00A65A', '#F39C12', '#0073B7', '#605CA8'],
                    xkey: 'period',
                    ykeys: ['sales', 'purchases', 'balance', 'accumulated_balance'],
                    labels: [messages.sale.title, 
                             messages.purchase.title, 
                             messages.dashboard.balance.title,
                             messages.dashboard.accumulated_balance.title],
                    xLabelFormat : function(x) { return moment(x.label).format('MMM YYYY'); }
                });

            });

    };

    // i18n
    $('span.cash_flow_chart_title').text(messages.dashboard.cashflow.title);
    $('small.cash_flow_chart_subtitle').text(messages.dashboard.cashflow.subtitle);
    $('p.revenue').text(messages.dashboard.revenue.title);
    $('p.net_profit').text(messages.dashboard.netprofit.title);
    $('p.profit_margin').text(messages.dashboard.profitmargin.title);
    $('p.average_ticket').text(messages.dashboard.averageticket.title);
    $('p.count span.sales').text(messages.dashboard.sales.title);
    $('p.count sup.customers').text(messages.dashboard.customers.title);
    $('p.instock').text(messages.dashboard.instock.title);

    // Período default para carregar o fluxo de caixa
    var COUNT_MONTH_CASH_FLOW_DEFAULT = 3;

    // Carregar informações do fluxo de caixa a partir do 'n'
    showCashFlowChart(COUNT_MONTH_CASH_FLOW_DEFAULT);

    $('a.cash_flow_chart_3months').text(messages.dashboard.cashflow.threemonths).bind(
        'click',
        function() {
            showCashFlowChart(3);
        });

    $('a.cash_flow_chart_6months').text(messages.dashboard.cashflow.sixmonths).bind(
        'click',
        function() {
            showCashFlowChart(6);
        });

    $('a.cash_flow_chart_1year').text(messages.dashboard.cashflow.oneyear).bind(
        'click',
        function() {
            showCashFlowChart(12);
        });
    
    // Obter valor de faturamento
    $('h3.revenue span.value').addClass(LOADING_CLASS);
    $.dashboard.api.revenue().then(
      function(response) { 
        $('h3.revenue span.value').removeClass().text($.number(response.result.value));
      });  

    // Obter valor de faturamento
    $('h3.net_profit span.value').addClass(LOADING_CLASS);
    $.dashboard.api.netProfit().then(
      function(response) { 
        $('h3.net_profit span.value').removeClass().text($.number(response.result.value));
      }); 

    // Obter valor de faturamento
    $('h3.profit_margin span.value').addClass(LOADING_CLASS);
    $.dashboard.api.profitMargin().then(
      function(response) { 
        $('h3.profit_margin span.value').removeClass().text($.number(response.result.value * 100, 1));
      }); 

    // Obter o ticket médio
    $('h3.average_ticket span.value').addClass(LOADING_CLASS);
    $.dashboard.api.averageTicket().then(
      function(response) { 
        $('h3.average_ticket span.value').removeClass().text($.number(response.result.value, 2));
      }); 

    // Obter count de vendas
    $('h3.count span.sales').addClass(LOADING_CLASS);
    $.dashboard.api.countSales().then(
      function(response) { 
        $('h3.count span.sales').removeClass().text(response.result.value);
      }); 

    // Obter count de clientes
    $('h3.count sup.customers').addClass(LOADING_CLASS);
    $.dashboard.api.countCustomers().then(
      function(response) { 
        $('h3.count sup.customers').removeClass().text(response.result.value);
      }); 


}();
