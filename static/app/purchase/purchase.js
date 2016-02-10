var API_ROOT = '//' + document.location.host + '/_ah/api';

purchase = {

	bindList : function(_data) {

		alert (_data.items.length);

		// Caso haja algum dado a tabela é montada		
		if (_data.items.length > 0) {

			$('table.table-purchases').DataTable({
	          "paging": true,
	          "lengthChange": false,
	          "searching": true,
	          "ordering": false,
	          "info": false,
	          "autoWidth": false
	        });

		}


	},

	load : function() {

		gapi.client.load('purchase', 'v1', function() {
			var request = gapi.client.purchase.list();
			request.execute(function(response) {
				// Atachar a lista de compras na tabela
				purchase.bindList(response);
			});
		}, API_ROOT);
	},

	put : function() {

		gapi.client.load('purchase', 'v1', function() {

			// Serialize form
			var form = $('form.purchase-form');
			console.log(JSON.stringify($('form').serializeObject()));

 			var data = JSON.stringify($('form').serializeObject());

			var request = gapi.client.purchase.put($('form').serializeObject());
			request.execute(function(response) {
				// Atachar a lista de compras na tabela
				// purchase.bindList(response);

				console.log(response);
			});

		}, API_ROOT);

		return false;
	}

};

// Carregar a lista de compras asinc
purchase.load();

// Atachar o formulário ao endpoint
$('form.purchase-form').bind('submit', purchase.put);

$.fn.serializeObject = function()
{
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