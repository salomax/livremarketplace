/******************************************************************************
 * app.js
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
 * Constante global para link da API.
 */
var API_ROOT = '//' + document.location.host + '/_ah/api';

/**
 * Funções para serem carregadas no load da página main.
 */
 !function($) {

 	$.locale = 'pt-BR';

 	$.main = {};

 	$.main.load = function() {

 		// Definir o locale padrão brasileiro para os plugins.
		moment.locale($.locale); 

		$.i18n.properties({
		    name:'messages', 
		    path:'bundle/', 
		    mode:'both',
		    checkAvailableLanguages: true,
		    async: true,
		    callback : function() {
		    	// Construir menu
		    	$.menu.build();	
		    }
		});

	};

	/**
	 * Object to view functions.
	 */
	$.view = {
		/**
		 * Methods update a progress bar.
		 */
		progressBar : function(options) {
			return {
				update : function(percent, messsage) {
					if (options && options.progressBar) {
						options.progressBar.progress(percent, messsage);
					}
				}
			};
		}
	};

	/**
	 * Util functions.
	 */
	$.util = {

		/**
		 * Merge two javascript objects into one.
		 */
		mergeObjects : function(obj1, obj2) {
			for (var attrname in obj2) { 
				obj1[attrname] = obj2[attrname]; 
			}
			return obj1;
		}

	};

	// API object encapsulates Google API calls.
	$.api = {

		/**
		 * Request google api. 
		 * Return promisse.
		 */
		request : function(options) {

            // Create promise
            var deferred = $.Deferred(function(def) {

	            // fn success
	            var success = function(response) {

	                // update progress bar
	                $.view.progressBar(options).update(100, messages.progressbar.done);

	                // show success dialog
	                if (options.dialogSuccess) {
		                $('.modal-dialog-message').modalDialog({
		                    title: options.dialogSuccess.title,
		                    message: options.dialogSuccess.message
		                }).success();	                	
	                }

	                // Resolve promise
	                def.resolve(response);
	            };

	            // fn error
	            var failure = function(reason) {

	                // update progress bar
	                $.view.progressBar(options).update(100, messages.progressbar.done);

	                // build default message
	                if (!options.dialogError) {
	                	title = messages.dialog.title
	                	message = messages.dialog.failure.message
	                } else {
	                	title = options.dialogError.title
	                	message = options.dialogError.message
	                }

	               // show error dialog
	                $('.modal-dialog-message').modalDialog({
	                    title: title,
	                    message: message
	                }).danger();

	                console.log(reason.result.error.message);

	                // Reject promise
	                resolve.reject(reason);
	            };

	            // Set root
	            options.root = API_ROOT;

	            // update progress bar
				$.view.progressBar(options).update(50, messages.progressbar.waitingserver);

	            // Execute request gapi client
	            request = gapi.client.request(options).then(success, failure);

            });
	
            // return promise
            return deferred.promise();
		}


	};

}(jQuery);

/**
 * Carregar menus.
 */
 !function($) {

 	$.menu = {

 		getMenus : function() {
 			return [
		 			{
		 				header : messages.menu.header.management
		 			}, 
					{
						icon : 'ion-arrow-graph-up-right',
						title : messages.menu.dashboard.title,
						subtitle : messages.menu.dashboard.subtitle,
						html : '/dashboard/dashboard.html', 
						script : '/dashboard/dashboard.js'
					}, 
		 			{
		 				header : messages.menu.header.commercial
		 			}, 
					{
						icon : 'ion-ios-cart-outline',
						title : messages.menu.purchase.title,
						subtitle : messages.menu.purchase.subtitle,
						html : '/purchase/purchase.html', 
						script : '/purchase/purchase.js',
						callback : function() {
							$.purchase.view.loadPage();
						}
					}, 
					{
						icon : 'ion-social-usd',
						title : messages.menu.sale.title,
						subtitle : messages.menu.sale.subtitle,
						html : '/sale/sale.html', 
						script : '/sale/sale.js'
					}, 
		 			{
		 				header : messages.menu.header.registration
		 			},
					{
						icon : 'ion-cube',
						title : messages.menu.product.title,
						subtitle : messages.menu.product.subtitle,
						html : '/product/product.html', 
						script : '/product/product.js',
						callback : function() {
							$.product.view.loadPage();
						}
					},
					{
						icon : 'ion-ios-people',
						title : messages.menu.supplier.title,
						subtitle : messages.menu.supplier.subtitle,
						html : '/supplier/supplier.html', 
						script : '/supplier/supplier.js',
						callback : function() {
							$.supplier.view.loadPage();
						}
					},					
					{
						icon : 'ion-happy-outline',
						title : messages.menu.customer.title,
						subtitle : messages.menu.customer.subtitle,
						html : '/customer/customer.html', 
						script : '/customer/customer.js',
						callback : function() {
							$.customer.view.loadPage();
						}
					}	
 					];
 		},

		/**
		 * Atacha os menus.
		 */
		build : function() {

			// Renderizar todos os menus
			$.each($.menu.getMenus(), function(index, menu) {

				if (menu.header) {

					// Renderizar header (agrupador de menus)
					$.menu.appendHeader(menu.header);

				} else {

					// Renderizar item de menu
					$.menu.appendMenuItem(menu);

				}
	
			});

		}, // Fim do bind

		appendHeader : function(name) {

			var header = $('<li>').addClass('header').appendTo($('ul.top-menu'));
			header.text(name);

		},

		appendMenuItem : function(menu) {

			var itemMenu = $('<li>').appendTo($('ul.top-menu'));
			var link = $('<a>').attr('href', '#').appendTo(itemMenu);

			link.bind('click', function() {
				$.menu.openMenu(menu);
			});

			$('<i>').addClass('ion ' + menu.icon).appendTo(link);
			$('<span>').text(menu.title).appendTo(link);

		},

		/**
		 * Abre um menu no <section class="content">.
		 */
		openMenu : function(menu) {

			$('section.content').hide();

			// Definir o icon
			$('i.icon-title').attr('class', 'icon-title ion ' + menu.icon);

			// Definir título
			$('span.content-header-title').text(menu.title);

			// Definir subtítulo
			$('small.content-header-title').text(menu.subtitle);

			// Mensagem carregando
			$('section.content').html('Carregando ' + menu.title + ' ...');

			// Executar ajax
			$.ajax({
				url: menu.html,
				context: document.body
			}).done(function(response) {

				// Inserir content
				$('section.content').html(response);

				// Inserir script
				$.getScript(menu.script).done(function() {
					// If menu.callback() is present
					if (menu.callback) {
						menu.callback($);
					}					
				});				

				// Aplicar máscaras (inputmask)
				$('input[data-inputmask]').inputmask();

				// Apply datepicker
				$('input.datepicker').datepicker({
					language: $.locale,
					autoclose: true
				});
				// http://stackoverflow.com/questions/21882279/set-default-date-bootstrap-datepicker
				$('input.datepicker').datepicker('setDate', new Date());
				$('input.datepicker').datepicker('update');
				$('input.datepicker').val('');

				// Reset form button
				$('button.new-item').bind('click', function() {
				    	$(this).closest('form').trigger('reset');
				    	$(this).closest('form').find('input').trigger('change');
				    });
				$('button.new-item').prop('disabled', true);
				$('input[name="id"]').change(function() {
					$('button.new-item').prop('disabled', ($(this).val() == ''));
				});

				$('section.content').fadeIn('slow');

			});

		} // Fim open()

	}; // Fim menu

 }(jQuery);

 /**
  * Handling google maps API.
  */
!function($) {

	/**
	 * ìcone default.
	 */
	$.maps = {
		getZoom : function() { return 15 },
		getIcon : function() {
			return {
				size: new google.maps.Size(71, 71),
				origin: new google.maps.Point(0, 0),
				anchor: new google.maps.Point(17, 34),
				scaledSize: new google.maps.Size(25, 25)
			};
		},
		getStartLocation : function() {
			return new google.maps.LatLng(32.5468, -23.203);
		},
		getStartZoom : function() {
			return 2;
		}
	};

	/**
	 * Bind autocomplete search no input.
	 */
	bindAutocompleteMap = function(map, autocomplete) {

		// Validar se é um input
		if (!autocomplete.is('input')) { 
			console.warning('Autocomplete object not is an input HTML element!'); 
			return; 
		}

		// Evitar que o enter ao selecionar uma localização
		// no input de pesquisa do map realize um submit
		autocomplete.keypress(function(event) {
			return event.keyCode != 13;
		});

		// Obter input
	    var input = autocomplete.get(0);

	    // Criar listener para qdo houver um reset
	    // no form do input o mapa tb deve ser "zerado" 
	    $(input.form).bind('reset', function() {
            map.setDefaultLocation();
			map.clearMarkers();    
	    });

	    // Criar pesquisa
	    var searchBox = new google.maps.places.SearchBox(input);
	    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

	    // Bias the SearchBox results towards current map's viewport.
	    map.addListener('bounds_changed', function() {
	        searchBox.setBounds(map.getBounds());
	    });

	    searchBox.addListener('places_changed', function() {
	        var places = searchBox.getPlaces();

	        if (places.length == 0) {
	            return;
	        }

	        // Clear out the old markers.
	        map.clearMarkers();

	        // For each place, get the icon, name and location.
	        var bounds = new google.maps.LatLngBounds();
	        places.forEach(function(place) {

	            // Create a marker for each place.
	            map.markers.push(new google.maps.Marker({
	                map: map,
	                icon: $.maps.icon,
	                title: place.name,
	                position: place.geometry.location
	            }));

	            if (place.geometry.viewport) {
	                // Only geocodes have viewport.
	                bounds.union(place.geometry.viewport);
	            } else {
	                bounds.extend(place.geometry.location);
	            }
	        });

	        // Definir bounds
	        map.fitBounds(bounds);

	        // Melhor zoom
	        if (map.markers.length == 1) map.setZoom(map.getZoom());
	    });
	};

	/**
	 * Bind mapa no elemento.
	 * @see https://developers.google.com/maps/documentation/javascript/examples/places-searchbox
	 */
	$.fn.maps = function(options) {

	    var element = $(this);

	    // Verificar se o elemento já não está carregado
	    // Isto pode lançar exceções no console caso esteja
	    if (element.html() == '') {

	      	// Incluir array dos marcadores ao tipo map
			google.maps.Map.prototype.markers = new Array();
			google.maps.Map.prototype.clearMarkers = function() {
		        this.markers.forEach(function(marker) {
		            marker.setMap(null);
		        });
		        this.markers = [];   
			};

			// Definir a posição inicial perto do usuário, caso o browser permita
	        // https://developers.google.com/maps/documentation/javascript/examples/map-geolocation
	        google.maps.Map.prototype.setDefaultLocation = function() {
	        	var map = this;
		        if (navigator.geolocation) {
		            navigator.geolocation.getCurrentPosition(function(position) {
		                var pos = {
		                    lat: position.coords.latitude,
		                    lng: position.coords.longitude
		                };
		                map.setCenter(pos);
		                map.setZoom($.maps.getZoom());
		            });
		        } // Fim if (navigator.geolocation)
	        };

	        // Criar o objeto mapa
	        var map = new google.maps.Map(
	            element.get(0), {
	                mapTypeControl: false,
	                streetViewControl: false,
	                mapTypeId: google.maps.MapTypeId.ROADMAP
	            });

	        // Definir local inicial (sem marcadores)
			map.setDefaultLocation();

	        // Bind método no elemento HTML para definir local no map
	        $(this).bind('setMapLocation', function(element, pos) { 
		            // Create a marker for each place.
		            map.markers.push(new google.maps.Marker({
		                map: map,
		                icon: $.maps.icon,
		                position: pos
		            }));
		            map.setCenter(pos);
		            map.setZoom($.maps.getZoom());
	        	});

	        // Caso haja autocomplete para o mapa
	        if (options.autocomplete) {

	            // Bind autocomplete
	            bindAutocompleteMap(map, options.autocomplete);

	        } // Fim if (options.autocomplete)

	    } 

	    if (options.autocomplete && $.trim(options.autocomplete.val()).length > 0) { // else if (element.html() == '')

	        var geocoder = new google.maps.Geocoder();
	        var address = options.autocomplete.val();

	        var _this = $(this);

	        geocoder.geocode({ 'address': address }, function(results, status) {

	            if (status == google.maps.GeocoderStatus.OK) {

					var pos = {
		                lat: results[0].geometry.location.lat(),
		                lng: results[0].geometry.location.lng()
		            };

		            _this.trigger('setMapLocation', pos);

	            }

	        });

	    } // Fim else (element.html() == '')

	};

}(jQuery);

/**
 * Using jQuery and JSON to populate forms
 * http://stackoverflow.com/questions/7298364/using-jquery-and-json-to-populate-forms
 */
$.fn.populate = function(data) {
	var _form = $(this);
	$.each(json2html_name_list(data), function(key, value) {
	    var $ctrl = $('[name="' + key + '"]', _form);  
	    if ($ctrl.is("input")) {
		    switch($ctrl.attr("type")) {  
		        case "text" :   
		        case "hidden":  
		        	$ctrl.val(value);   
		        break;   
		        case "radio" : case "checkbox":   
		        $ctrl.each(function(){
		           if($(this).attr('value') == value) {  $(this).attr("checked",value); } });   
		        break;  
		        default:
		        $ctrl.val(value); 
		    }  
	    } else if ($ctrl.is("select")) {
	    	$ctrl.trigger('initSelect', [data[key.split("[")[0]]]);
	    }
	    $ctrl.trigger('change');
    });  
}
json2html_name_list = function (json, result, parent){
    if(!result)result = {};
    if(!parent)parent = '';
    if((typeof json)!='object'){
        result[parent] = json;
    } else {
        for(var key in json){
            var value = json[key];
            if(parent=='')var subparent = key;
            else var subparent = parent+'['+key+']';
            result = json2html_name_list(value, result, subparent);
        }
    }
    return result;
}

/**
 * Handle modal para mensagens.
 */
$.fn.modalDialog = function(options) {
	// Validar
	if (options.title && options.message) {
		// Obter elemento
		var _element =  $(this);
		// Set título
		_element.find('.modal-title').text(options.title);
		// Set mensagem
		_element.find('.modal-body-message').text(options.message);
		// Retorno
		return {
			success : function() {
				// Show modal
				_element.showModalDialog('modal-success');
			},
			danger : function() {
				// Show modal
				_element.showModalDialog('modal-danger');
			}
		}
	}
};
/**
 * Handle modal para mensagens.
 */
$.fn.showModalDialog = function(className, options) {
	// Show modal
	$(this).toggleClass(className, true).modal(options);
	// Remover class qdo fechar
	$(this).on('hidden.bs.modal', function (e) {
		$(this).toggleClass(className, false);
	});
};
/**
 * Handle modal para mensagens.
 */
$.fn.progress = function(percent, message) {
	// iniciar barra de progresso
	if (percent < 100 && $(this).find('.progress-bar').width() == 100) {
		$(this).find('.progress-bar').width('0%').html('0%');
	}
	// verificar se conclui o processo
	if (percent == 100) {
		$(this).find('.progress-bar').width(percent + '%').html([message, ' (', percent, ' %)'].join(''));
		$(this).slideUp();
	} else {
		// Mostrar progress
		$(this).slideDown();
		$(this).find('.progress-bar').width(percent + '%').html([message, ' (', percent, ' %)'].join(''));
	}
};

$.fn.$elect = function(selectOptions) {

	// Init validation
	if (!selectOptions || !selectOptions.search || !selectOptions.formatData) {
		console.warning('$elect initialized inappropriately');
		return;
	}

	// Get select element
	$ctrl = $(this);

	// workround to update data in select2
	// https://github.com/select2/select2/issues/2830#issuecomment-74971872
	$ctrl.bind('initSelect', function(event, _data) {
				console.log('oi' + _data);
			_this = $(this);
			options = {
			  data : [],
			  // placeholder: (selectOptions.placeholder? selectOptions.placeholder : ''),
			  // allowClear: true,
			  ajax: {
			  	transport : function (params, success, failure) {
			  		if (!params.data.term) return;
			  		selectOptions.search(params.data.term)
			  		.then(function(response) {
						success(response);
					});	
			  	},
			  	processResults: function(response) {
			  		if (!selectOptions.getItems(response)) return [];
					return {
	                    results: $.map(selectOptions.getItems(response), function(item) {
	                        return selectOptions.formatData(item);
	                    })
	                };
			    }
			  },
			  width: '100%',
			  templateResult: function(data) {
			  	if (data.loading) {
			  		return messages.select.search;
			  	}
			  	return data.text;
			  }
			};
			option = $('<option selected>teste</option>');

			// Handling data
			if (!_data) {
				_data = { id: '', text: ''}
			} else {
				_data = selectOptions.formatData(_data);
			}

			// Apply init value
			option.val(_data.id);
			option.text(_data.text);
			_this.empty().append(option);
			
			// Create select2
			_this.select2(options);	
	});

	// Init
	$ctrl.trigger('initSelect');

	// Reset selects
	$ctrl.closest("form").bind('reset', function() {
		// Init
		$('select').trigger('initSelect');
	});
};

/**
 * Carregar todos os elementos que são genéricos 
 * ou comnuns na aplicação.
 */
!function($) {

	// Namespace common (comunm)
	$.common = {};

	// Variáveis e funções comuns inerentes à view.
	$.common.view = {

		/**
		 * Função que retorna os botões de ação update 
		 * e delete de uma tabela de dados.
		 */
		tableactionbuttons : function(value, row, index) {
				return  [
						'<div class="btn-group">',
						'<button class="btn btn-link btn-sm update" data-title="Edit" data-toggle="modal" data-target="#edit">',
						'<span class="glyphicon glyphicon-pencil"></span>',
						'</button>',
						'<button class="btn btn-link btn-sm delete" data-title="Delete" data-toggle="modal" data-target="#delete">',
						'<span class="glyphicon glyphicon-trash"></span>',
						'</button>',
						'</div>'].join('');
			}

	}; 

}(jQuery);

/**
 * TODO colocar no common.
 * Método utilizado para se adequar ao padrão 
 * RFC3339 os campos data são convertidos.
 */
$.toRFC3339 = function (str) {
	// Validação
	if (!str || !str.length) return null;

	var pattern = /(\d{2})\/(\d{2})\/(\d{4})/;
	var date = new Date(str.replace(pattern,'$3-$2-$1'));

	pad = function(n) {return n<10 ? '0'+n : n}

	return date.getUTCFullYear()+'-'
	      + pad(date.getUTCMonth()+1)+'-'
	      + pad(date.getUTCDate())+'T'
	      + pad(date.getUTCHours())+':'
	      + pad(date.getUTCMinutes())+':'
	      + pad(date.getUTCSeconds())
}
/**
 * TODO colocar no common. 
 * Objeto auxiliar para formatação de dados.
 */
$.dataFormatter = {
	// Método para definir a formatação.
	format : function(options) {
		// Validar informação
		if (!(options 
			&& options.data 
			&& options.data instanceof Array 
			&& options.data.length > 0)) return;
		// Realizar formatação do array
		data = options.data;
		$.each(data, function(index, row) {
			$.each(row, function(key, value) {
				$.each(options.format, function(_index, format) {
					if (format[key] != undefined) {
						row[key] = format[key](value);
					}
				});
			}); // Fim each
		}); // Fim for
		return data;
	}, // Fim format()
	// Formatação padrão para data.
	dateFormat : function(value) {
		return moment(value).format('L');
	},
	// Formatação padrão para data e hora.
	dateTimeFormat : function(value) {
		return moment(value).format('LLL');
	}
};
