from flask import Flask, jsonify
from flask_cors import CORS

def create_app(test_configure= None):
    app = Flask(__name__)

    #CORS APP
    cors = CORS(app, resources = {r"/api/*":{"origins":"*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
                response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
                return response

    @app.route('/mesages')
    @cross_origin()
    def get_messages():
                return 'GETTING MESSAGES'



    # define endpoint

    @app.route('/')
    def hello():
            return jsonify({"message": 'Helloe world'})

    @app.route('/smiley')
    def smile():
            return jsonify({"message": 'I am smiling'})
    return app 