from app import db, Google_API_Key
from app.models import *

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
    latitude = coordinate[0]
    longitude = coordinate[1]

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

        area_rectangle = 0.5 * abs(
        #   y_A                          y_C                   x_D                   x_B
        (map_area.longitude_1 - map_area.longitude_3) * (map_area.latitude_4 - map_area.latitude_2)
        #    y_B                     y_D                        x_A                  x_C
        + (map_area.longitude_2 - map_area.longitude_4) * (map_area.latitude_1 - map_area.latitude_3)
        )

        triangle1 = 0.5 * abs(
        latitude * (map_area.longitude_1 - map_area.longitude_4)
        + map_area.latitude_1 * (map_area.longitude_4 - longitude)
        + map_area.latitude_4 * (longitude - map_area.longitude_1)
        )

        triangle2 = 0.5 * abs(
        latitude * (map_area.longitude_4 - map_area.longitude_3)
        + map_area.latitude_4 * (map_area.longitude_3 - longitude)
        + map_area.latitude_3 * (longitude - map_area.longitude_4)
        )

        triangle3 = 0.5 * abs(
        latitude * (map_area.longitude_3 - map_area.longitude_2)
        + map_area.latitude_3 * (map_area.longitude_2 - longitude)
        + map_area.latitude_2 * (longitude - map_area.longitude_3)
        )

        triangle4 = 0.5 * abs(
        latitude * (map_area.longitude_2 - map_area.longitude_1)
        + map_area.latitude_2 * (map_area.longitude_1 - longitude)
        + map_area.latitude_1 * (longitude - map_area.longitude_2)
        )

        added_area = (triangle1 + triangle2 + triangle3 + triangle4)

        if(area_rectangle < added_area):
            return map_area

    return None
