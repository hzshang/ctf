from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from resources.user import User
from resources.report import Report
from resources.session import Session
from resources.processing import Processing

app = Flask(__name__)
app.secret_key = 'Nq1By9zIqkqnag7yu2'
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api.add_resource(Processing, '/api/processing/', '/api/processing/<string:type>', endpoint='type')
api.add_resource(Report, '/api/report/')
api.add_resource(Session, '/api/session/')
api.add_resource(User, '/api/user/', '/api/user/<string:user_id>', endpoint='user_id')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)  # debug=True
