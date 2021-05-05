import requests
import os, datetime
from flask import abort, jsonify, request, send_file, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
<<<<<<< HEAD
import json
from app.forms import FindARDestinationForm
from app.models import Building, Node
from app import qrcode
from flask import jsonify
from flask_simple_geoip import SimpleGeoIP
=======
import json,math
from app import app, db, qrcode, Google_API_Key
from app.models import *
from app.forms import *
from app.helper import *

"""
    Routes
"""
@app.route('/', methods=['GET'])
def defHome():
    return redirect(url_for("home"))
>>>>>>> ARview


# Initialize the extension
simple_geoip = SimpleGeoIP(app)

@app.route('/nav', methods=['GET'])
def ar():
    """Render camera with ar experience  <19/3/2021 N.Bedassie>"""
    # currentLocation = fetchCurrentLocation()
    form = FindARDestinationForm()
    if form.validate_on_submit() and request.method == 'GET':
        myDestination = request.form["myDestination"]
       
        locationBuilding = Building.query.filter_by(name=myLocation).first()
        destinationBuilding = Building.query.filter_by(name=myDestination).first()
        
        return render_template("map.html", form=form, locationBuilding=locationBuilding,destinationBuilding=destinationBuilding)
    buildings = db.session.query(Building).all()
    nodes = db.session.query(Node).all()
    node_list = []
    for node in nodes:
        node_list.append(vars(node))
    node_len = len(node_list)
    for i in range(node_len):
        if i == 0:
            node_list[i]["look_at"] = "[gps-camera]"
        else:
            node_list[i]["look_at"] = "#node-" + str(node_list[i-1]['id'])
    return render_template("map.html",form=form, buildings=buildings, nodes=nodes)

@app.route('/nav/OD/orientation', methods=['GET'])
def od_orientation():
    return render_template("od_orientation.html")

"""
    API EndPOints
"""

@app.route('/ar-find/', methods=['GET'])
def ar_find():
    """Render camera with ar experience  <19/3/2021 N.Bedassie>"""
    return render_template("map.html")

@app.route('/api/test')
def home():
    return jsonify({"test":"Its working"})

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
            'building_image': building.image_url,
            # 'building_latittude': building.lattitude,
            # 'building_longitude':building.longitude,
            'building_latittude': 'lt98.7654',
            'building_longitude':'lg12.3456',
            'building_info': building.info 
        }

        qrcode_data = json.dumps(qrcode_data)

        return send_file(qrcode(qrcode_data,  box_size=20, border=3, mode="raw"), mimetype="image/png")
    return errorResponse("no such building found")

@app.route('/api/building/<building_id>', methods=['GET'])
def get_building(building_id):

    # building = Building("test", "address1", "address2", "address3", "static/images/building/test.jpg", "b_type", "The Building info", 12.3456, 98.7654)
    # db.session.add(building)
    # db.session.commit()
     
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
            # 'building_latittude': building.lattitude,
            # 'building_longitude':building.longitude,
            'building_latittude': 'lt98.7654',
            'building_longitude':'lg12.3456',
            'building_info': building.info 
        }

        return successResponse(qrcode_data)
    return errorResponse("no such building found")

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
                    # 'building_latittude': building.lattitude,
                    # 'building_longitude':building.longitude,
                    'building_latittude': 'lt98.7654',
                    'building_longitude':'lg12.3456',
                    'building_info': building.info 
                }
            allBuildings.append(qrcode_data)
        return successResponse(allBuildings)
    return errorResponse("no destinations found")

@app.route('/api/closest/destination/<cur_latitude>,<cur_longitude>', methods=['GET'])
def get_closest_destinations(cur_latitude, cur_longitude):

    # building = Building("test2", "address1", "address2", "address3", "static/images/building/test.jpg", "b_type", "The Building info", 12.3556, 98.7654)
    # db.session.add(building)
    # db.session.commit()
    if(not isNum(cur_latitude) or not isNum(cur_longitude)):  abort(400)

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
                    # 'building_latittude': building.lattitude,
                    # 'building_longitude':building.longitude,
                    'building_latittude': 'lt98.7654',
                    'building_longitude':'lg12.3456',
                    'building_info': building.info 
                }
            allBuildings.append(qrcode_data)
        return successResponse(allBuildings)
    return errorResponse("no destinations found")

@app.route('/api/destination/estimate/(<cur_latitude>,<cur_longitude>)(<dest_latitude>,<dest_longitude>)', methods=['GET'])
def get_destimations_estimates(cur_latitude, cur_longitude, dest_latitude, dest_longitude):
    if(not isNum(cur_latitude) or not isNum(cur_longitude) or not isNum(dest_latitude) or not isNum(dest_longitude)): return errorResponse("Invalid parameters")

    cur_longitude = float(cur_longitude)
    cur_latitude = float(cur_latitude)
    dest_longitude = float(dest_longitude)
    dest_latitude = float(dest_latitude)
    language = "en"
    unit="metric"
    mode ="walking"

    # try requesting information from api
    try:
        request_link = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={},{}&destinations={},{}&mode={}&language={}&units={}&key={}\
        ".format(
            cur_latitude,
            cur_longitude,
            dest_latitude,
            dest_longitude,
            mode,
            language,
            unit,
            Google_API_Key
        )

     
        response = requests.get( request_link)

        json_result  = response.json()

        estimates = "Bad Response"

        if( json_result['rows'][0]["elements"][0]['status'] == "OK"):         
            estimates = {
                "distance": json_result['rows'][0]["elements"][0]['distance']['value'],
                "time": json_result['rows'][0]["elements"][0]['duration']['value']
                }
        
        return successResponse(estimates)
    except:
        return errorResponse("Fail to connect to API or Error occured")
    return errorResponse("no metrix available")


# Jsonify the response and add it under the data field
def successResponse(message):
    return jsonify({'data':message})
    
# jsonify the response message with a error title
def errorResponse(message):
    return jsonify({'error':message})


<<<<<<< HEAD
def fetchCurrentLocation():
    # Retrieve geoip data for the given requester
    geoip_data = simple_geoip.get_geoip_data()

    return jsonify(data=geoip_data)
=======
# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port="5000")
>>>>>>> ARview
