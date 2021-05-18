from app import db
from app.models import *
from app.helper import *
import datetime



"""
EVENT
"""

# add event
def addEvent(building_id=None, name="Custom Event", start_time=datetime.time(0, 0, 0), end_time=datetime.time(23, 59, 59), 
    recurrent=True, day_of_week=1, specific_date=None, info="Some information about the custom event"):
    try:
        event = Event(
            building_id=building_id, 
            name=name,
            start_time=start_time,
            end_time=end_time,
            recurrent=recurrent,
            day_of_week=day_of_week,
            specific_date=specific_date,
            info=info)
        db.session.add(event)
        db.session.commit()
    except:
        pass

"""
MAP AREA
"""

# add map area
def addMapArea(name="AREA", description = "Map AREA", coord_1 = (None, None), coord_2 = (None, None), coord_3 = (None, None), coord_4 = (None, None)):
    try:
        ma = MapArea(
            name=name,
            description= description,
            latitude_1= coord_1[0],
            longitude_1= coord_1[1],
            latitude_2= coord_2[0],
            longitude_2= coord_2[1], 
            latitude_3= coord_3[0],
            longitude_3= coord_3[1],
            latitude_4= coord_4[0],
            longitude_4= coord_4[1])

        db.session.add(ma)
        db.session.commit()
    except:
        pass

"""
MAP ZONE
"""

# add map zone
def addMapZone(name="AREA", map_area = None, coord_1 = (None, None), coord_2 = (None, None), coord_3 = (None, None), coord_4 = (None, None)):
    try:
        mz = MapZone(
            name=name,
            map_area=map_area,
            latitude_1= coord_1[0],
            longitude_1= coord_1[1],
            latitude_2= coord_2[0],
            longitude_2= coord_2[1], 
            latitude_3= coord_3[0],
            longitude_3= coord_3[1],
            latitude_4= coord_4[0],
            longitude_4= coord_4[1])
        db.session.add(mz)
        db.session.commit()
    except:
        pass

"""
BUILDING
"""

# add building
def addBuilding(name="unname", address1=None, address2=None, address3=None, image_url="default_building.jpg", b_type="Lecture Theatre", info="no imformation added", 
    coord = (None, None), connected_path = 1, stop_node_coord1 = (None, None), stop_node_coord2 = (None, None)):
    try:
        b = Building(
            name=name,
            address1=address1, 
            address2=address2,
            address3=address3,
            image_url=image_url, 
            b_type=b_type, 
            info=info,
            latitude=coord[0],
            longitude=coord[1])
        db.session.add(b)
        db.session.commit()

        # add new node 
        stop_node = Node(
            description="building_"+name+"_stop_node",
            latitude_1= stop_node_coord1[0],
            longitude_1= stop_node_coord1[1],
            latitude_2= stop_node_coord2[0],
            longitude_2= stop_node_coord2[1])
        db.session.add(stop_node)
        db.session.commit()

        # add the path building connection
        pbc = Path_Building_Connection(
            building_id=b.id,
            path=connected_path,
            stop_node=stop_node.id)
        db.session.add(pbc)
        db.session.commit()

    except:
        pass

"""
PATH
"""

# add path
def addPath(name = "unname", start_node_coord1 = (None, None), start_node_coord2 = (None, None), end_node_coord1 = (None, None), end_node_coord2 = (None, None),
    connected_path=None, map_area_id=1, use_connected_path_end_for_start = False):
    try:
        # add the nodes
        start_node = None
        if(use_connected_path_end_for_start):
            connected_path_object = Path.query.get(connected_path)
            start_node = Node.query.get(connected_path_object.end)
        else:
            start_node = Node(
                description="path_"+name+"_start_node",
                latitude_1= start_node_coord1[0],
                longitude_1= start_node_coord1[1],
                latitude_2= start_node_coord2[0],
                longitude_2= start_node_coord2[1])
            db.session.add(start_node)

        end_node = Node(
            description="path_"+name+"_end_node",
            latitude_1= end_node_coord1[0],
            longitude_1= end_node_coord1[1],
            latitude_2= end_node_coord2[0],
            longitude_2= end_node_coord2[1])
        db.session.add(end_node)
        db.session.commit()

        # calculate the length of the path 
        path_length = calculatePathLength(start_node, end_node)

        # add the path 
        path = Path(
            name=name,
            start=start_node.id,
            end=end_node.id,
            length= path_length,
            map_area=map_area_id)
        db.session.add(path)
        db.session.commit()

        # add the path connection if necessary
        if(not connected_path == None):
            pc = Path_Connection(
                path1=path.id,
                path2=connected_path)
            db.session.add(pc)
            db.session.commit()
    except:
        pass

"""
STARTING POINT
"""

# add the starting point
def addStartingPoint(name="unname", map_area_id=1, coord= (None, None), connected_path = 1):
    try:
        sp = Starting_Point(
            name= name, 
            map_area=map_area_id,
            latitude= coord[0], 
            longitude= coord[1])
        db.session.add(sp)
        db.session.commit()

        # add path to starting point connection
        sppc = Path_Starting_Point_Connection(
            starting_point_id= sp.id,
            path= connected_path)
        db.session.add(sppc)
        db.session.commit()

    except:
        pass

"""
OD OBJECTS
"""

# add od objects
def add_OD_Objects(name="unname", object_name="unname", map_zone=None, building_id=None, coord = (None, None)):
    try:
        odo = OD_Objects(
                name=name, 
                object_name=object_name, 
                map_zone=map_zone,
                building_id=building_id,
                latitude=coord[0], 
                longitude=coord[1])
        db.session.add(odo)
        db.session.commit()
    except:
        pass