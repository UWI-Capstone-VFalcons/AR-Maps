from . import db
from werkzeug.security import generate_password_hash

# The location / building database object
# The building object is responsible to store
# all the relevant information about the building

class Building(db.Model):
    __tablename__ = 'buildings'
    id = db.Column('building_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    address1 = db.Column(db.Text)
    address2 = db.Column(db.Text)
    address3 = db.Column(db.Text)
    image_url = db.Column(db.Text)
    b_type = db.Column(db.String(20), nullable=False)
    info = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float(10,20), nullable=False)
    longitude =  db.Column(db.Float(10, 20), nullable=False)

    def __init__(self, name, address1, address2, address3, image_url, b_type, info, latitude, longitude):
        self.name = name
        self.address1 = address1
        self.address2 = address2
        self.address3 = address3
        self.image_url = image_url
        self.b_type = b_type
        self.info = info
        self.latitude = latitude
        self.longitude = longitude

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


class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column('node_id', db.Integer, primary_key=True)
    description = db.Column(db.String())
    latitude = db.Column(db.Float(10,20), nullable=False)
    longitude =  db.Column(db.Float(10, 20), nullable=False)
    latitude_2 = db.Column(db.Float(10,20))
    longitude_2 = db.Column(db.Float(10,20))

    def __init__(self, latitude, longitude, latitude_2, longitude_2):
        self.latitude = latitude
        self.longitude = longitude
        self.latitude_2 = latitude_2
        self.longitude_2 = longitude_2

    def __repr__(self):
        return '<Node %r>' % self.id

class Path(db.Model):
    __tablename__ = 'path'
    id = db.Column('path_id', db.Integer, primary_key=True)
    start = db.Column(db.Integer, db.ForeignKey('node.node_id'), nullable=False)
    end =  db.Column(db.Integer, db.ForeignKey('node.node_id'), nullable=False)
    length = db.Column(db.Float(10, 20), nullable=False)

    def __init__(self, start, end, length):
        self.start = start
        self.end = end
        self.length = length

    def __repr__(self):
        return '<Path %r>' % self.id