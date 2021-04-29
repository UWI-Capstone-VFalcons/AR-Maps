from app import db, Google_API_Key
from app.models import *
from shapely.geometry import Point, Polygon, MultiPoint
from shapely.ops import nearest_points
import numpy as np
import math

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

def checkPath(user_loc, map_area):
    """
        Parameters
        user_loc : tuple/list
            pair of latitude and longitude (17.98321, -76.13138) or [17.13183, -77.13176]
    """
    latitude = float(user_loc[0])
    longitude = float(user_loc[1])

    paths = Path.query.filter(Path.map_area==map_area).all()
    my_paths = []

    for path in paths:
        start = Node.query.filter_by(id=path.start).first()
        end = Node.query.filter_by(id=path.end).first()
        my_paths.append([start,end])

    i = 0
    for path in my_paths:  
        path[0].latitude_1 = float(path[0].latitude_1)
        path[0].latitude_2 = float(path[0].latitude_2)
        path[1].latitude_1 = float(path[1].latitude_1)
        path[1].latitude_2 = float(path[1].latitude_2)

        path[0].longitude_1 = float(path[0].longitude_1)
        path[0].longitude_2 = float(path[0].longitude_2)
        path[1].longitude_1 = float(path[1].longitude_1)
        path[1].longitude_2 = float(path[1].longitude_2)

        path_fence = [
            (path[0].latitude_1, path[0].longitude_1),
            (path[0].latitude_2, path[0].longitude_2),
            (path[1].latitude_1, path[1].longitude_1),
            (path[1].latitude_2, path[1].longitude_2)
        ]

        path_polygon = Polygon(path_fence)
        print(path_fence)

        coordinate_point = Point(latitude, longitude)

        if(coordinate_point.within(path_polygon)):
            return paths[i]
        i += 1
    return None