"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets
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

user = [
    {
        'id' : 1,
        'name' : 'Joe Shmoe',
        'email' : 'JBoogie@aol.com',      
    },    

    {
        'id' : 2,
        'name' : 'Jane Doe',
        'email' : 'JDoeADeer95@gmail.com',   
    }
]

characters = [
    {
        'id': 1,
        'name': 'Luke Skywalker',
        'planet_from': 'Tatooine',
        'birth_year': '19 BBY'
    },

    {
        'id': 2,
        'name': 'Darth Vader',
        'planet_from': 'Tatooine',
        'birth_year': '41 BBY'
    }
]

planets = [
    {
        'planet_id': 1,
        'name': 'Tatooine',
        'diameter': '10465',
        'population': '200000',
        'climate': 'arid',
    },

    {
       'id': 2,
       'name': 'Naboo', 
       'diameter': '10465',
       'population': '4500000000',
       'climate': 'temperate',
    }
]

vehicles = [
    {
        'vehicle_id': '001' ,
        'name': 'Sand Crawler',
        'pilot': 'Digger Crawler',
    },

    {
        'vehicle_id': '002',
        'name': 'T-16 skyhopper',
        'pilot': '1',
    }
]

favorites = [
    {
        'date_added': 12152022,
        'user_id': 1,
        'favorite_characters': 
        {
            'name': 'Darth Vader'
        },
        'favorite_planets': 
        {
            'name': 'Naboo'
        },
        'favorite_vehicles': 
        {
        },
    }
]

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
def get_characters():
    all_characters = People.query.all()
    all_characters = list(map(lambda index: index.serialize(), all_characters))
    response_body = all_characters
    return jsonify(response_body), 200



@app.route('/planets' , methods=['GET'])
def get_planets():
    json_text = jsonify(planets)
    return json_text, 200

@app.route('/favorites' , methods=['GET'])
def get_favorites():
    json_text = jsonify(favorites)
    return json_text, 200

@app.route('/vehicles' , methods=['GET'])
def get_vehicles():
    json_text = jsonify(vehicles)
    return json_text, 200

@app.route('/characters/<int:id>', methods=['GET'])
def get_single_character(id):
    single_character = characters[id]
    return jsonify(single_character), 200

@app.route('/vehicles/<int:id>', methods=['GET'])
def get_single_vehicle(id):
    single_vehicle = vehicles[id]
    return jsonify(single_vehicle), 200

@app.route('/users/<int:id>/favorites/', methods=['GET'])
def get_all_favorites(id):
    user = User.query.get(id)
    user.to_dict()
    user_favorites = {
        "favorite_characters": user.favorite_characters,
        "favorite_planets": user.favorite_planets,
        "favorite_vehicles": user.favorite_vehicles
    }
    return jsonify(user_favorites), 200

@app.route('/users/<int:id>/favorites/character/<int:name>', methods=['POST', 'DELETE'])
def add_to_favorite_characters(id, name):
    body = request.get_json()
    if request.method == 'POST':
        user = User.query.get(id)
        character = Characters.query.get(name)
        user.favorite_characters.append(character)
        db.session.commit()
        return "Favorite character has been added", 200
    if request.method == 'DELETE':
        user = User.query.get(id)
        character = Characters.query.get(name)
        user.favorite_characters.remove(character)
        db.session.commit()
        return "Character has been deleted from favorites", 200
    return "POST or DELETE requests were invalid", 404






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)