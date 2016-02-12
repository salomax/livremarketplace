/**
 * Objeto pertinente às funcionalidades da feature de compras (purchase).
 */
purchase = {

	bindList : function(_data) {

		// Construir tabela
		$('table.table-purchases').bootstrapTable({
				uniqueId : 'id',
				columns : [
					{
						field: 'id',
						visible : false
					},
					{
						field : 'product.name',
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
									'<button class="btn btn-secundary btn-sm update" data-title="Edit" data-toggle="modal" data-target="#edit">',
									'<span class="glyphicon glyphicon-pencil"></span>',
									'</button>',
									'<button class="btn btn-danger btn-sm delete" data-title="Delete" data-toggle="modal" data-target="#delete">',
									'<span class="glyphicon glyphicon-trash"></span>',
									'</button>',
									'</div>'].join('');
						},
						events : {
							'click button.delete' : function(e, value, row, index) {
								purchase.delete(row.id).then(
									function() {
											$('table.table-purchases').bootstrapTable('remove', {
											                field: 'id',
											                values: [row.id]
											            });
										});
							},
							'click button.update' : function(e, value, row, index) {
								// mostar tab do form
								$('.nav-tabs a[href="#tab_2"]').tab('show');
								// Preencher form
								$('form.purchase-form').populate(row);
							}
						}				
					}
				],
				pageList : [15],
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
							{field : 'product.name', title : 'Produto'},
							{field : 'supplier', title : 'Fornecedor'},
							{field : 'quantity', title : 'Quantidade'},
							{field : 'purchase_date', title : 'Data da Compra'},
							{field : 'payment_date', title : 'Data do Pagamento'},
							{field : 'received_date', title : 'Data de Recebimento'},
							{field : 'shipping_cost', title : 'Custo de Postagem'},
							{field : 'cost', title : 'Custo por Unidade'},
							{field : 'total_cost', title : 'Custo Total da Compra'},
							{field : 'cost_dollar', title : 'Custo por Unidade (US$)'},
							{field : 'total_cost_dollar', title : 'Custo Total da Compra (US$)'},
							{field : 'exchange_dollar', title : 'Valor do Câmbio'},
							{field : 'invoice', title : 'Dados da Fatura'},
							{field : 'purchase_link', title : 'Link da Compra',
								formatter : function(value, row, index) {
									return ['<a href="', value ,'" target="_blank">', value, "</a>"].join('');
								}
							},
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
		// atualizar barra de progresso
		$('.progress-bar-table').progress(50, 'Aguardo resposta do servidor');
		// Load API e  executar serviço
		gapi.client.load('purchase', 'v1', function() {
			var request = gapi.client.purchase.list();
			request.then(
				function(response) {
					// atualizar barra de progresso
					$('.progress-bar-table').progress(60, 'Construindo tabela');
					// Formatar os campos para a view
					response.result.items = formatter.format({
							data : response.result.items,
							format : [
								{'purchase_date' : formatter.dateFormat},
								{'received_date' : formatter.dateFormat},
								{'payment_date' : formatter.dateFormat},
								{'created_date' : formatter.dateTimeFormat},
							]
							});
					// Atachar a lista de compras na tabela
					purchase.bindList(response.result);
					// atualizar barra de progresso					
					$('.progress-bar-table').progress(100, 'Concluído');
				}, function(reason) {
					// atualizar barra de progresso					
					$('.progress-bar-table').progress(100, 'Concluído');
					// apresentar mensagem ao usuário
					$('.modal-dialog-message').modalDialog({
							title : 'Cadastro Compras',
							message : 'Ocorreu um erro ao tentar cadastar uma compra. Motivo: ' + reason.result.error.message
						}).danger();

				});
		}, API_ROOT);
	},

	put : function(_data) {
		// atualizar barra de progresso
		$('.progress-bar-form').progress(50, 'Aguardo resposta do servidor');
		// Criar controle promise
		var deferred = $.Deferred();
		// fn sucesso
		var success = function(response) {
			// atualizar barra de progresso
			$('.progress-bar-form').progress(100, 'Concluído');
			// apresentar mensagem ao usuário
			$('.modal-dialog-message').modalDialog({
					title : 'Cadastro Compras',
					message : 'Compra cadastrada com sucesso!'
				}).success();
			// Formatar valores
			response.result = formatter.format({
							data : [response.result],
							format : [
								{'purchase_date' : formatter.dateFormat},
								{'received_date' : formatter.dateFormat},
								{'payment_date' : formatter.dateFormat},
								{'created_date' : formatter.dateTimeFormat},
							]
						})[0];
			// promisse
			deferred.resolve(response);
		}; 
		// fn erro
		var failure = function(reason) {
			// atualizar barra de progresso
			$('.progress-bar-form').progress(100, 'Concluído');
			// apresentar mensagem ao usuário
			$('.modal-dialog-message').modalDialog({
					title : 'Cadastro Compras',
					message : 'Ocorreu um erro ao tentar cadastar uma compra. Motivo: ' + reason.result.error.message
				}).danger();
			// promisse
			resolve.reject();
		};
		// Load API e  executar serviço
		gapi.client.load('purchase', 'v1', function() {
			var request = gapi.client.purchase.put(_data);
			request.then(success, failure);
		}, API_ROOT);
		// retornar promise
		return deferred.promise();
	},

	delete : function(_id) {
		// atualizar barra de progresso
		$('.progress-bar-table').progress(50, 'Aguardo resposta do servidor');
		// Criar controle promise
		var deferred = $.Deferred();
		// fn sucesso
		var success = function(response) {
			// atualizar barra de progresso
			$('.progress-bar-table').progress(100, 'Concluído');
			// apresentar mensagem ao usuário
			$('.modal-dialog-message').modalDialog({
					title : 'Exclusão Compras',
					message : 'Compra removida com sucesso!'
				}).success();
			// Executar promise
			deferred.resolve();
		};
		// fn erro
		var failure = function(reason) {
			// atualizar barra de progresso
			$('.progress-bar-table').progress(100, 'Concluído');
			// apresentar mensagem ao usuário
			$('.modal-dialog-message').modalDialog({
					title : 'Exclusão Compras',
					message : 'Ocorreu um erro ao tentar remover uma compra. Motivo: ' + reason.result.error.message
				}).danger();
			// Executar promise
			resolve.reject();
		};
		// Load API e  executar serviço
		gapi.client.load('purchase', 'v1', function() {
			var request = gapi.client.purchase.delete({id:_id});
			request.then(success, failure);
		}, API_ROOT);
		// retornar promise
		return deferred.promise();
	}

};

// Carregar a lista de compras asinc
purchase.load();

// Validação do formulário
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
    	// Convert form to JSON Object
    	var data = $(form).serializeObject();
    	// Para se adequar ao padrão RFC3339 os campos data são convertidos
    	data.purchase_date = toRFC3339(data.purchase_date);
    	data.received_date = toRFC3339(data.received_date);
    	data.payment_date = toRFC3339(data.payment_date);
    	console.log(data);
    	// Submeter ao endpoint
	    purchase.put(data).then(function(_data) {
	    	// Zerar o form qdo houver sucesso
	    	$(form).trigger('reset');
	    	// Atualizar lista
			var row = $('table.table-purchases').bootstrapTable(
				'getRowByUniqueId', _data.result.id);
			// Insere se não existe ou atualiza caso já esteja inserida
			if (row == null) {
		    	$('table.table-purchases').bootstrapTable('insertRow', {
	                index: 0,
	                row: _data.result
	            });
			} else {
		    	$('table.table-purchases').bootstrapTable('updateByUniqueId', {
	                id: _data.result.id,
	                row: _data.result
	            });
			}
	    });
	}
});

// Autocomplete para produtos e fornecedores
var products = [
   { value: 'Cílios 123', data: 342342 },
   { value: 'Cílios ABC', data: 123456 },
   { value: 'Batom', data: 123987654 }
];

$('input[name="product[name]"]').autocomplete({
    source: products
});

