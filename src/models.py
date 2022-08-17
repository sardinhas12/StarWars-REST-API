from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.name
            # do not serialize the password, its a security breach
        }
class Character (db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(50), nullable = False, unique = True)
    birth_day = db.Column(db.Integer(), nullable = False)
    gender = db.Column(db.String(20), nullable = False)
 
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_day": self.birth_day,
            "gender": self.gender
            }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    population = db.Column(db.Integer(), nullable=False, unique=True)
    rotation = db.Column(db.String(150), nullable=False)
    orbital = db.Column(db.String(150), nullable=False)
    climate = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Planet %r>' %self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "rotation":self.rotation,
            "orbital": self.orbital,
            "climate": self.climate
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer(), db.ForeignKey('character.id'))
    character = db.relationship(Character)
    planet_id = db.Column(db.Integer(), db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    user = db.relationship(User)

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "character_id":self.character_id,
            "planet_id":self.planet_id,
        }
