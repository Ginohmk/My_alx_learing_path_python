from flask import Flask, jsonify, request, abort
from models import setup_db, Plant
from flask_cors import CORS

def create_app(test_config=None):
        app = Flask(__name__)
        setup_db(app)
        CORS(app)
        
        @app.after_request
        def after_request(response):
            response.headers.add('Acess-Control-Allow-Headers', 'Content-Type, Authorization,true ')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,DELETE,OPTIONS')
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

        @app.route('/plants/<int:plant_id>', methods=['GET'])
        def get_specific_plant(plant_id):
            plant = Plant.query.get(plant_id)

            if plant is None:
                abort(404)
            else:
                return({
                    'status': True,
                    'plant': plant.format()
                })

        return app