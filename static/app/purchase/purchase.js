var API_ROOT = '//' + document.location.host + '/_ah/api';

purchase = {

	bindList : function(_data) {
		// Construir tabela com as compras
		$('table.table-purchases').bootstrapTable({
			columns : [{
			        field: 'product',
			        title: 'Produto'
			    }, {
			        field: 'quantity',
			        title: 'Quantidade'
			    }, {
			        field: 'cost',
			        title: 'Custo'
			    }, {
			        field: 'supplier',
			        title: 'Fornecedor'
			    }],	
			data : _data.items	
		});

		$('table.table-purchases').DataTable({
          "paging": true,
          "lengthChange": false,
          "searching": true,
          "ordering": false,
          "info": false,
          "autoWidth": false
        });

        $('div.fixed-table-loading').remove();

	},

	load : function() {

		gapi.client.load('purchase', 'v1', function() {
			var request = gapi.client.purchase.list();
			request.execute(function(response) {
				// Atachar a lista de compras na tabela
				purchase.bindList(response);
			});
		}, API_ROOT);
	}	
};

purchase.load();

