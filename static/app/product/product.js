/**
 * Objeto global relativo aos produtos da loja.
 */
$.product = {};
/**
 * Métodos relativos à API.
 */
$.product.api = {
	// Função para pesquisar pelo nome ou código os produtos cadastrados. 
	search : function(_data) {
		// Criar controle promise
		var deferred = $.Deferred();
		// fn sucesso
		var success = function(response) {
			// resolve promise
			deferred.resolve(response);
		} // Fim fn sucesso
		// fn error
		var error = function(reason) {
			// apresentar mensagem ao usuário
			$('.modal-dialog-message').modalDialog({
					title : 'Pesquisa Produtos',
					message : 'Ocorreu um erro ao tentar pesquisar os produtos cadastrados. Motivo: ' + reason.result.error.message
				}).danger();
			resolve.reject();
		} // Fim fn error
		// Load API e executar serviço
		gapi.client.load('product', 'v1', function() {
			var request = gapi.client.product.search(_data);
			request.then(success, error);
		}, API_ROOT);
		// retornar promise
		return deferred.promise();
	}
};