"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, requests
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite, Planet, Character
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




@app.route('/get/initial', methods=['GET'])
def initial():
    result_char = Character.query.all()
    if not result_char:
        response = requests.get("https://swapi.dev/api/people")
        characters = response.json()['results']

        for pers in characters:
            char_id = pers['url'].split('/')[-2]
            char = Character(name = pers['name'], swapi_id = char_id, url = pers['url'], gender = pers['gender'], eye_color = pers['eye_color'], hair_color = pers['hair_color'] )
            db.session.add(char)
            db.session.commit()
    
    character_records = Character.query.all()
    character_records = list(map(lambda x: x.serialize(), character_records))
    

    result_planet = Planet.query.all()
    if not result_planet:
        response = requests.get("https://swapi.dev/api/planets")
        planets = response.json()['results']

        for planet in planets:
            plan_id = planet['url'].split('/')[-2]
            plan = Planet(name = planet['name'], swapi_id = plan_id, url = planet['url'], population = planet['population'], terrain = planet['terrain'])
            db.session.add(plan)
            db.session.commit()
    
    planet_records = Planet.query.all()
    planet_records = list(map(lambda x: x.serialize(), planet_records))



    records = {
        "character_records": character_records,
        "planet_records": planet_records
    }

    print('record: ', records)
    return jsonify(records)





@app.route('/user', methods=['POST'])
def add_user():
    password = request.json['password']
    firstname = request.json['firstname']
    email = request.json['email']
    is_active = request.json['is_active']
    user = User( password=password, firstname=firstname, email=email, is_active=is_active)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User added successfully", "user": {"email": email, "is_active": is_active}}), 201


@app.route('/login', methods=['POST'])
def log_user():
    email = request.json['email']
    password = request.json['password']
    
    user_exists = User.query.filter_by(email=email, password=password).first()
    print("user_exists", user_exists)
    
    if user_exists:
        user_exists = user_exists.serialize()
        return jsonify(user_exists), 200
    else:
        return "User not found", 404





@app.route('/favorite/plan', methods=['POST'])
def favorite_planet():
    
    body = request.json

    fave = Favorite(name=body['name'], user_id=body['user_id'], planet_id=body['planet_id'], char_id=body['char_id'])
    db.session.add(fave)
    db.session.commit() 
    if fave:
        fave = fave.serialize()
        return jsonify(fave), 200
    else:
        return "User not found", 404
    



@app.route('/favorite/char', methods=['POST'])
def favorite_character():
    
    body = request.json

    fave = Favorite(name=body['name'], user_id=body['user_id'], planet_id=body['planet_id'], char_id=body['char_id'])
    db.session.add(fave)
    db.session.commit() 
    if fave:
        fave = fave.serialize()
        return jsonify(fave), 200
    else:
        return "User not found", 404
    


@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def del_fav_plan(id):
    planet = Favorite.query.get(id)
    db.session.delete(planet)
    db.session.commit()


@app.route('/favorite/planet/', methods=['GET'])
def fav_plan():
    res = Favorite.query.all()
    
    if res:
        res  = res.serialize()
        return jsonify(res), 200
    else:
        return "User not found", 404

    
    







@app.route('/favorite/char/<int:id>',methods=['DELETE'])
def del_fav_char(id):
    character = Favorite.query.get(id)
    db.session.delete(character)
    db.session.commit()






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
