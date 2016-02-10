var API_ROOT = '//' + document.location.host + '/_ah/api';

purchase = {
	load : function() {

		gapi.client.load('purchase', 'v1', function() {
			var request = gapi.client.purchase.list();
			request.execute(function(response) {
				console.log(response);
				$('section.content').text(response);
			});
		}, API_ROOT);
	}	
};

purchase.load();

