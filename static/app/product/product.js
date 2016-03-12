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
	 * Controller API 
	 *****************************************************************************/

	/**
	 * Métodos relativos à API do recurso produto.
	 */
	$.product.api = {

        SERVICE_NAME : 'product',
        VERSION : 'v1',

        service : function(method) {
            return ['/', $.product.api.SERVICE_NAME, '/', $.product.api.VERSION, '/', method].join(''); 
        },

		/* 
		 * Método destinado à pesquisar pelo nome ou código os produtos cadastrados.
		 */
		search : function(_data) {

            // Execute product delete endpoint 
            return $.api.request({
                path : $.product.api.service('search'),
                method : 'POST',
                body : _data,
                dialogError : {
					title : messages.product.search.dialog.title,
					message : messages.product.search.dialog.errormessage
                }
            });  

		}, // Fim search

		/**
		 *  Método persiste o produto.
		 */
		save : function(_data) {

            // Execute product save endpoint 
            return $.api.request({
                path : $.product.api.service('save'),
                method : 'POST',
                body : _data,
                progressBar : $('.progress-bar-form'),
                dialogSuccess : {
					title : messages.product.save.dialog.title,
					message : messages.product.save.dialog.success 
                },
                dialogError : {
					title : messages.product.save.dialog.title,
					message : messages.product.save.dialog.errormessage
                }
            }).then(function(response) {
                $('form.product-form').populate(response.result);
                return response;
            });

		}, // Fim save

		/**
		 *  Método realiza a exclusão do produto.
		 */
		delete : function(_id) {

            // Execute product delete endpoint 
            return $.api.request({
                path : $.product.api.service(_id),
                method : 'DELETE',
                progressBar : $('.progress-bar-table'),
                dialogError : {
					title : messages.product.delete.dialog.title,
					message : messages.product.delete.dialog.errormessage
                }
            });

		}, // Fim delete

        list : function(options) {
            return $.api.request($.util.mergeObjects({
                path : $.product.api.service('list')
            }, options));    
        }

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
						searchable : true,
                        'class' : 'col-sm-9'                        
					},{
						title : '',
						align : 'center',
						searchable : false,
						'class' : 'col-sm-3',
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
				// striped : true
			});
			$('table').fadeIn();

		}, // Fim bindTable

		/**
		 * Método destinado à carregar a tabela com os produtos.
		 */ 
		loadTable : function() {

            $('table').fadeOut();

            // Execute product list endpoint 
            var request = $.product.api.list({
                progressBar : $('.progress-bar-table'),
                dialogError : {
                    title : messages.product.list.dialog.title,
                    message : messages.product.list.dialog.errormessage
                }
            }).then(
                function(response) {

                    // Create table with response result
                    $.product.view.bindTable(response.result);

                });

		}, // Fim loadTable

		loadPage : function() {

			// Carregar a lista de produtos
			$.product.view.loadTable();

		    // Aplicar i18n
		    $('span.tab_list').text(messages.product.tab.list);
		    $('span.tab_save').text(messages.product.tab.save);
		    $('h3.product_save_title').text(messages.product.save.title);
		    $('span.new-item').text(messages.action.new_item);
		    $('small.product_save_subtitle').text(messages.product.save.subtitle);
		    $('label.name').text(messages.product.name);
		    $('input[name="name"]').attr('placeholder', messages.product.form.name.placeholder);
		    $('label.code').text(messages.product.code);
		    $('input[name="code"]').attr('placeholder', messages.product.form.code.placeholder);
		    
		    $('button.save').text(messages.action.save);

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

		} // Fim loadPage()

	} // Fim $.product.view

}(jQuery);