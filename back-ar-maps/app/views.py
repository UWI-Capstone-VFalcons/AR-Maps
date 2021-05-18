import os, datetime, sys, traceback
from flask import abort, jsonify, request, send_file, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import json, math, requests
from app import app, qrcode, Google_API_Key, image_folder, csrf
from app.models import *
from app.forms import *
from app.helper import *
from app.my_encoders import *


"""

    Routes
  **********

"""

@app.route('/', methods=['GET'])
def defHome():
    return redirect(url_for("home"))

@app.route('/nav', methods=['GET','POST'])
def ar():
    """Render camera with ar experience  <19/3/2021 N.Bedassie>"""
    # check if the response is a post request
    # send the data if it is
    if request.method == 'POST':
        data = request.form["data"]
    else:
        data={
            "destination":1,
            "gps_error":{
                "lat":0,
                "lng":0
                },
            "zone_id":None
        }
        data = json.dumps(data)
        
    #  continue adding form for everything else 
    form = FindARDestinationForm()
    buildings = Building.query.all()
    form.myDestination.choices = ([(b.id, b.name) for b in buildings])
    return render_template("ar_directions.html",form=form, buildings=buildings, data=data)

@app.route('/nav/OD/detect', methods=['GET','POST'])
def od_orientation():  
    data = {}
    # check if its a post request and send the data
    if request.method == 'POST':
        data=request.form["data"]
    return render_template("od_orientation.html", data=data)

"""
    API EndPOints
"""

@app.route('/nav/to/<float:des_lat>/<float:des_long>', methods=['GET'])
def ar_find():
    """Render camera with ar experience  <19/3/2021 N.Bedassie>"""
    return render_template("ar_directions.html")


"""
    
    API EndPoints
  ******************

"""

@app.route('/api/test')
def home():
    return jsonify({"test":"Its working"})

"""
    Building
"""

@app.route('/api/buildingQR/<building_id>', methods=['GET'])
def building_qr(building_id):
    
    building = Building.query.get(building_id)
    if(not building is None):
        # ceate the dictionary with the building data
        qrcode_data = {
            'qrType':'building',
            'building_id':building.id,
            'building_name':building.name,
            'building_type':building.b_type,
            'building_address1': building.address1,
            'building_address2': building.address2,
            'building_address3': building.address3,
            'building_image': image_folder+building.image_url,
            'building_latittude': building.latitude,
            'building_longitude':building.longitude,
            'building_info': building.info 
        }

        qrcode_data = json.dumps(qrcode_data, cls=DecimalEncoder)

        return send_file(qrcode(qrcode_data,  box_size=20, border=3, mode="raw"), mimetype="image/png")
    return errorResponse("no such building found")

@app.route('/api/building/<building_id>', methods=['GET'])
def get_building(building_id):
     
    if (not isinstance(building_id, int) and not building_id.isnumeric()): abort(400)
    
    building = Building.query.get(building_id)
    if(not building is None):
        # ceate the dictionary with the building data
        qrcode_data = {
            'building_id':building.id,
            'building_name':building.name,
            'building_type':building.b_type,
            'building_address1': building.address1,
            'building_address2': building.address2,
            'building_address3': building.address3,
            'building_image': building.image_url,
            'building_latittude': building.latitude,
            'building_longitude':building.longitude,
            'building_info': building.info 
        }

        return successResponse(qrcode_data)
    return errorResponse("no such building found")


"""
    Event
"""
@app.route('/api/event/current/<building_id>', methods=['GET'])
def get_current_event(building_id):
    if(not isNum(building_id)): return errorResponse("The building id must be a number")
    try:
        des_building_id = int(building_id)

        response = []
        
        # get the current time 
        now = datetime.now()

        current_time = now.time()
        today_date = now.date()
        current_day_of_week = today_date.weekday()

        current_events = Event.query.filter(Event.building_id == building_id ).all()

        for event in current_events:
            if(time_in_range(event.start_time, event.end_time, current_time) 
                and ((event.recurrent == True and event.day_of_week == current_day_of_week))
                    or (event.recurrent == False and event.specific_date == today_date)):
                response.append({
                    'building_id': building_id,
                    'event_id': event.id,
                    'building_event_name': event.name,
                    'building_event_start_time': event.start_time.strftime("%I:%M:%p"),
                    'building_event_end_time': event.end_time.strftime("%I:%M:%p"),
                    'building_event_info': event.info
                })
                break
        return successResponse(response)
    except:
        pass
    return errorResponse("Error occured, report to the admin")

"""
    Current Location
"""
@app.route('/api/location_name/<cur_latitude>,<cur_longitude>', methods=['GET'])
def get_location_name(cur_latitude, cur_longitude):
    if(not isNum(cur_latitude) or not isNum(cur_longitude)):  return errorResponse("coordinates are not numbers")
    
    location_name = "Unname Location"
    cur_longitude = float(cur_longitude)
    cur_latitude = float(cur_latitude)
    # check if the user is inside of a map area
    location_map_area =  getMapArea((cur_latitude,cur_longitude))
    
    if(not location_map_area  == None):
        # find the path in the map area found that is closest
        # to the coordinate
        closest_path = closestPath(location_map_area.id, (cur_latitude, cur_longitude))
        if(not closest_path == None):
            location_name = closest_path.name +" path"
        return successResponse({"name":location_name})
        
    else:
        # if the location is outside of a map area get the location name from google
        try:
            # Get the nearest road the location is attached to 
            nearest_road_link = "https://roads.googleapis.com/v1/nearestRoads?points={},{}&key={}\
            ".format(
                cur_latitude,
                cur_longitude,
                Google_API_Key
            )
            nearest_road_response = requests.get(nearest_road_link)
            if(not nearest_road_response.json() == {}):
                nearest_road_placeid = nearest_road_response.json()["snappedPoints"][0]["placeId"]
                
                # Get the place ID address information 
                loc_address_link = "https://maps.googleapis.com/maps/api/geocode/json?place_id={}&language={}&key={}\
                ".format(
                    nearest_road_placeid,
                    "en",
                    Google_API_Key
                )
                loc_address_response = requests.get(loc_address_link)
                loc_address_result  = loc_address_response.json()

                loc_address_result = loc_address_result["results"][0]["address_components"]

                if(loc_address_result[0]["long_name"]== "Unnamed Road"):
                    location_name = loc_address_result[1]["short_name"]+", "+loc_address_result[3]["short_name"]
                else:
                    location_name = loc_address_result[0]["short_name"]+" "+loc_address_result[1]["short_name"]+", "+loc_address_result[3]["short_name"]
            else:
                # Get the place ID address information 
                loc_address_link = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&language={}&key={}\
                ".format(
                    cur_latitude,
                    cur_longitude,
                    "en",
                    Google_API_Key
                )
                loc_address_response = requests.get(loc_address_link)
                loc_address_result  = loc_address_response.json()
                if(len(loc_address_result["results"]) > 0):
                    loc_address_result = loc_address_result["results"][0]["address_components"]

                    if(loc_address_result[0]["long_name"]== "Unnamed Road"):
                        location_name = loc_address_result[1]["short_name"]+", "+loc_address_result[3]["short_name"]
                    else:
                        location_name = loc_address_result[0]["short_name"]+" "+loc_address_result[1]["short_name"]+", "+loc_address_result[3]["short_name"]


            return successResponse({"name":location_name})
        except:
            e = sys.exc_info()[0]
            print(e)
            return errorResponse("Fail to connect to API or Error occured ")
    return successResponse("no address or name available for location")


"""
    Destinations
"""

@app.route('/api/destinations', methods=['GET'])
def get_all_destinations():

    # building = Building("test2", "address1", "address2", "address3", "static/images/building/test.jpg", "b_type", "The Building info", 12.3556, 98.7654)
    # db.session.add(building)
    # db.session.commit()
         
    buildings = Building.query.all()
   
    # list for all the buidlings 
    allBuildings = []

    if len(buildings) > 0:
        for building in buildings:
            qrcode_data = {}
            if(not building is None):
                # ceate the dictionary with the building data
                qrcode_data = {
                    'building_id':building.id,
                    'building_name':building.name,
                    'building_type':building.b_type,
                    'building_address1': building.address1,
                    'building_address2': building.address2,
                    'building_address3': building.address3,
                    'building_image': building.image_url,
                    'building_latittude': building.latitude,
                    'building_longitude':building.longitude,
                    'building_info': building.info 
                }
            allBuildings.append(qrcode_data)
        return successResponse(allBuildings)
    return successResponse("no destinations found")

@app.route('/api/closest/destination/<cur_latitude>,<cur_longitude>', methods=['GET'])
def get_closest_destinations(cur_latitude, cur_longitude):

    # building = Building("test2", "address1", "address2", "address3", "static/images/building/test.jpg", "b_type", "The Building info", 12.3556, 98.7654)
    # db.session.add(building)
    # db.session.commit()
    if(not isNum(cur_latitude) or not isNum(cur_longitude)):  return errorResponse("coordinates are not nuumber")

    cur_longitude = float(cur_longitude)
    cur_latitude = float(cur_latitude)

    buildings = Building.query.filter((
    ( (Building.latitude <= cur_latitude+0.2) & (Building.latitude >= cur_latitude-0.2) ) &
    ( (Building.longitude <= cur_longitude+0.2) & (Building.longitude >= cur_longitude-0.2) )
    )).all()

    # list for all the buidlings 
    allBuildings = []


    if len(buildings) > 0:
        for building in buildings:
            qrcode_data = {}
            if(not building is None):
                # ceate the dictionary with the building data
                qrcode_data = {
                    'building_id':building.id,
                    'building_name':building.name,
                    'building_type':building.b_type,
                    'building_address1': building.address1,
                    'building_address2': building.address2,
                    'building_address3': building.address3,
                    'building_image': building.image_url,
                    'building_latittude': building.latitude,
                    'building_longitude':building.longitude,
                    'building_info': building.info 
                }
            allBuildings.append(qrcode_data)
        return successResponse(allBuildings)
    return errorResponse("no destinations found")

@app.route('/api/destination/estimate/(<cur_latitude>,<cur_longitude>)&<des_building_id>&<starting_point_id>&<route>', methods=['GET'])
def get_destinations_estimates(cur_latitude, cur_longitude, des_building_id, starting_point_id, route):
    if(not isNum(cur_latitude) or not isNum(cur_longitude) or not isNum(des_building_id) or not isNum(starting_point_id) or not type(route) == str): return errorResponse("Invalid parameters")

    cur_longitude = float(cur_longitude)
    cur_latitude = float(cur_latitude)
    cur_coord = (cur_latitude,cur_longitude)

    des_building_id = int(des_building_id)
    starting_point_id = int(starting_point_id)

    try:
        route = [int(x) for x in route.split(',')]
        estimates = "Bad Response"

        building = Building.query.get(des_building_id)
        dest_coord = (float(building.latitude),float(building.longitude))

        sp = Starting_Point.query.get(starting_point_id)
        metrix = estimateDistanceAndTime(cur_coord, dest_coord, sp, route)

        estimates = metrix
        
        return successResponse(estimates)
    except:
        return errorResponse("Fail to connect to API or Error occured")
    return successResponse("no metrix available")

@app.route('/api/arrive/destinations/(<cur_latitude>,<cur_longitude>)/<des_building_id>', methods=['GET'])
def get_reach_destination(cur_latitude, cur_longitude, des_building_id):
    if(not isNum(cur_latitude) or not isNum(cur_longitude) or not isNum(des_building_id)): return errorResponse("Invalid parameters")
    
    cur_longitude = float(cur_longitude)
    cur_latitude = float(cur_latitude)
    cur_coord = (cur_latitude,cur_longitude)

    des_building_id = int(des_building_id)
    try:
        response = checkCurrentAndDestination(cur_coord, des_building_id)
        return successResponse(response)
    except:
        return errorResponse("Error occured, report to the admin")
    return errorResponse("Something went wrong!")

"""
    Paths
"""

@app.route('/api/paths', methods=['GET'])
def get_all_paths():
    all_paths_json = []
    map_paths = Path().query.all()

    if len(map_paths) > 0:
        for map_path in map_paths:
            startNode = Node.query.get(map_path.start)
            endNode = Node.query.get(map_path.end)
            json_path = {
                'id': map_path.id,
                'name': map_path.name,
                'description': map_path.description,
                'start_latitude_1': startNode.latitude_1,
                'start_longitude_1': startNode.longitude_1,
                'start_latitude_2': startNode.latitude_2,
                'start_longitude_2': startNode.longitude_2,
                'end_latitude_1': endNode.latitude_1,
                'end_longitude_1': endNode.longitude_1,
                'end_latitude_2': endNode.latitude_2,
                'end_longitude_2': endNode.longitude_2,
            }
            all_paths_json.append(json_path)
        return successResponse(all_paths_json)
    # return if no path was found
    return successResponse("no paths were found")

@app.route('/api/shortest_paths/overheadMap/<destination_id>&(<cur_latitude>,<cur_longitude>)', methods=['GET'])
def get_shortest_path_overhead(cur_latitude, cur_longitude, destination_id):    
    if(not isNum(cur_latitude) or not isNum(cur_longitude) or not isNum(destination_id)):  return errorResponse("All parameters must be numeric")

    # convert the variables 
    cur_longitude = float(cur_longitude)
    cur_latitude = float(cur_latitude)
    cur_coordinate = (cur_latitude, cur_longitude)
    shortest_path_response = {}

    try:
        destination_id = int(destination_id)
        building = Building.query.get(destination_id)
        dest_coord = (float(building.latitude),float(building.longitude))

        shortestPathDetail = shortestRoute(cur_coordinate, destination_id)
        
        metrics = estimateDistanceAndTime(cur_coordinate, dest_coord, shortestPathDetail[2], shortestPathDetail[3][1])

        # create dictionary for ouput
        shortest_path_response = {
            "starting_path":shortestPathDetail[0],
            "use_starting_point": shortestPathDetail[1],
            "route": shortestPathDetail[3][1]
        }

        # add starting point if neessary
        if(shortestPathDetail[1]):
            starting_point = shortestPathDetail[2]
            starting_point_lat = float(starting_point.latitude)
            starting_point_lng = float(starting_point.longitude)
            shortest_path_response["starting_point_latitude"] = starting_point_lat
            shortest_path_response["starting_point_longitude"] = starting_point_lng

        # add metrics
        if not metrics == None:
            shortest_path_response["metrics"] = metrics

        # add boolean if user reach their destintion
        if(checkCurrentAndDestination(cur_coordinate, destination_id)):
            shortest_path_response["reach_destination"] = True
        else:
            shortest_path_response["reach_destination"] = False
        return successResponse(shortest_path_response)
    except:
        return errorResponse("Error occured, report to the admin")
    return errorResponse("Invalid Request, destination not valid")

@app.route('/api/shortest_paths/ar/<destination_id>/<cur_latitude>/<cur_longitude>', methods=['GET'])
def get_shortest_path_ar(cur_latitude, cur_longitude, destination_id):
    """
        Get each path in the route e.g.[1,2,3]
        Starting point would be first point
        Case 1:
            When you are outside of Scitech,
            Get total distance and time -> Phillip
            In JSON, return the starting point.
            then Jump to Case 2.
        Case 2:    
            For each path inside of Scitech, 
            Write a function that will take distance between 3D objects and a path
            Create evenly spaced GPS points between them. (based on the distance points)
            Use it to generate each point for each path.
            Wrap in JSON and return it.
    """
    if(not isNum(cur_latitude) or not isNum(cur_longitude) or not isNum(destination_id)):
        return errorResponse("All parameters must be numeric")

    # convert the variables 
    cur_longitude = float(cur_longitude)
    cur_latitude = float(cur_latitude)
    cur_coordinate = (cur_latitude, cur_longitude)
    
    try:
        route = shortestRoute(cur_coordinate, destination_id) 
        # returns tuple with 4 values (starting_path, use_starting_point, best_starting_point, shortest route)
        dest = Building.query.get(destination_id)
        dest_coord = (float(dest.latitude), float(dest.longitude))
        meta = None
        if route[1]: # get distance and time
            meta = estimateDistanceAndTime(cur_coordinate, dest_coord, route[2], route[3][1])
            print(meta)
        paths = []
        positions = [] # 3D objects placed 2 meters apart(just randomly chosen)
        for pid in route[3][1]:
            paths.append(Path.query.get(pid))
        for path in paths:
            start = Node.query.filter_by(id=path.start).first()
            end = Node.query.filter_by(id=path.end).first()
            result = getPositions([(start.latitude_1, start.longitude_1), (start.latitude_2,start.longitude_2)], [(end.latitude_1, end.longitude_1),(end.latitude_2, end.longitude_2)])
            positions.append(result)
            # print(result, path, paths)
        if(meta):
            return successResponse({"positions":positions, "meta": meta})
        return successResponse({"positions":positions})
    except Exception:
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        return errorResponse("Error occured, report to the admin")
    return errorResponse("Invalid Request, destination not valid")

"""
    Zone
"""
@app.route('/api/zone/<cur_latitude>/<cur_longitude>', methods=['GET'])
def get_zone(cur_latitude, cur_longitude):
    # return 
    #   - the mapzone id and name that the user is in currently
    #   - object ids, name, latitude and longitude in the form of a list of
    #        dictionaries eg[{"object_name":--,"object_id:--", "object_lat": ---, "object_lng":---}, {"object_name":--,"object_id:--"}]
    #  eg return resutlt {"zone_id":---, "zone_name":---, [list of objects above]}
    if not isNum(cur_latitude) or not isNum(cur_longitude):
        return errorResponse("All parameters must be numeric")

    # convert the variables 
    cur_longitude = float(cur_longitude)
    cur_latitude = float(cur_latitude)
    cur_coordinate = (cur_latitude, cur_longitude)

    try:
        map_area = getMapArea(cur_coordinate)
        if(map_area):
            zone = getMapZone(cur_coordinate, map_area.id)
            if(zone == None):
                return errorResponse2("User is not in a zone", 404)
        else:
            return errorResponse2("User outside of map area", 404)
        objs = OD_Objects.query.filter_by(map_zone=zone.id).all()
        objects = [{"object_name":obj.name,
                    "object_digital_name":obj.object_name,
                    "object_id":obj.id,
                    "object_lat":obj.latitude,
                    "object_lng":obj.longitude} for obj in objs]
        return successResponse({"zone_id":zone.id, "zone_name":zone.name, "objects":objects})
    except Exception:
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        return errorResponse("Error occured, report to the admin")
    return errorResponse2("Invalid Request, destination not valid", 400)

@app.route('/api/obj/<int:obj_id>', methods=['GET'])
def od_object(obj_id):
    obj = OD_Objects.query.filter_by(id=obj_id).first()
    if obj:
        object = {
            "name": obj.name,
            "id": obj.id,
            "latitude": obj.latitude,
            "longitude": obj.longitude,
            "map_zone": obj.map_zone,
            "building_id": obj.building_id
        }
        return successResponse({"object":object})
    return errorResponse2("Object not Found", 404)


"""
    responses
"""
# Jsonify the response and add it under the data field
def successResponse(message):
    return jsonify({'data':message}), 200
    
# jsonify the response message with a error title
def errorResponse(message):
    return jsonify({'error':message})

# jsonify the response message with a error title and code
def errorResponse2(message, code):
    return json.dumps({'error':message}), code

# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port="5000")
