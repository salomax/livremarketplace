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
 * Definir o locale padrão brasileiro para os plugins.
 */
moment.locale('pt-br'); 
jQuery.i18n.properties({
    name:'messages', 
    path:'bundle/', 
    mode:'both',
    language:'pt_BR',
    checkAvailableLanguages: true,
    async: true
});

/**
 * Objeto referente ao menu.
 */
$.menu = {
	/**
	 * Atacha os menus.
	 */
	bind : function() {
		$('a.menu-purchase').bind('click', $.menu.openPurchase);
		$('a.menu-product').bind('click', $.menu.openProduct);
	}, // Fim do bind

	/**
	 * Abre um menu no <section class="content">.
	 */
	openMenu : function(menu) {

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
			$.getScript(menu.script);
			// Aplicar máscaras (inputmask)
			$('input[data-inputmask]').inputmask();
			// Aplicar datepicker
			//Date range picker
			$('input.datepicker').datepicker({
				language: 'pt-BR'
			});

		});

	}, // Fim open()

	/**
	 * Abre o menu de compras.
	 */
	openPurchase : function() {

		$.menu.openMenu({
			icon : 'ion-ios-cart-outline',
			title : 'Compras',
			subtitle : 'Gerencie as compras da loja',
			html : '/purchase/purchase.html', 
			script : '/purchase/purchase.js'
		});

	}, // Fim openPurchase()

	/**
	 * Abre o menu de compras.
	 */
	openProduct : function() {

		$.menu.openMenu({
			icon : 'ion-cube',
			title : 'Produtos',
			subtitle : 'Gerencie os produtos da loja',
			html : '/product/product.html', 
			script : '/product/product.js'
		});

	}  // Fim openProduct()

}; // Fim menu

/**
 * Using jQuery and JSON to populate forms
 * http://stackoverflow.com/questions/7298364/using-jquery-and-json-to-populate-forms
 */
$.fn.populate = function(data) {
	var _form = $(this);
	$.each(json2html_name_list(data), function(key, value) {
	    var $ctrl = $('[name="'+key+'"]', _form);  
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
		$(this).fadeOut(200);
	} else {
		// Mostrar progress
		$(this).show();
		$(this).find('.progress-bar').width(percent + '%').html([message, ' (', percent, ' %)'].join(''));
	}
};
/**
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
						'<button class="btn btn-secundary btn-sm update" data-title="Edit" data-toggle="modal" data-target="#edit">',
						'<span class="glyphicon glyphicon-pencil"></span>',
						'</button>',
						'<button class="btn btn-danger btn-sm delete" data-title="Delete" data-toggle="modal" data-target="#delete">',
						'<span class="glyphicon glyphicon-trash"></span>',
						'</button>',
						'</div>'].join('');
			}

	}; 

}(jQuery);