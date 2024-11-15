from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(250), nullable=False)
    firstname = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id, 
            "firstname": self.firstname,
            "email": self.email,
            "is_active": self.is_active
            
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)



class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(250), nullable=False)

        

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    user_to_fav = db.Column(db.Integer, db.ForeignKey('user.id')) 
    user_to_fav_planet = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user_to_fav_char = db.Column(db.Integer, db.ForeignKey('character.id')) 
    user = db.relationship(User)
    character = db.relationship(Character)
    planet = db.relationship(Planet)











def to_dict(self):
        return {}    