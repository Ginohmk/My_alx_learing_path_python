from flask import Flask, jsonify, request
from models import setup_db, Plant
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app,resources={r"*/api/*": {"origins": "*"}})
    
    @app.after_request
    def after_request(response):
        response.headers.add('Acess-Control-Allow-Headers', 'Content-Type, Authorization,true ')
        response.header.add('Access-Control-Allow-Methods', 'GET,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/plants', methods=['GET', 'POST'])
    def get_plants():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        plants = Plant.query.all()
        formatted_plant = [plant.format() for plant in plants]

        return({
            'total_plants': len(formatted_plant),
            'plants': formatted_plant[start:end],
        'Success': True
    })

    return app