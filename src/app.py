"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
# from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Vehicle, Favorito

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = People.query.all()
    all_people = list(map(lambda person: person.serialize(), all_people))
    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        raise APIException('Person not found', status_code=404)
    return jsonify(person.serialize()), 200

@app.route('/planet', methods=['GET']) 
def get_all_planets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda planet: planet.serialize(), all_planets))
    return jsonify(all_planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    all_vehicles = Vehicle.query.all()
    all_vehicles = list(map(lambda vehicle: vehicle.serialize(), all_vehicles))
    return jsonify(all_vehicles), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_single_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        raise APIException('Vehicle not found', status_code=404)
    return jsonify(vehicle.serialize()), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    all_users = list(map(lambda user: user.serialize(), all_users))
    return jsonify(all_users), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.json.get('user_id')
    if user_id is None:
        raise APIException('User ID is required', status_code=400)
    
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    
    favorites = Favorito.query.filter_by(user_id=user_id).all()
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    if user_id is None:
        raise APIException('User ID is required', status_code=400)
    
    new_favorite = Favorito(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    if user_id is None:
        raise APIException('User ID is required', status_code=400) 

    favorite = Favorito.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.json.get('user_id')
    if user_id is None:
        raise APIException('User ID is required', status_code=400)
    
    new_favorite = Favorito(user_id=user_id, person_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.json.get('user_id')
    if user_id is None:
        raise APIException('User ID is required', status_code=400)
    
    favorite = Favorito.query.filter_by(user_id=user_id, person_id=people_id).first()
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    user_id = request.json.get('user_id')
    if user_id is None:
        raise APIException('User ID is required', status_code=400)
    
    new_favorite = Favorito(user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    user_id = request.json.get('user_id')
    if user_id is None:
        raise APIException('User ID is required', status_code=400)
    
    favorite = Favorito.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200                              
                            

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
