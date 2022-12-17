from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(120) , unique=True , nullable=False) #unique = only 1 character w/ the name, nullable =cannot be blank
    planet_from = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String)

#tells python how to print to the console under character
    def __repr__(self):
        return '<Character %r>' % self.name
        

#serialize = every single time we add item to the column, we are going to add the id and name to the columns.
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'planet_from': self.planet_from,
            'birth_year': self.birth_year 
        }

#start Planets here :)
class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120) , unique=True , nullable=False)
    diameter = db.Column(db.Integer)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(120))
    
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            'planet_id': self.planet_id,
            'name': self.name,
            'diameter': self.diameter,
            'population': self.population,
            'climate': self.climate,
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    date_added = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    favorite_characters = db.Column(db.Integer, db.ForeignKey('characters.name'))
    favorite_planets = db.Column(db.Integer, db.ForeignKey('planets.name'))
    favorite_vehicles = db.Column(db.Integer, db.ForeignKey('vehicles.name'))

    def __repr__(self):
        return '<Favorites %r>' % self.name


    def serialize(self):
        return {
            'date_added': self.user_id,
            'user_id': self.user_id,
            'favorite_characters': self.favorite_characters,
            'favorite_planets': self.favorite_planets,
            'favorite_vehicles': self.favorite_vehicles
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    pilot = db.Column(db.String(250))
    vehicle_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            'pilot': self.pilot,
            'vehicle_id': self.vehicle_id,
            'name': self.name
        }