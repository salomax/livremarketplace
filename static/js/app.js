/**
 * Objeto referente ao menu.
 */
menu = {
	/**
	 * Atacha os menus.
	 */
	bind : function() {
		$('a.menu-purchase').bind('click', menu.openPurchase);
	}, // Fim do bind
	/**
	 * Abre um menu no <section class="content">.
	 */
	openMenu : function(menu) {
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
		menu.openMenu({
			title : 'Compras',
			subtitle : 'Gerencie as compras da loja',
			html : '/purchase/purchase.html', 
			script : '/purchase/purchase.js'
		});
	}  // Fim openPurchase()
}; // Fim menu

/**
 * Método utilitário que transforma um form e um objeto JSON.
 * Caso o campo esteja vazio é atribuído valor NULO.
 */
$.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(value || null);
        } else {
            o[this.name] = this.value || null;
        }
    });
    return o;
};

/**
 * Using jQuery and JSON to populate forms
 * http://stackoverflow.com/questions/7298364/using-jquery-and-json-to-populate-forms
 */
$.fn.populate = function(data) {
	var _form = $(this);
    $.each(data, function(key, value) {
	    var $ctrl = $('[name='+key+']', _form);  
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
		$(this).fadeOut(600);
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
function toRFC3339(str) {

	if (str == undefined || str ==  null) return null;

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