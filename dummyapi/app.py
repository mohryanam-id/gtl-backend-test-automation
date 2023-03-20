from flask import Flask, Response, request
from flask_restx import Api, Resource, fields
import csv

app = Flask(__name__)
api = Api(app, version='1.0', title='Securities List API', description='API for retrieving a list of securities in CSV format.')

security_record = api.model('SecurityRecord', {
    'name': fields.String(required=True, description='Name of the company.'),
    'symbol': fields.String(required=True, description='Symbol of the security.'),
    'exchangeMarket': fields.String(required=True, description='Exchange market where the security is listed.'),
    'dateOfListing': fields.Date(required=True, description='Date the security was listed.'),
    'outstandingShares': fields.Integer(required=True, description='Number of outstanding shares of the security.')
})

@api.route('/getSecuritiesList')
class SecuritiesList(Resource):
    @api.doc('get_securities_list', params={
        'page': {'in': 'query', 'description': 'Page number', 'type': 'int', 'default': 1},
        'size': {'in': 'query', 'description': 'Number of records per page', 'type': 'int', 'default': 20}
    })
    @api.response(200, 'CSV file containing a list of securities.')
    def get(self):
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
        start = (page - 1) * size
        end = start + size
        securities = []
        with open('dummyapi/data/stg_env_securities.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                securities.append(row)
        securities = securities[start:end]
        output = ','.join(['NAME OF COMPANY', 'SYMBOL', 'Exchange Market', 'DATE OF LISTING', 'Outstanding Shares']) + '\n'
        for security in securities:
            output += ','.join([security['NAME OF COMPANY'], security['SYMBOL'], security['Exchange Market'], security['DATE OF LISTING'], security['Outstanding Shares']]) + '\n'
        return Response(output, mimetype='text/csv')
    
if __name__ == '__main__':
    app.run(debug=True, port=7777)
