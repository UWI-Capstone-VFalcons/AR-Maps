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
    latitude = db.Column(db.Float(10,20), nullable=False)
    longitude =  db.Column(db.Float(10, 20), nullable=False)

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Node %r>' % self.id

# This model defines all the starting point locations
# to the sci tech area
class Starting_Point(db.Model):
    __tablename__ = 'starting_points'
    id = db.Column('node_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    latitude = db.Column(db.Float(10,20), nullable=False)
    longitude =  db.Column(db.Float(10, 20), nullable=False)

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<starting_points %r>' % self.id

# This model would save all the objects that can be detected by 
# the object detection model
class OD_Objects(db.Model):
    __tablename__ = 'object_detection_objects'
    id = db.Column('object_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    object_name = db.Column(db.String(200), unique=True, nullable=False)
    latitude = db.Column(db.Float(10,20), nullable=False)
    longitude =  db.Column(db.Float(10, 20), nullable=False)

    def __init__(self, name, object_name, latitude, longitude):
        self.name = name
        self.object_name = object_name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<object_detection_objects %r>' % self.id
