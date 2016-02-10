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
} // Fim menu



