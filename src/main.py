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
from models import db, User
from models import db, Character
from models import db, Planet
from models import db, Favorite


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
################## User #######################3

@app.route('/user', methods=['GET'])
def handle_hello():
    user_query = User.query.all()
    all_users = list(map(lambda x: x.serialize(), user_query))
    #response_body = {
     #   "msg": "Hello, this is your GET /user response "}
    return jsonify(all_users), 200

############## Character #####################
#Get all characters
@app.route('/character', methods=['GET'])
def get_all_characters():
    character_query = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), character_query))
    response_body = {
        "msg": "Hello, this is your GET /character response "
        }
    return jsonify(all_characters), 200
    
#Get one single character information 
@app.route('/characters/<int:id>', methods=['GET'])
def get_character_by_id(id):
    character = Character.query.filter_by(id=id).first_or_404()
    return jsonify(character.serialize()), 200

# Delete one character
@app.route('/character/<int:character>', methods=['DELETE'])
def character_delete(character_id):
    one_character = Character.query.get(character_id)
    if one_character is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(one_character)
    db.session.commit()
    return ("Successfully deleted"), 200
    
######## Planets #####

#Get a list of all the planets 
@app.route('/planet', methods=['GET'])
def get_all_planets():
    planet_query = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planet_query))
    return jsonify(all_planets), 200

#get one single planet information 
@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    planet = Planet.query.filter_by(id=id).first_or_404()
    return jsonify(planet.serialize()), 200

####### Favorites ######

#get all favorites 
@app.route('/favorites', methods=['GET'])
def get_user_favorites():
    favorite_query = Favorite.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorite_query))
    return jsonify(all_favorites), 200

#Add a new favorite 
@app.route('/favorites', methods=['POST'])
def add_favorite():
    request_body = request.get_json()
    favorite = Favorite(id = request_body["id"], character_id = request_body["character_id"], planet_id = request_body["planet_id"])
    db.session.add(favorite)
    db.session.commit()
    return jsonify("Well done"), 200

#Delete favorite
@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def favorite_delete(favorite_id):
    one_favorite = Favorite.query.get(favorite_id)
    if one_favorite is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(one_favorite)
    db.session.commit()
    return ("Successfully deleted"), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
