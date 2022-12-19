from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    characterFavorites = db.relationship(Characters,
                            secondary = characterFavorites,
                            lazy = 'subquery',
                            backref = db.backref('users', lazy=True))
    planetFavorites = db.relationship(Planets,
                            secondary = planetFavorites,
                            lazy = 'subquery',
                            backref = db.backref('users', lazy=True))


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "characterFavorites": self.get_characterFavorites(),
            "planetFavorites": self.get_planetFavorites()
        }

    def get_characterFavorites(self):
        return list(map(lambda index: index.serialize(), self.characterFavorites))

    def get_planetFavorites(self):
        return list(map(lambda index: index.serialize(), self.planetFavorites))



class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(120) , unique=True , nullable=False) #unique = only 1 character w/ the name, nullable =cannot be blank
    planet_from = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String)
        

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
    
    def serialize(self):
        return {
            'planet_id': self.planet_id,
            'name': self.name,
            'diameter': self.diameter,
            'population': self.population,
            'climate': self.climate,
        }

characterFavorites = db.Table("characterFavorites",
    db.Column('user_id', db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column('character_name', db.String(250), db.ForeignKey("characters.name"), primary_key=True),
)

planetFavorites = db.Table("planetFavorites",
    db.Column('user_id', db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column('planet_name', db.String(250), db.ForeignKey("planets.name"), primary_key=True),
)


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    pilot = db.Column(db.String(250))
    vehicle_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))

    def serialize(self):
        return {
            'pilot': self.pilot,
            'vehicle_id': self.vehicle_id,
            'name': self.name
        }