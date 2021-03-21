from . import db
from werkzeug.security import generate_password_hash

# The location / building database object
# The building object is responsible to store
# all the relevant information about the building

class Building(db.Model):
    __tablename__ = 'buildings'
    id = db.Column('building_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    b_type = db.Column(db.String(20), nullable=False)
    info = db.Column(db.Text, nullable=False)
    lattitude = db.Column(db.Float(10,6), nullable=False)
    longtitude =  db.Column(db.Float(10, 6), nullable=False)

    def __init__(self, name, b_type, info, lattitude, longtitude):
        self.name = name
        self.b_type = b_type
        self.info = info
        self.lattitude = lattitude
        self.longtitude = longtitude

    def __repr__(self):
        return '<Building %r>' % self.id


# The event database object
# The event object is responsible to store
# the specific events at a loction or event along with the 
# event time and information

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column('event_id', db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'), nullable=False)
    name = db.Column(db.String(200), unique=True, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    info = db.Column(db.Text, nullable=False)

    def __init__(self, building_id, name, dateTime, info):
        self.building_id = building_id
        self.name = name
        self.dateTime = dateTime
        self.info = info

    def __repr__(self):
        return '<Event %r>' % self.id


