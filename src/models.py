from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)

    user = db.relationship('User', back_populates='favoritos')
    people = db.relationship('People', back_populates='favoritos')
    planet = db.relationship('Planet', back_populates='favoritos')
    vehicle = db.relationship('Vehicle', back_populates='favoritos')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favoritos = db.relationship('Favorito', back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    height = db.Column(db.String(10), nullable=False)
    mass = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    favoritos = db.relationship('Favorito', back_populates='people')

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    diameter = db.Column(db.String(10), nullable=False)
    population = db.Column(db.String(10), nullable=False)
    climate = db.Column(db.String(20), nullable=False)
    terrain = db.Column(db.String(20), nullable=False)
    favoritos = db.relationship('Favorito', back_populates='planet')

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    length = db.Column(db.String)
    crew = db.Column(db.String)
    passengers = db.Column(db.String)
    favoritos = db.relationship('Favorito', back_populates='vehicle')

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
        }