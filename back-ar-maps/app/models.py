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
    latitude = db.Column(db.Numeric(9,6), nullable=False)
    longitude =  db.Column(db.Numeric(9,6), nullable=False)

    def __init__(self, name="unname", address1=None, address2=None, address3=None, image_url="default_building.jpg", b_type="Lecture Theatre", info="no imformation added", latitude=None, longitude=None):
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
    latitude_1 = db.Column(db.Numeric(9,6), nullable=False)
    longitude_1 =  db.Column(db.Numeric(9,6), nullable=False)
    latitude_2 = db.Column(db.Numeric(9,6))
    longitude_2 = db.Column(db.Numeric(9,6))
    
    def __init__(self, latitude_1, longitude_1, latitude_2, longitude_2, description="no description"):
        self.latitude_1 = latitude_1
        self.longitude_1 = longitude_1
        self.latitude_2 = latitude_2
        self.longitude_2 = longitude_2
        self.description = description

    def __repr__(self):
        return '<Node %r>' % self.id

# The model used to save the gps coordinates for the areas that 
# ar maps can be used in 
# The cordinates are saved moving in a clockwise direction
class MapArea(db.Model):
    __tablename__ = 'map_areas'
    id = db.Column('map_area_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    latitude_1 = db.Column(db.Numeric(9,6), nullable=False)
    longitude_1 =  db.Column(db.Numeric(9,6), nullable=False)

    latitude_2 = db.Column(db.Numeric(9,6), nullable=False)
    longitude_2 =  db.Column(db.Numeric(9,6), nullable=False)

    latitude_3 = db.Column(db.Numeric(9,6), nullable=False)
    longitude_3 =  db.Column(db.Numeric(9,6), nullable=False)

    latitude_4 = db.Column(db.Numeric(9,6), nullable=False)
    longitude_4 =  db.Column(db.Numeric(9,6), nullable=False)

    def __init__(self, name="AREA", description = "Map AREA", latitude_1=None, longitude_1=None, latitude_2=None, longitude_2=None, latitude_3=None, longitude_3=None, latitude_4=None, longitude_4=None):
        self.name = name
        self.description = description
        self.latitude_1 = latitude_1
        self.longitude_1 = longitude_1
        self.latitude_2 = latitude_2
        self.longitude_2 = longitude_2
        self.latitude_3 = latitude_3
        self.longitude_3 = longitude_3
        self.latitude_4 = latitude_4
        self.longitude_4 = longitude_4

    def __repr__(self):
        return '<Map_Area %r>' % self.id

# The model used to save the gps coordinates for the zones that 
# are in an area  
class MapZone(db.Model):
    __tablename__ = 'map_zones'
    id = db.Column('map_zone_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    map_area = db.Column(db.Integer, db.ForeignKey('map_areas.map_area_id'), nullable=False)

    latitude_1 = db.Column(db.Numeric(9,6), nullable=False)
    longitude_1 =  db.Column(db.Numeric(9,6), nullable=False)

    latitude_2 = db.Column(db.Numeric(9,6), nullable=False)
    longitude_2 =  db.Column(db.Numeric(9,6), nullable=False)

    latitude_3 = db.Column(db.Numeric(9,6), nullable=False)
    longitude_3 =  db.Column(db.Numeric(9,6), nullable=False)

    latitude_4 = db.Column(db.Numeric(9,6), nullable=False)
    longitude_4 =  db.Column(db.Numeric(9,6), nullable=False)

    def __init__(self, name="Zone", map_area=None, latitude_1=None, longitude_1=None, latitude_2=None, longitude_2=None, latitude_3=None, longitude_3=None, latitude_4=None, longitude_4=None):
        self.name = name
        self.map_area = map_area
        self.latitude_1 = latitude_1
        self.longitude_1 = longitude_1
        self.latitude_2 = latitude_2
        self.longitude_2 = longitude_2
        self.latitude_3 = latitude_3
        self.longitude_3 = longitude_3
        self.latitude_4 = latitude_4
        self.longitude_4 = longitude_4

    def __repr__(self):
        return '<Map_Zone %r>' % self.id

# The model saves all the paths that are recorded in the scitech area
class Path(db.Model):
    __tablename__ = 'paths'
    id = db.Column('path_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    map_area = db.Column(db.Integer, db.ForeignKey('map_areas.map_area_id'), nullable=False)
    start = db.Column(db.Integer, db.ForeignKey('nodes.node_id'), nullable=False)
    end =  db.Column(db.Integer, db.ForeignKey('nodes.node_id'), nullable=False)
    length = db.Column(db.Numeric(9,6))

    def __init__(self, name="unname", start=None, end=None, length=None, map_area=None):
        self.name = name
        self.start = start
        self.end = end
        self.length = length
        self.map_area = map_area

    def __repr__(self):
        return '<Path %r>' % self.id

# The model saves how all the paths are connected
class Path_Connection(db.Model):
    __tablename__ = 'path_connections'
    id = db.Column('path_connection_id', db.Integer, primary_key=True)
    path1 = db.Column(db.Integer, db.ForeignKey('paths.path_id'), nullable=False)
    path2 = db.Column(db.Integer, db.ForeignKey('paths.path_id'), nullable=False)

    def __init__(self, path1=None, path2=None):
        self.path1 = path1
        self.path2 = path2

    def __repr__(self):
        return '<Path_Connection %r>' % self.id

# The model saves the path that each building is connected to
# and the area of the path to stop to get to the building
class Path_Building_Connection(db.Model):
    __tablename__ = 'path_building_connections'
    id = db.Column('path_building_connection_id', db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'), nullable=False)
    path = db.Column(db.Integer, db.ForeignKey('paths.path_id'), nullable=False)
    stop_node = db.Column(db.Integer, db.ForeignKey('nodes.node_id'), nullable=False)

    def __init__(self, building_id=None, path=None, stop_node=None):
        self.building_id = building_id
        self.path = path
        self.stop_node = stop_node

    def __repr__(self):
        return '<Path_Building_Connection %r>' % self.id


# This model defines all the starting point locations
# to the sci tech area
class Starting_Point(db.Model):
    __tablename__ = 'starting_points'
    id = db.Column('sp_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    latitude = db.Column(db.Numeric(9,6), nullable=False)
    longitude =  db.Column(db.Numeric(9,6), nullable=False)

    def __init__(self, name="unname", latitude=None, longitude=None):
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
    map_zone = db.Column(db.Integer, db.ForeignKey('map_zones.map_zone_id'))
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'))
    latitude = db.Column(db.Numeric(9,6), nullable=False)
    longitude =  db.Column(db.Numeric(9,6), nullable=False)

    def __init__(self, name="unname", object_name="unname", map_zone=None, building_id=None, latitude=None, longitude=None):
        self.name = name
        self.object_name = object_name
        self.map_zone = map_zone
        self.building_id = building_id
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Object_Detection_Object %r>' % self.id