from app import db, Google_API_Key
from app.models import *
from shapely.geometry import Point, Polygon, MultiPoint
from shapely.ops import nearest_points
import math, requests
from datetime import datetime

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

    # Radius of earth in meters.
    r_earth = 6371000

    # error in reading
    val_error = 1.7
      
    # calculate the distane in meters
    return (distance_radians * r_earth)* val_error

# get straight line distance
def get_dist_straight(coord_a, coord_b):
    """
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

# calculate and add path length to database
def postPathLengths(map_area):
    """
        Populate paths with lengths in database
    """
    paths = Path.query.filter(Path.map_area==map_area).all()

    for path in paths:
        start = Node.query.filter_by(id=path.start).first()
        end = Node.query.filter_by(id=path.end).first()
        # get the length of the two side of the paths
        length_1 = dist(
            [float(start.latitude_1), 
            float(start.longitude_1)], 
            [float(end.latitude_1),
            float(end.longitude_1)])
        length_2 = dist(
            [float(start.latitude_2),
            float(start.longitude_2)], 
            [float(end.latitude_2),
            float(end.longitude_2)])
        # find the average of the two lengths 
        # and set it as the path length
        avg_length = (length_1 + length_2)/2
        path.length = avg_length
        print(avg_length)
    # save the changes to the database
    db.session.commit()

# This method gets the users map area,  starting path id and building destination of type object
# it uses dijkstras algorthim to create the shortest path after creating the path structure
# The return value is a list of paths id in the order that the user should take
def generateShortestRoute(start_path_id, destination_building_id, map_area):
    # create graph from all the paths in the map area
    # graph structure
    pathRoutes = {}
    allPaths_and_connections = {}
    pathsToVisit = []
    pathsToVisitLength = []
    pathsToVisitRoute = []

    vistedPaths = set([])
    unvistedPaths = set([])

    map_area_paths = Path.query.filter(Path.map_area == map_area).all()

    # check if any of the path lengths are missing and update them all before continueing
    for map_area_path in map_area_paths:
        if map_area_path.length == None:
            postPathLengths(map_area)
            map_area_paths = Path.query.filter(Path.map_area == map_area).all()
            break

    # create a list with all the path connections and their length
    for path in map_area_paths:
        pcs1 = Path_Connection.query.filter(Path_Connection.path1 == path.id).all()
        pcs2 = Path_Connection.query.filter(Path_Connection.path2 == path.id).all()

        connections = [float(path.length), set([])]
        for pc in pcs1:
            connections[1].add(pc.path2)

        for pc in pcs2:
            if not pc.path1 in connections[1]:
                connections[1].add(pc.path1)
        connections[1] = list(connections[1])
        unvistedPaths.add(path.id)
        # add the connections to the path 
        allPaths_and_connections[path.id]= connections

        # add all the path routes 
        pathRoutes[path.id]=[float('infinity'),[]]
    
    # add the starting point to the dictionarys
    allPaths_and_connections[0] = [0, [start_path_id]]
    pathRoutes[0]=[0,[]]


    # DIJKSTRA'S algorithm
    
    # set the first route that is connected to the starting point
    pathsToVisit += allPaths_and_connections[0][1]
    pathsToVisitLength += [ 0+ allPaths_and_connections[pathsToVisit[0]][0]]
    pathsToVisitRoute += [[pathsToVisit[0]]]
    prevPathVisited = [0]

    minimum_path_index = 0

    while(len(pathsToVisit)>0):
        # skip the path if the first is already visited
        if pathsToVisit[0] in unvistedPaths:

            # find the minimum path index
            minLength = float('infinity')
            for indx in range(len(pathsToVisit)):
                if(pathsToVisitLength[indx] < minLength):
                    minLength = pathsToVisitLength[indx]
                    minimum_path_index = indx

            # get the current path, prev path visited 
            # the current length and current route for the pathe
            # the current path would be the least expensive path
            prev_path = prevPathVisited.pop(minimum_path_index)
            current_path = pathsToVisit.pop(minimum_path_index)
            current_length = pathsToVisitLength.pop(minimum_path_index)
            current_route = pathsToVisitRoute.pop(minimum_path_index)

            if(current_path in unvistedPaths):
                vistedPaths.add(current_path) # add the current path to the visted list
                unvistedPaths.remove(current_path) # remove current path from the unvisited list

                # add the connecting paths and previous paths 
                # if the path is not visted by priority 
                # calculate the path lengths for each and plot the route
                for path_id in allPaths_and_connections[current_path][1]:
                    if(path_id in unvistedPaths):
                        pathsToVisit.append(path_id)
                        pathsToVisitLength.append(current_length +  allPaths_and_connections[path_id][0])
                        pathsToVisitRoute.append(current_route+[path_id])
                        prevPathVisited.append(current_path)

                # create the new route
                currentRoute = [current_length, current_route]

                # add the route if the previous route for the path 
                # is a greater cost 
                if(pathRoutes[current_path][0]>currentRoute[0]):
                    pathRoutes[current_path]= currentRoute

        else:
            # remove the duplicates
            prevPathVisited.pop(0)
            pathsToVisit.pop(0)

    # Find the path that the destination is connect to 
    # and return the route
    pbc = Path_Building_Connection.query.filter_by(building_id=destination_building_id).first()
    best_route_to_destination = pathRoutes[pbc.path]
    return best_route_to_destination

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
                best_starting_point = closestStartingPoint(user_coord, destin_building.id, destin_building_map_area.id)
                # get path connected to the starting point 
                PSPC = Path_Starting_Point_Connection.query.filter_by(starting_point_id=best_starting_point.id).first()
                starting_path = PSPC.path

            """
                Generate the shortest route to thedestination
            """
            shortestRoute = generateShortestRoute(starting_path, destin_building.id, destin_building_map_area.id)
            
            return (starting_path, use_starting_point, best_starting_point, shortestRoute)
        except:
            pass
    return None

def getPositions(start, end):
    interval = 0.000039 # about three meters
    positions = []
    start = [(float(start[0][0]), float(start[0][1])), (float(start[1][0]), float(start[1][1]))]
    end = [(float(end[0][0]), float(end[0][1])),(float(end[1][0]), float(end[1][1]))]
    dis_lat_1 = start[0][0] - end[0][0]
    dis_long_1 = start[0][1] - end[0][1]
    dis_lat_2 = start[1][0] - end[1][0]
    dis_long_2 = start[1][1] - end[1][1]

    # Latitude
    i = 0
    direct_1 = move(start[0][0], end[0][0])
    direct_2 = move(start[1][0], end[1][0])
    if end[0][0] < start[0][0]:
        #print(direct_1(start[0][0], interval*i))
        while direct_1(start[0][0], interval*i) > end[0][0] and direct_2(start[1][0], interval*i) > end[1][0]:
            # perhaps appending the average will give a good distance between the two nodes
            positions.append([(direct_1(start[0][0], interval*i) + direct_2(start[1][0], interval*i))/2])
            # positions.append([direct_2(start[1][0], interval*i)])
            i += 1
    else:
        while direct_1(start[0][0], interval*i) < end[0][0] and direct_2(start[1][0], interval*i) < end[1][0]:
            positions.append([(direct_1(start[0][0], interval*i) + direct_2(start[1][0], interval*i))/2])
            # positions.append([direct_2(start[1][0], interval*i)])
            i += 1
    
    # Need to account for overflow of longitude without a check
    # use interval binning
    interval = ((dis_long_1 + dis_long_2)/2)/float(i)
    #Longitude
    j = int(i)
    i = 0
    direct_1 = move(start[0][1], end[0][1])
    direct_2 = move(start[1][1], end[1][1])
    if end[0][1] < start[0][1]:
        #print(direct_1(start[0][0], interval*i))
        # while direct_1(start[0][0], interval*i) > end[0][0] and direct_2(start[1][0], interval*i) > end[1][0]:
        while i < j:
            positions[i].append((direct_1(start[0][1], interval*i) + direct_2(start[1][1], interval*i))/2)
            positions[i].append(i)
            # positions[i+1].append(direct_2(start[1][1], interval*i))
            if i != 0:
                positions[i].append(i-1)
            else:
                positions[i].append("camera")
            i += 1
    else:
        # while direct_1(start[0][0], interval*i) < end[0][0] and direct_2(start[1][0], interval*i) < end[1][0]:
        while i < j:
            positions[i].append((direct_1(start[0][1], interval*i) + direct_2(start[1][1], interval*i))/2)
            positions[i].append(i)
            # positions[i+1].append(direct_2(start[1][1], interval*i))
            if i != 0:
                positions[i].append(i-1)
            else:
                positions[i].append("camera")
            i += 1

    # # Latitude
    # i = 0
    # direct_1 = move(start[0][0], end[0][0])
    # direct_2 = move(start[1][0], end[1][0])
    # if end[0][0] < start[0][0]:
    #     #print(direct_1(start[0][0], interval*i))
    #     while direct_1(start[0][0], interval*i) > end[0][0] and direct_2(start[1][0], interval*i) > end[1][0]:
    #         # perhaps appending the average will give a good distance between the two nodes
    #         positions.append([direct_1(start[0][0], interval*i)])
    #         positions.append([direct_2(start[1][0], interval*i)])
    #         i += 1
    # else:
    #     while direct_1(start[0][0], interval*i) < end[0][0] and direct_2(start[1][0], interval*i) < end[1][0]:
    #         positions.append([direct_1(start[0][0], interval*i)])
    #         positions.append([direct_2(start[1][0], interval*i)])
    #         i += 1
    
    # # Need to account for overflow of longitude without a check
    # # use interval binning
    # interval = ((dis_long_1 + dis_long_2)/2)/float(i)
    # #Longitude
    # j = int(i)
    # i = 0
    # direct_1 = move(start[0][1], end[0][1])
    # direct_2 = move(start[1][1], end[1][1])
    # if end[0][1] < start[0][1]:
    #     #print(direct_1(start[0][0], interval*i))
    #     # while direct_1(start[0][0], interval*i) > end[0][0] and direct_2(start[1][0], interval*i) > end[1][0]:
    #     while i < j:
    #         positions[i].append(direct_1(start[0][1], interval*i))
    #         positions[i+1].append(direct_2(start[1][1], interval*i))
    #         i += 1
    # else:
    #     # while direct_1(start[0][0], interval*i) < end[0][0] and direct_2(start[1][0], interval*i) < end[1][0]:
    #     while i < j:
    #         positions[i].append(direct_1(start[0][1], interval*i))
    #         positions[i+1].append(direct_2(start[1][1], interval*i))
    #         i += 1
    return (len(positions),positions)

def absNeg(num):
    if num < 0:
        return num
    return -1*num

def move(start, end):
    if start <= end:
        return lambda x,y: x + y
    return lambda x,y: x - y

# get the distance and time between two coordiates 
# with one being a destination in a map area
# return the distance and time to reach the target
# the coordinate are in the form (lat, lng)
# the shortest route is a list with the routes in order
def estimateDistanceAndTime(cur_coord, dest_coord, starting_point, shortest_route):
    try:
        cur_lat = float(cur_coord[0])
        cur_lng = float(cur_coord[1])
        cur_coord = (cur_lat, cur_lng)

        dest_lat = float(dest_coord[0])
        dest_lng = float(dest_coord[1])
        dest_coord = (dest_lat, dest_lng)

        # initialize variables
        total_distance = 0
        total_time = 0
        track_start_path = None
        average_walking_speed = 1.31 # this value is in meters/second

        # if the route is empty 
        # assume the user is on the path connected to the destination
        # return the striaght line distance
        if(len(shortest_route) > 0):

            # check if the user is outside of a map area 
            # if the user is outside a map area get distance 
            # and time to the starting poing
            map_area = getMapArea(cur_coord)
            if(map_area == None):
                language = "en"
                unit="metric"
                mode ="walking"

                starting_point_lat = float(starting_point.latitude)
                starting_point_lng = float(starting_point.longitude)

                # try requesting information from api
                try:
                    request_link = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={},{}&destinations={},{}&mode={}&language={}&units={}&key={}\
                    ".format(
                        cur_lat,
                        cur_lng,
                        starting_point_lat,
                        starting_point_lng,
                        mode,
                        language,
                        unit,
                        Google_API_Key
                    )

                
                    response = requests.get( request_link)

                    json_result  = response.json()

                    if( json_result['rows'][0]["elements"][0]['status'] == "OK"):      
                        total_distance += json_result['rows'][0]["elements"][0]['distance']['value'] 
                        total_time += json_result['rows'][0]["elements"][0]['duration']['value']

                    # set the starting path to the first element in the route
                    track_start_path = shortest_route[0]

                except:
                    # exit the function and return all the values as  0 
                    # if an error occured while trying to fetch the metrix 
                    return {"distance":total_distance, "time":total_time}
            else:

                #find the best starting path to track from

                # check if the user is on a path 
                current_path = checkPath(cur_coord, map_area.id)
                if(current_path == None):
                    # if the user is not currently on a path fetch
                    #  the closest path to the user is on 
                    closest_path = closestPath(map_area.id, cur_coord)

                    # check if the closest path is in the routes list
                    # if it is not return the first element
                    if(closest_path.id in shortest_route):
                        track_start_path = closest_path.id
                    else:
                        track_start_path = shortest_route[0]
                else:
                    # get the total distance and time from 
                    # the persons current location until the end of their path
                    # if they are not on a pth in the list initalize the value to the first
                    if(current_path.id in shortest_route):
                        current_distance = 0
                        current_time = 0
                        routes = shortest_route[:]

                        for path_id in routes:
                            if(path_id == current_path.id):
                                # assummes that the user is trying to get to the end of the path
                                e_node = Node.query.get(current_path.end)
                                if(len(shortest_route)>1):
                                    current_distance += dist(cur_coord, (float(e_node.latitude_1), float(e_node.longitude_1)))
                                    shortest_route.pop(0)
                                    track_start_path= shortest_route[0]
                                else:
                                    current_distance += dist(cur_coord, dest_coord)
                                    shortest_route.pop(0)
                                    track_start_path= None
                                
                                # update the distance and time
                                current_time += current_distance/average_walking_speed
                                total_distance += current_distance
                                total_time += current_time
                                break
                            else:
                                shortest_route.pop(0) # romove the element to prevent loss in processing time rechecking
                    else:
                        track_start_path = shortest_route[0]
            
            # use the starting point to the last path in the route to
            # get the distance and time
            internal_distance = 0
            internal_time = 0
            start_checking = False

            if(not track_start_path == None):
                for path_id in shortest_route:
                    if start_checking :
                        path = Path.query.get(path_id)
                        internal_distance += float(path.length)
                    else:
                        if path_id == track_start_path:
                            start_checking = True
                            path = Path.query.get(path_id)
                            internal_distance += float(path.length)
                
            # calculate the total time
            internal_time = internal_distance/average_walking_speed

            # add internal to total
            total_distance += internal_distance
            total_time += internal_time    
        else:
            # get the straight line distance
            distance = dist(cur_coord, dest_coord)
            time = distance/average_walking_speed
            total_distance += distance
            total_time += time

        return {"distance":total_distance, "time":total_time}
    except:
        pass
    return {"distance":0, "time":0}

# check if the user is in close proximity to the destination
# return True if it is in close proximity
# return false if it is out of bound
def checkCurrentAndDestination(cur_coord, dest_id):
    try:
        cur_lat = float(cur_coord[0])
        cur_lng = float(cur_coord[1])

        destin_building = Building.query.get(dest_id)
        destin_coordinate = (float(destin_building.latitude), float(destin_building.longitude))

        # enter the value for meters around the building
        # that will be used to validate if the person is
        # at the destination
        radius_meter = 25
        cordinate_per_meter = 0.000006555
        radius = radius_meter * cordinate_per_meter
        
        #create the circle polygon 
        destination_circle = Point(destin_coordinate[0], destin_coordinate[1]).buffer(radius)
        destination_circle_polygon = Polygon(destination_circle)

        coordinate_point = Point(cur_lat, cur_lng)

        if(coordinate_point.within(destination_circle_polygon)):
            return True
    except:
        pass
    return False

# check if a location is inside a map zone and return the zone ID
# coordinate is in the form (lat, longitude)
def getMapZone(coordinate, mapArea_id):
    latitude = float(coordinate[0])
    longitude = float(coordinate[1])

    map_zones  = MapZone.query.filter_by(map_area=mapArea_id).all()

    for map_zone in map_zones:

        map_zone.latitude_1 = float(map_zone.latitude_1)
        map_zone.latitude_2 = float(map_zone.latitude_2)
        map_zone.latitude_3 = float(map_zone.latitude_3)
        map_zone.latitude_4 = float(map_zone.latitude_4)

        map_zone.longitude_1 = float(map_zone.longitude_1)
        map_zone.longitude_2 = float(map_zone.longitude_2)
        map_zone.longitude_3 = float(map_zone.longitude_3)
        map_zone.longitude_4 = float(map_zone.longitude_4)

        map_zone_fence = [
            (map_zone.latitude_1, map_zone.longitude_1),
            (map_zone.latitude_2, map_zone.longitude_2),
            (map_zone.latitude_3, map_zone.longitude_3),
            (map_zone.latitude_4, map_zone.longitude_4)
        ]

        map_zone_polygon = Polygon(map_zone_fence)

        coordinate_point = Point(latitude, longitude)

        if(coordinate_point.within(map_zone_polygon)):
            return map_zone
    return None

# check to ensure a time is in range
# return a boolean if the time is
#  in range of the start and end
def time_in_range(start, end, time):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= time <= end
    else:
        return start <= time or time <= end