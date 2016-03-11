/******************************************************************************
 * purchase.js
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
 * Global declarations.
 */
! function($) {

    /*
     * Purchase.
     */
    $.purchase = {};

    /*****************************************************************************
     * Controller API 
     *****************************************************************************/

    /**
     * Purchase API methods.
     */
    $.purchase.api = {

    	SERVICE_NAME : 'purchase',
    	VERSION : 'v1',

    	service : function() {
    		return ['/', $.purchase.api.SERVICE_NAME, '/', $.purchase.api.VERSION].join(''); 
    	},

    	/**
    	 * List purchases.
    	 */
		list : function(options) {

	        return $.api.request($.util.mergeObjects({
		            path : [$.purchase.api.service(), 'list'].join('/')
		        }, options));  

		},

		/**
		 * Save purchase.
		 */
		save : function(_data) {

	        // Execute custumers delete endpoint 
	        return $.api.request({
	            path :  [$.purchase.api.service(), 'save'].join('/'),
	            method : 'POST',
	            body : _data,
	            progressBar : $('.progress-bar-form'),
	            dialogSuccess : {
	                title: messages.purchase.save.dialog.title,
	                message: messages.purchase.save.dialog.success
	            },
	            dialogError : {
	                title : messages.purchase.save.dialog.title,
	                message : messages.purchase.save.dialog.errormessage
	            }
	        }).then(function(response) {
                $('form.purchase-form').populate(response.result);
                return response;
            });

		},

	    /**
	     *  Remove a purchase.
	     */
	    delete: function(_id) {

	        // Execute custumers delete endpoint 
	        return $.api.request({
	            path : [$.purchase.api.service(), _id].join('/'),
	            method : 'DELETE',
	            progressBar : $('.progress-bar-table'),
	            dialogSuccess : {
	                title: messages.purchase.delete.dialog.title,
	                message: messages.purchase.delete.dialog.success
	            },
	            dialogError : {
	                title : messages.purchase.delete.dialog.title,
	                message : messages.purchase.delete.dialog.errormessage
	            }
	        });

	    } // Fim delete()

    }; // End $.purchase.api


    /**
     * Purchase view methods.
     */
    $.purchase.view = {

    	/**
    	 * Create table and load purchase list.
    	 */
		loadTable : function(_data) {

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
							title : messages.purchase.product,
		                    'class': 'col-sm-4',
							searchable : true
						},
						{
							field : 'supplier.name',
							title : messages.purchase.supplier,
		                    'class': 'col-sm-3',
							searchable : true
						},
						{
							field : 'quantity',
							title : messages.purchase.quantity,
		                    'class': 'col-sm-1',
							align : 'center',
							searchable : false
						},
						{
							field : 'purchase_date',
							title : messages.purchase.purchase_date,
		                    'class': 'col-sm-1',
							align : 'center',
							searchable : false
						},
						{
							field : 'received_date',
							title : messages.purchase.received_date,
		                    'class': 'col-sm-1',
							align : 'center',
							searchable : false
						},
						{
							title : '',
		                    'class': 'col-sm-2',						
							align : 'center',
							searchable : false,
							formatter : $.common.view.tableactionbuttons,
							events : {
								'click button.delete' : function(e, value, row, index) {
									$.purchase.api.delete(row.id).then(
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
					search : false,
					detailView : true,
					// striped : true,
			        icons: {
			            paginationSwitchDown: 'glyphicon-collapse-down icon-chevron-down',
			            paginationSwitchUp: 'glyphicon-collapse-up icon-chevron-up',
			            refresh: 'glyphicon-refresh icon-refresh',
			            toggle: 'glyphicon-list-alt icon-list-alt',
			            columns: 'glyphicon-th icon-th',
			            detailOpen: 'glyphicon-option-vertical',
			            detailClose: 'glyphicon-minus'
			        },
					detailFormatter : function(index, row, element) {

							var table = $('<table>');
							$(element).append(table);

							_columns = [
								{field : 'product.name', title : 'Produto',
									formatter : function(value, row, index) {
										return  ['<span class="badge">', row.product.code, "</span>", value].join(' ');
									}
								},
								{field : 'supplier.name', title : messages.purchase.supplier},
								{field : 'quantity', title : messages.purchase.quantity},
								{field : 'purchase_date', title : messages.purchase.purchase_date},
								{field : 'payment_date', title : messages.purchase.payment_date},
								{field : 'received_date', title : messages.purchase.received_date},
								{field : 'shipping_cost', title : messages.purchase.shipping_cost},
								{field : 'cost', title : messages.purchase.cost},
								{field : 'total_cost', title : messages.purchase.total_cost},
								{field : 'cost_dollar', title : messages.purchase.cost_dollar},
								{field : 'total_cost_dollar', title : messages.purchase.total_cost_dollar},
								{field : 'exchange_dollar', title : messages.purchase.exchange_dollar},
								{field : 'invoice', title : messages.purchase.invoice},
								{field : 'purchase_link', title : messages.purchase.purchase_link,
									formatter : function(value, row, index) {
										return ['<a href="', value ,'" target="_blank">', value, "</a>"].join('');
									}
								},
								{field : 'track_code', title : messages.purchase.track_code,
									formatter : function(value, row, index) {
										return ['<span class="tracking_info" data-trackcode="', value, '">', value, "</span>"].join('');
									}
								},
								{field : 'created_date', title : messages.purchase.created_date}
								];

							table.bootstrapTable({
								columns : _columns,
								data : [row],
								cardView : true,
								striped : true
							});

							// Bind tracking code info
							$.getScript('/postal/postal.js', function() {
								$('span.tracking_info').bindTrackCode();
							});

							return element;
						}
				});

	            $('table.table-purchases').fadeIn();

		}, // End loadList()

	
        /**
         * Load page event.
         */
        loadPage : function() {

			$('table.table-purchases').fadeOut();

		    // Aplicar i18n
		    $('span.tab_list').text(messages.purchase.tab.list);
		    $('span.tab_save').text(messages.purchase.tab.save);
		    $('h3.purchase_save_title').text(messages.purchase.save.title);
		    $('span.new-item').text(messages.action.new_item);
		    $('small.purchase_save_subtitle').text(messages.purchase.save.subtitle);

		    $('label.name').text(messages.product.name);
		    $('input[name="name"]').attr('placeholder', messages.product.form.name.placeholder);

		    $('label.product').text(messages.purchase.product)
		    $('label.supplier').text(messages.purchase.supplier);
		    $('label.quantity').text(messages.purchase.quantity);
		    $('label.purchase_date').text(messages.purchase.purchase_date);
		    $('label.payment_date').text(messages.purchase.payment_date);
		    $('label.received_date').text(messages.purchase.received_date);
		    $('label.shipping_cost').text(messages.purchase.shipping_cost);
		    $('label.track_code').text(messages.purchase.track_code);
		    $('label.purchase_link').text(messages.purchase.purchase_link);
		    $('label.cost').text(messages.purchase.cost);
		    $('label.total_cost').text(messages.purchase.total_cost);
		    $('label.cost_dollar').text(messages.purchase.cost_dollar);
		    $('label.total_cost_dollar').text(messages.purchase.total_cost_dollar);
		    $('label.exchange_dollar').text(messages.purchase.exchange_dollar);
		    $('label.invoice').text(messages.purchase.invoice);
		    
            $('input[name="quantity"]').attr('placeholder', messages.purchase.form.quantity.placeholder);
            $('input[name="purchase_date"]').attr('placeholder', messages.purchase.form.purchase_date.placeholder);
            $('input[name="payment_date"]').attr('placeholder', messages.purchase.form.payment_date.placeholder);
            $('input[name="received_date"]').attr('placeholder', messages.purchase.form.received_date.placeholder);
            $('input[name="invoice"]').attr('placeholder', messages.purchase.form.invoice.placeholder);
            $('input[name="purchase_link"]').attr('placeholder', messages.purchase.form.purchase_link.placeholder);

		    $('button.save').text(messages.action.save);			
			
			// Carregar a lista de compras asinc
			$.purchase.api.list({
		                progressBar : $('.progress-bar-table'),
		                dialogError : {
		                    title : messages.purchase.list.dialog.title,
		                    message : messages.purchase.list.dialog.errormessage
		                }
		            }).then(function(response) {

						// Formatar os campos para a view
						response.result.items = $.dataFormatter.format({
								data : response.result.items,
								format : [
									{'purchase_date' : $.dataFormatter.dateFormat},
									{'received_date' : $.dataFormatter.dateFormat},
									{'payment_date' : $.dataFormatter.dateFormat},
									{'created_date' : $.dataFormatter.dateTimeFormat},
								]
								});

						// Atachar a lista de compras na tabela
						$.purchase.view.loadTable(response.result);

					});

			// Validação do formulário
			$('form.purchase-form').validate({ // initialize the plugin
			    rules: {
			        'product[id]' : {
			        	required: true,
			        },
			        'supplier[id]' : {
						required: true
			        },
			        quantity : {
			        	required: true,
			        	number: true,
			        	min: 0.01
			        },
			        purchase_date : {
			        	required: true,        	
			        },
			        payment_date : {
			        	required: true,        	
			        },
			        cost : {
			        	required: true, 
			        	number: true,
			        	min: 0.01        	            	
			        },
			        total_cost : {
			        	required: true,
			        	number: true,
			        	min: 0.01
			        }

			    },
			    messages : {
			    	'product[id]' : messages.purchase.form.product.required,
			    	'supplier[id]' : messages.purchase.form.supplier.required,
			    	quantity : messages.purchase.form.supplier.required,
			    	purchase_date : messages.purchase.form.purchase_date.required,
			    	payment_date : messages.purchase.form.payment_date.required,
			    	cost : messages.purchase.form.cost.required,
			    	total_cost : messages.purchase.form.total_cost.required
			    },
			    submitHandler: function(form, event) {

                    // não submete form
                    event.preventDefault();

			    	// Convert form to JSON Object
			    	var data = $(form).serializeObject();

			    	// Para se adequar ao padrão RFC3339 os campos data são convertidos
			    	data.purchase_date = $.toRFC3339(data.purchase_date);
			    	data.received_date = $.toRFC3339(data.received_date);
			    	data.payment_date = $.toRFC3339(data.payment_date);

			    	// Submeter ao endpoint
				    $.purchase.api.save(data).then(function(_data) {

				    	// Format dates
						_data.result = $.dataFormatter.format({
										data : [_data.result],
										format : [
											{'purchase_date' : $.dataFormatter.dateFormat},
											{'received_date' : $.dataFormatter.dateFormat},
											{'payment_date' : $.dataFormatter.dateFormat},
											{'created_date' : $.dataFormatter.dateFormat},
										]
									})[0];

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

			}); // End validate form

			// Autocomplete products
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
					placeholder: messages.purchase.form.product.placeholder
				});
			});
			
			// Autocomplete suppliers
			$.getScript('/supplier/supplier.js', function() {
				$('.supplier-select').$elect({
					search : function(term) {
						return $.supplier.api.search({
							name : term});
					},
					formatData : function(data) {
						return { text: data.name, id: data.id  };
					},
					getItems : function(response) {
						return response.result.items;
					},
					placeholder: messages.purchase.form.supplier.placeholder
				});
			});

			// Bind calculate costs
			$('input[name="quantity"], input[name="cost"], input[name="total_cost"], input[name="shipping_cost"]').bind(
				'keyup paste', function(event) {

					var target = $(event.target);

					var quantity = $('input[name="quantity"]');
					var cost = $('input[name="cost"]');
					var total_cost = $('input[name="total_cost"]');
					var shipping_cost = $('input[name="shipping_cost"]');

					switch (event.target.name) {
						case 'quantity':
						case 'cost':
						case 'shipping_cost':
							total_cost.val(parseFloat(quantity.val() * cost.val()) + parseFloat(shipping_cost.val() ? shipping_cost.val() : '0'));
						break;
						case 'total_cost':
							cost.val((total_cost.val() - shipping_cost.val()) / quantity.val());
						break;
					};

				});

		}, // End $.purchase.view.loadPage()

	}; // End $.purchase.view

}(jQuery); // End !function($)