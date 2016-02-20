/******************************************************************************
 * product.js
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
 * Objeto global relativo aos produtos da loja.
 */
!function($) {

	/*
	 * Inserindo o escopo de produto.
	 */
	$.product = {};

	/*****************************************************************************
	 * Controller API REST 
	 *****************************************************************************/

	/**
	 * Métodos relativos à API REST do recurso produto.
	 */
	$.product.api = {

		/* 
		 * Método destinado à pesquisar pelo nome ou código os produtos cadastrados.
		 */
		search : function(_data) {

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
						title : messages.product.search.dialog.title,
						message : messages.product.search.dialog.errormessage
					}).danger();

				console.log (reason.result.error.message);

				// Executar fn erro pelo promise
				resolve.reject();
			} // Fim fn error

			// Load API e executar serviço
			gapi.client.load('product', 'v1', function() {
				var request = gapi.client.product.search(_data);
				request.then(success, error);
			}, API_ROOT);

			// retornar promise
			return deferred.promise();

		}, // Fim search

		/**
		 *  Método persiste o produto.
		 */
		save : function(_data) {

			// atualizar barra de progresso
			$('.progress-bar-form').progress(50, messages.progressbar.waitingserver);

			// criar controle promise
			var deferred = $.Deferred();

			// fn sucesso
			var success = function(response) {

				// atualizar barra de progresso
				$('.progress-bar-form').progress(100, messages.progressbar.done);

				// apresentar mensagem ao usuário
				$('.modal-dialog-message').modalDialog({
						title : messages.product.save.dialog.title,
						message : messages.product.save.dialog.success 
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
						title : messages.product.save.dialog.title,
						message : messages.product.save.dialog.errormessage
					}).danger();

				console.log(reason.result.error.message);

				// promisse
				resolve.reject();
			};

			// Load API e  executar serviço
			gapi.client.load('product', 'v1', function() {
					var request = gapi.client.product.save(_data);
					request.then(success, failure);
				}, API_ROOT);

			// retornar promise
			return deferred.promise();
		}, // Fim save

		/**
		 *  Método realiza a exclusão do produto.
		 */
		delete : function(_id) {

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
						title : messages.product.delete.dialog.title,
						message : messages.product.delete.dialog.success
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
						title : messages.product.delete.dialog.title,
						message : messages.product.delete.dialog.errormessage
					}).danger();

				console.log(reason.result.error.message);

				// Executar promise
				resolve.reject();
			};

			// Load API e  executar serviço
			gapi.client.load('product', 'v1', function() {
				var request = gapi.client.product.delete({id:_id});
				request.then(success, failure);
			}, API_ROOT);

			// retornar promise
			return deferred.promise();
		} // Fim delete

	}; // Fim API


	/*****************************************************************************
	 * View components
	 *****************************************************************************/

	$.product.view = {

		/**
		 * Método destinado à criar a tabela com os produtos.
		 */ 
		bindTable : function(_data) {

			// Construir tabela
			$('table.table-products').bootstrapTable({
				uniqueId : 'id',
				columns : [
					{
						field: 'id',
						visible : false
					},
					{
						field : 'code',
						title : messages.product.code,
						searchable : true,
						'class' : 'col-sm-1'
					},
					{
						field : 'name',
						title : messages.product.name,
						searchable : true
					},{
						title : '',
						align : 'center',
						searchable : false,
						'class' : 'col-sm-2',
						formatter : $.common.view.tableactionbuttons,
						events : {
							'click button.delete' : function(e, value, row, index) {
								$.product.api.delete(row.id).then(
									function() {
											$('table.table-products').bootstrapTable('remove', {
											                field: 'id',
											                values: [row.id]
											            });
										});
							},
							'click button.update' : function(e, value, row, index) {
								// mostar tab do form
								$('.nav-tabs a[href="#tab_2"]').tab('show');
								// Preencher form
								$('form.product-form').populate(row);
							}
						}				
					}
				],
				pageList : [15],
				data : _data.items,
				pagination : true,
				search : true,
				striped : true
			});

		}, // Fim bindTable

		/**
		 * Método destinado à carregar a tabela com os produtos.
		 */ 
		loadTable : function() {

			// atualizar barra de progresso
			$('.progress-bar-table').progress(50, messages.progressbar.waitingserver);

			// Load API e  executar serviço
			gapi.client.load('product', 'v1', function() {
				var request = gapi.client.product.list();
				request.then(
					function(response) {

						// atualizar barra de progresso
						$('.progress-bar-table').progress(75, messages.progressbar.building);

						// Atachar a lista de compras na tabela
						$.product.view.bindTable(response.result);

						// atualizar barra de progresso					
						$('.progress-bar-table').progress(100, messages.progressbar.done);

					}, function(reason) {

						// atualizar barra de progresso					
						$('.progress-bar-table').progress(100, messages.progressbar.done);

						// apresentar mensagem ao usuário
						$('.modal-dialog-message').modalDialog({
								title : messages.product.list.dialog.title,
								message : messages.product.list.dialog.errormessage
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
!function($) {

	// Carregar a lista de produtos
	$.product.view.loadTable();

	// Criar a validação do formulário
	$('form.product-form').validate({ // initialize the plugin
	    rules: {
	        	name : {
	        	required: true,
				minlength: 3
	        },
	        code : {
				required: true,
				minlength: 3
	        }
	    },
	    messages : {
	    	name : messages.product.form.name.required,
	    	code : messages.product.form.code.required
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
		    $.product.api.save(data).then(function(_data) {

		    	// Zerar o form qdo houver sucesso
		    	$(form).trigger('reset');

		    	// Atualizar lista
				var row = $('table.table-products').bootstrapTable(
					'getRowByUniqueId', _data.result.id);

				// Insere se não existe ou atualiza caso já esteja inserida
				if (row == null) {
			    	$('table.table-products').bootstrapTable('insertRow', {
		                index: 0,
		                row: _data.result
		            });
				} else {

			    	$('table.table-products').bootstrapTable('updateByUniqueId', {
		                id: _data.result.id,
		                row: _data.result
		            });
				}

		    });

		}

	}); // Fim validate


}(jQuery);