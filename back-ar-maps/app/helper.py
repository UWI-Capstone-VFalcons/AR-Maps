from app import db, Google_API_Key
from app.models import *
from shapely.geometry import Point, Polygon, MultiPoint
from shapely.ops import nearest_points
import numpy as np

# check any value enter if it is a number
def isNum( number ):
    try:
        float(number)
        return True
    except ValueError:
        return False

# calculate the shortent path between two coordinates
def calculateShortestPath(coord_a, coord_b):
    """
    Calculate the shortest path between two locations using the nodes scattered around the 
    area of interest.

    Parameters
        ----------
        coord_a : tuple/list
            the first pair of latitude and longitude (17.98321, -76.13138) or [17.13183, -77.13176]
        coord_b : tuple/list
            the second pair of latitube and longitude (17.98321, -76.13138) or [17.13183, -77.13176] 
    """

    # initialize graph
    g = {"a":coord_a, "b":coord_b} # 1:[[2,.0123]]
    nodes = db.session.query(Node).all()
    for node in nodes:
        break

# calculate the distance between two cordiates
def dist(coord_a, coord_b):
    """
    Calculate the straight line distance between two gps coordinates

    Parameters
        ----------
        coord_a : tuple/list
            the first pair of latitude and longitude (17.98321, -76.13138) or [17.13183, -77.13176]
        coord_b : tuple/list
            the second pair of latitube and longitude (17.98321, -76.13138) or [17.13183, -77.13176] 
    """
    return math.sqrt((coord_a[0] - coord_b[0])**2 + (coord_a[1] - coord_b[1])**2)

# check if a location is inside a map area and return the area ID
# coordinate is in the form (lat, longitude)
def getMapArea(coordinate):
    latitude = float(coordinate[0])
    longitude = float(coordinate[1])

    map_areas  = MapArea.query.all()

    for map_area in map_areas:

        map_area.latitude_1 = float(map_area.latitude_1)
        map_area.latitude_2 = float(map_area.latitude_2)
        map_area.latitude_3 = float(map_area.latitude_3)
        map_area.latitude_4 = float(map_area.latitude_4)

        map_area.longitude_1 = float(map_area.longitude_1)
        map_area.longitude_2 = float(map_area.longitude_2)
        map_area.longitude_3 = float(map_area.longitude_3)
        map_area.longitude_4 = float(map_area.longitude_4)

        map_area_fence = [
            (map_area.latitude_1, map_area.longitude_1),
            (map_area.latitude_2, map_area.longitude_2),
            (map_area.latitude_3, map_area.longitude_3),
            (map_area.latitude_4, map_area.longitude_4)
        ]

        map_area_polygon = Polygon(map_area_fence)

        coordinate_point = Point(latitude, longitude)

        if(coordinate_point.within(map_area_polygon)):
            return map_area
    return None

# get the closest path in a map area that 
# a point is close to
# coordinates are in the form (lat, lng)
def closestPath(map_area_id, coordinate):
    latitude = float(coordinate[0])
    longitude = float(coordinate[1])

    paths = Path.query.filter(Path.map_area == map_area_id).all()
    path_midpoints = []
    if(len(paths)>0):
        for path in paths:
            start_node = Node.query.get(path.start)
            end_node = Node.query.get(path.end)
            # generate the midpoint from each node
            start_mid = lineMidpoint(
                float(start_node.latitude_1), 
                float(start_node.latitude_2),
                float(start_node.longitude_1), 
                float(start_node.longitude_2))
            
            end_mid = lineMidpoint(
                float(end_node.latitude_1), 
                float(end_node.latitude_2),
                float(end_node.longitude_1), 
                float(end_node.longitude_2))

            # find the midpoint of the path
            path_midpoints.append(lineMidpoint(
                start_mid[0],
                end_mid[0], 
                start_mid[1], 
                end_mid[1]
                )
            )
        destin_paths = MultiPoint(path_midpoints)
        coordinate_point = Point(latitude, longitude)

        closest_point = nearest_points(coordinate_point, destin_paths)
        closest_point_index = path_midpoints.index(list(closest_point[1].coords)[0])
        
        return paths[closest_point_index]
    return None

# find the midpoint of two points 
def lineMidpoint(x1, x2, y1, y2):
    return ((x1 + x2) / 2,(y1 + y2) / 2)


# This would find the closest starting point relative to the user location
# and the destination. It would take the user location and destination id
# return the starting point that is best for the user
def closestStartingPoint(coordinate, destination_building_id, map_area_id):
    # try:
    latitude = float(coordinate[0])
    longitude = float(coordinate[1])
    # get the building and all the paths 
    destination_building = Building.query.get(destination_building_id)
    starting_points = Starting_Point.query.filter(Starting_Point.map_area == map_area_id).all()

    # create starting point and building destination midpoints
    if(len(starting_points) > 0 ):
        starting_point_destin_mid = []
        for starting_point in starting_points:
            starting_point_destin_mid.append(lineMidpoint(
                float(starting_point.latitude), 
                float(destination_building.latitude), 
                float(starting_point.longitude), 
                float(destination_building.longitude)
                )    
            )
        
        starting_mids = MultiPoint(starting_point_destin_mid)

        coordinate_point = Point(latitude, longitude)

        closest_point = nearest_points(coordinate_point, starting_mids)
        closest_point_index = starting_point_destin_mid.index(list(closest_point[1].coords)[0])
        print(closest_point[1])
        
        return starting_points[closest_point_index]
    # except:
    #     pass
    return None

# This method takes a list of paths in the order from start to finish
# It would then calculate the distance from the starting path to the ending path
# and the time base on the average walking speed of a person
# return the distance and the time as tuple (distance, time)
def calculatePathMetrix(list_of_path_to_take):
    pass

# This method gets the users map area,  starting path id and building destination
# it uses dijkstras algorthim to create the shortest path after creating the path structure
# The return value is a list of paths id in the order that the user should take
def generateShortestPath(start_path_id, destination_building_id):
    return []

