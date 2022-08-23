from flask import Flask, jsonify

def create_app(test_configure= None):
    app = Flask(__name__)


    # define endpoint

    @app.route('/')
    def hello():
            return jsonify({"message": 'Helloe world'})

    @app.route('/smiley')
    def smile():
            return jsonify({"message": 'I am smiling'})
    return app 