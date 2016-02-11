var API_ROOT = '//' + document.location.host + '/_ah/api';

/**
 * Objeto pertinente às funcionalidades da feature de compras (purchase).
 */
purchase = {

	bindList : function(_data) {

		$('table.table-purchases').bootstrapTable({
				columns : [
					{
						field : 'product',
						title : 'Produto',
						searchable : true
					},
					{
						field : 'supplier',
						title : 'Fornecedor',
						searchable : true
					},
					{
						field : 'quantity',
						title : 'Qtde',
						align : 'center',
						searchable : false
					},
					{
						field : 'purchase_date',
						title : 'Data Compra',
						align : 'center',
						searchable : false
					},
					{
						field : 'received_date',
						title : 'Data Recebimento',
						align : 'center',
						searchable : false
					},
					{
						title : '',
						align : 'center',
						searchable : false,
						formatter : function(value, row, index) {
							return  [
									'<div class="btn-group">',
									'<button class="btn btn-secundary btn-sm" data-title="Edit" data-toggle="modal" data-target="#edit">',
									'<span class="glyphicon glyphicon-download-alt"></span>',
									'</button>',
									'<button class="btn btn-secundary btn-sm" data-title="Edit" data-toggle="modal" data-target="#edit">',
									'<span class="glyphicon glyphicon-pencil"></span>',
									'</button>',
									'<button class="btn btn-danger btn-sm" data-title="Delete" data-toggle="modal" data-target="#delete">',
									'<span class="glyphicon glyphicon-trash"></span>',
									'</button>',
									'</div>'].join('');
						}					
					}
				],
				data : _data.items,
				pagination : true,
				search : true,
				detailView : true,
				striped : true,
		        icons: {
		            paginationSwitchDown: 'glyphicon-collapse-down icon-chevron-down',
		            paginationSwitchUp: 'glyphicon-collapse-up icon-chevron-up',
		            refresh: 'glyphicon-refresh icon-refresh',
		            toggle: 'glyphicon-list-alt icon-list-alt',
		            columns: 'glyphicon-th icon-th',
		            detailOpen: 'glyphicon-option-horizontal',
		            detailClose: 'glyphicon-option-vertical'
		        },
				detailFormatter : function(index, row, element) {

						var table = $('<table>');
						$(element).append(table);

						_columns = [
							{field : 'product', title : 'Produto'},
							{field : 'supplier', title : 'Fornecedor'},
							{field : 'quantity', title : 'Quantidade'},
							{field : 'purchase_date', title : 'Data da Compra'},
							{field : 'received_date', title : 'Data de Recebimento'},
							{field : 'shipping_cost', title : 'Custo de Postagem'},
							{field : 'cost', title : 'Custo por Unidade'},
							{field : 'total_cost', title : 'Custo Total da Compra'},
							{field : 'cost_dollar', title : 'Custo por Unidade (US$)'},
							{field : 'total_cost_dollar', title : 'Custo Total da Compra (US$)'},
							{field : 'exchange_dollar', title : 'Valor do Câmbio'},
							{field : 'invoice', title : 'Dados da Fatura'},
							{field : 'track_code', title : 'Código de Rastreamento'},
							{field : 'created_date', title : 'Data de Criação'}
						];

						table.bootstrapTable({
							columns : _columns,
							data : [row],
							cardView : true,
							striped : true
						});

						return element;
					}
			});

	},

	load : function() {

		$('.progress-bar-table').progress(20, 'Aguardo resposta do servidor');

		gapi.client.load('purchase', 'v1', function() {
			var request = gapi.client.purchase.list();
			request.then(
				function(response) {

					$('.progress-bar-table').progress(60, 'Construindo tabela');

					// Atachar a lista de compras na tabela
					purchase.bindList(response.result);

					$('.progress-bar-table').progress(100, 'Concluído');

				}, function(reason) {

					$('.modal-dialog-message').modalDialog({
							title : 'Cadastro Compras',
							message : 'Ocorreu um erro ao tentar cadastar uma compra. Motivo: ' + reason.result.error.message
						}).danger();

				});
		}, API_ROOT);
	},

	put : function(_data) {

		$('.progress-bar-form').progress(50, 'Aguardo resposta do servidor');

		gapi.client.load('purchase', 'v1', function() {

			var request = gapi.client.purchase.put(_data);
			request.then(
				function(response) {
					
					$('.progress-bar-form').progress(100, 'Concluído');

					$('.modal-dialog-message').modalDialog({
							title : 'Cadastro Compras',
							message : 'Compra cadastrada com sucesso!'
						}).success();

				}, 
				function(reason) {

					$('.progress-bar-form').progress(100, 'Concluído');

					$('.modal-dialog-message').modalDialog({
							title : 'Cadastro Compras',
							message : 'Ocorreu um erro ao tentar cadastar uma compra. Motivo: ' + reason.result.error.message
						}).danger();

				});

		}, API_ROOT);

		return false;
	}

};

// Carregar a lista de compras asinc
purchase.load();

$('form.purchase-form').validate({ // initialize the plugin
    rules: {
        product : {
        	required: true,
			minlength: 3
        },
        supplier : {
			required: true,
			minlength: 3
        },
        quantity : {
        	required: true,
        	number: true,
        	min: 0.01
        },
        purchase_date : {
        	required: true,        	
        },
        cost : {
        	required: true, 
        	number: true,
        	min: 0.01        	            	
        }

    },
    messages : {
    	product : 'Produto é uma informação obrigatória!',
    	supplier : 'Fornecedor é uma informação obrigatória!',
    	quantity : 'Quantidade é numérico obrigatória e maior que zero!',
    	purchase_date : 'Data da Compra é obrigatória!',
    	cost : 'Custo por unidade é numérico e obrigatório!'
    },
    submitHandler: function(form) {
	    purchase.put($(form).serializeObject());
	}
});



