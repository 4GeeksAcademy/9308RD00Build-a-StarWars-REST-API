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




@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def favorite_planet():
    body = request.json
    id = body['id']
    favorite_planet = body['favorite_planet']
    user_to_fav = body[user_to_fav]
    user_to_fav_planet = body[user_to_fav_planet]

    user_fav = User.query.filter_by(id=id, favorite_planet=favorite_planet).first()



@app.route('/favorite/char/<int:character_id>', methods=['POST'])
def favorite_character():
    body = {
        "name": "",
        "user_id": "5", 
        "planet_id": "0",
        "char_id": "23" 
    }
    body = request.json

    fave = Favorite(name=body['name'], user_to_fav=body['user_id'], )
    db.session.add(fave)
    db.session.commit() 

    user_fav = User.query.filter_by().first()




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
