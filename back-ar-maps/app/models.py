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

# The model define all nodes that are used in the paths
class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column('node_id', db.Integer, primary_key=True)
    description = db.Column(db.Text)
    latitude = db.Column(db.Float(10,20), nullable=False)
    longitude =  db.Column(db.Float(10, 20), nullable=False)
    latitude_2 = db.Column(db.Float(10,20))
    longitude_2 = db.Column(db.Float(10,20))

    def __init__(self, latitude, longitude, latitude_2, longitude_2):
        self.latitude = latitude
        self.longitude = longitude
        self.latitude_2 = latitude_2
        self.longitude_2 = longitude_2
    
    def __init__(self, latitude, longitude, latitude_2, longitude_2, description):
        self.latitude = latitude
        self.longitude = longitude
        self.latitude_2 = latitude_2
        self.longitude_2 = longitude_2
        self.description = description

    def __repr__(self):
        return '<Node %r>' % self.id

# The model used to save the gps coordinates for the areas that 
# ar maps can be used in 
class MapArea(db.Model):
    __tablename__ = 'map_areas'
    id = db.Column('map_area_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    point1 = db.Column(db.Integer, db.ForeignKey('nodes.node_id'), nullable=False)
    point2 =  db.Column(db.Integer, db.ForeignKey('nodes.node_id'), nullable=False)
    point3 =  db.Column(db.Integer, db.ForeignKey('nodes.node_id'), nullable=False)
    point4 =  db.Column(db.Integer, db.ForeignKey('nodes.node_id'), nullable=False)

    def __init__(self, name="AREA", description = "Map AREA", point1=None, point2=None, point3=None, point4=None):
        self.name = name
        self.description = description
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4

    def __repr__(self):
        return '<Map_Areas %r>' % self.id

# The model saves all the paths that are recorded in the scitech area
class Path(db.Model):
    __tablename__ = 'paths'
    id = db.Column('path_id', db.Integer, primary_key=True)
    map_area = db.Column(db.Integer, db.ForeignKey('map_areas.map_area_id'), nullable=False)
    start = db.Column(db.Integer, db.ForeignKey('nodes.node_id'), nullable=False)
    end =  db.Column(db.Integer, db.ForeignKey('nodes.node_id'), nullable=False)
    length = db.Column(db.Float(10, 20), nullable=False)

    def __init__(self, start, end, length, map_area):
        self.start = start
        self.end = end
        self.length = length
        self.map_area = map_area

    def __repr__(self):
        return '<Path %r>' % self.id

# This model defines all the starting point locations
# to the sci tech area
class Starting_Point(db.Model):
    __tablename__ = 'starting_points'
    id = db.Column('sp_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    latitude = db.Column(db.Float(10,20), nullable=False)
    longitude =  db.Column(db.Float(10, 20), nullable=False)

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Starting_Point %r>' % self.id

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
        return '<Object_Detection_Object %r>' % self.id