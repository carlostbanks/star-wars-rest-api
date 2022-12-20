from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(120) , unique=True , nullable=False) #unique = only 1 character w/ the name, nullable =cannot be blank
    planet_from = db.Column(db.String(120), unique=True, nullable=False)
   

#serialize = every single time we add item to the column, we are going to add the id and name to the columns.
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'planet_from': self.planet_from
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




peopleFavorites = db.Table("peopleFavorites",
    db.Column('user_id', db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey("people.id"), primary_key=True),
)

planetFavorites = db.Table("planetFavorites",
    db.Column('user_id', db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey("planets.planet_id"), primary_key=True),
)





class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    peopleFavorite = db.relationship(People,
                            secondary = peopleFavorites,
                            lazy = 'subquery',
                            backref = db.backref('users', lazy=True))
    planetFavorite = db.relationship(Planets,
                            secondary = planetFavorites,
                            lazy = 'subquery',
                            backref = db.backref('users', lazy=True))


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "peopleFavorites": self.get_peopleFavorites(),
            "planetFavorites": self.get_planetFavorites()
        }

    def get_peopleFavorites(self):
        return list(map(lambda index: index.serialize(), self.peopleFavorite))

    def get_planetFavorites(self):
        return list(map(lambda index: index.serialize(), self.planetFavorite))






