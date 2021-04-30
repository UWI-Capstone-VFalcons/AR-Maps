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
    lat1 = math.radians(coord_a[0])
    lat2 = math.radians(coord_a[0])
    lng1 = math.radians(coord_a[1])
    lng2 = math.radians(coord_b[1])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlng = lng2 - lng1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2)**2
 
    distance_radians = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers.
    r_earth = 6371
      
    # calculate the distane in kilometers
    return(distance_radians * r_earth)


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
    try:
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
            # print(closest_point[1])
            
            return starting_points[closest_point_index]
    except:
        pass
    return None

# This method takes a list of paths in the order from start to finish
# It would then calculate the distance from the starting path to the ending path
# and the time base on the average walking speed of a person
# return the distance and the time as tuple (distance, time)
def calculatePathMetrix(list_of_path_to_take):
    pass

# check the path that the coordinates is on, if any
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
        # print(path_fence)

        coordinate_point = Point(latitude, longitude)

        if(coordinate_point.within(path_polygon)):
            return paths[i]
        i += 1
    return None


# This method gets the users map area,  starting path id and building destination of type object
# it uses dijkstras algorthim to create the shortest path after creating the path structure
# The return value is a list of paths id in the order that the user should take
def generateShortestRoute(start_path_id, destination_building, map_area):
    # create graph from all the paths in the map area
    
    map_area_paths = Path.query.filter(Path.map_area == map_area).all()
    map_area_paths_connection = []
    for path in map_area_paths:
        pcs = Path_Connection.query.filter(Path_Connection.path1 == path.id)
        for pc in pcs:
            map_area_paths_connection.append((pc.path1, pc.path2))

    print(map_area_paths_connection)
    return []

"""
Calculate the shortest Route between two locations using the nodes scattered around the 
area of interest.

Parameters
    ----------
    user_coord : tuple/list
        the first pair of latitude and longitude (17.98321, -76.13138) or [17.13183, -77.13176]
    building_id : building object id 
        in the form of an integer
Return
   --------
   A tuple containing
    - starting path,
    - use starting point - a boolean to check if starting point would be used
    - best starting point
    - shortestRoute
"""
def shortestRoute(user_coord, building_id):
    # get the building and building map area
    starting_path = None
    best_starting_point = None
    use_starting_point =  False
    shortestRoute = []

    destin_building = Building.query.get(building_id)

    if(not destin_building == None):
        try:
            """
            First to try finding the best starting point to plan the route
            """
            destin_coordinate = (destin_building.latitude, destin_building.longitude)
            destin_building_map_area = getMapArea(destin_coordinate)
        
            # Check if the user is in any of the map area
            user_map_area = getMapArea(user_coord)
            
            if(not user_map_area == None):
                # check the path that the user is on if they are in a map are
                current_path = checkPath(user_coord, user_map_area.id)

                if(not current_path == None):
                    # use the path the user is on 
                    starting_path = current_path.id
                else:
                    # get the closest path to the user if the user is not on a path
                    user_closest_path = closestPath(user_map_area.id, user_coord)
                    starting_path = user_closest_path.id
            else:
                # if the user is not in one of the map areas, 
                # find the closest starting point for the map area of the destination
                use_starting_point = True
                best_starting_point = closestStartingPoint(user_coord, destination_id, destin_building_map_area.id)
                # get path connected to the starting point 
                PSPC = Path_Starting_Point_Connection.query.filter_by(starting_point_id=best_startign_point.id).first()
                starting_path = PSPC.path

            """
                Generate the shortest route to thedestination
            """
            shortestRoute = generateShortestRoute(starting_path, destin_building, destin_building_map_area.id)
            
            return (starting_path, use_starting_point, best_starting_point, shortestRoute)
        except:
            pass
    return None


    """
    1) we will need to get all data 
    - destination
    - current location
    - paths
    - paths connection
    - building path connectioon

2) check if the user is insde of a map area and return the map area *
    a) if the user is 
        1) check if the user is on a path -
            a) if they are then 
                - use their current location as he starting point for calulation
            b) if they are not 
                - find the closes path to the users ,
                then 
 find the closes path to the users ,
                then use that path statign point as the starting point for calculation
                
        continue to next step 
    b) if not 
        1) find the the closest starting relative to the destination and curentlocation -
            - find the middle point between each starting point and destination ,
             then find the the closest middle point to tghe use current location
        2) user google distance matirx api to get the dist
d
distance and time to the starting point *
        from the current user location
        3) continue to next step 
3) get the disatance, time and shortest path from the user's starting point to the destination - 
    """
