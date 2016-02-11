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
            o[this.name].push(this.value || null);
        } else {
            o[this.name] = this.value || null;
        }
    });
    return o;
};


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
$.fn.showModalDialog = function(className) {
	// Show modal
	$(this).toggleClass(className, true).modal();
	// Remover class qdo fechar
	$(this).on('hidden.bs.modal', function (e) {
		$(this).toggleClass(className, false);
	});
};
/**
 * Handle modal para mensagens.
 */
$.fn.progress = function(percent, message) {
	if (percent == 100) {
		$(this).fadeOut(600);
	} else {
		// Mostrar progress
		$(this).show();
		$(this).find('.progress-bar').width(percent + '%').html([message, ' (', percent, ' %)'].join(''));
	}
};
