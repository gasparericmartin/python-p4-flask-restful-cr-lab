#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plant_list = []
        for plant in Plant.query.all():
            plant_list.append(plant.to_dict())
        
        response = make_response(plant_list, 200)
        return response

    def post(self):
        new_plant = Plant(
            name = request.json['name'],
            image = request.json['image'],
            price = request.json['price']
        )

        db.session.add(new_plant)
        db.session.commit()

        new_plant_dict = new_plant.to_dict()
        response = make_response(new_plant_dict, 201)
        return response
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()

        response = make_response(plant, 200)
        return response
    
    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first()
        for attr in request.json:
            setattr(plant, attr, request.json[attr])
        
        db.session.add(plant)
        db.session.commit()

        plant_dict = plant.to_dict()

        response = make_response(plant_dict, 200)
        return response
    
    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()

        db.session.delete(plant)
        db.session.commit()

        response_body = {
            "Message deleted": True,
            "Message": "Plant has been deleted"
        }
        response = make_response(response_body, 200)
        return response

api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
