# [openMarketplace](https://salomax-marketplace.appspot.com) 
<sup>open source light ERP for e-commerces</sup>

![Code Climate](https://codeclimate.com/github/salomax/openMarketplace/badges/gpa.svg)
![Test Coverage](https://codeclimate.com/github/salomax/openMarketplace/badges/coverage.svg)

### Enviroment

- Google Appengine (Endpoints API) and Datastore
- Python
- Bootstrap and JQuery

### Modules in development
- Products
- Suppliers
- Purchases
- Sales
- Cash Flow
- Dashboard
- Reports

### To Do Features
- Android and iOS clients

### Git

	git add .
	git commit -m "Comments"
	git push

### Dev server

	$ dev_appserver.py . --log_level=debug [--clear_datastore] [--clear_search_indexes]

### Upload Application (Example)

	$ appcfg.py -A salomax-marketplace update .

### WebClient

	https://your-app-id.appspot.com/

### Endpoints API

	http://your-app-id.appspot.com/_ah/api/explorer
	
## License

See [LICENSE](https://github.com/salomax/openMarketplace/blob/master/LICENSE).	

