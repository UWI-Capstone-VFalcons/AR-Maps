from app import app
from app.models import *
from app.forms import *
from app import db
import os, datetime
from flask import abort, jsonify, request, send_file, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import json
from app.forms import FindARDestinationForm
from app.models import Building
from app import qrcode

# create all uncreated databases 
db.create_all()

@app.route('/nav', methods=['GET'])
def ar():
    """Render camera with ar experience  <19/3/2021 N.Bedassie>"""
    form = FindARDestinationForm()
    if form.validate_on_submit() and request.method == 'GET':
        myLocation = request.form["myLocation"]
        myDestination = request.form["myDestination"]
       
        locationBuilding = Building.query.filter_by(name=myLocation).first()
        destinationBuilding = Building.query.filter_by(name=myDestination).first()
        print(locationBuilding.lattitude)
        print(destinationBuilding.lattitude)
        return render_template("map.html", form=form, locationBuilding=locationBuilding,destinationBuilding=destinationBuilding)
    return render_template("map.html",form=form)
    
@app.route('/ar-find/', methods=['GET'])
def ar_find():
    """Render camera with ar experience  <19/3/2021 N.Bedassie>"""
    return render_template("map.html")

@app.route('/api/test')
def home():
    return jsonify({"test":"Its working"})

@app.route('/api/buildingQR/<building_id>', methods=['GET'])
def building_qr(building_id):

    if (not isinstance(building_id, int) and not building_id.isnumeric()): abort(400)
    
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

    building = Building("test", "address1", "address2", "address3", "static/images/building/test.jpg", "b_type", "The Building info", 12.3456, 98.7654)
    db.session.add(building)
    db.session.commit()
     
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

# Jsonify the response and add it under the data field
def successResponse(message):
    return jsonify({'data':message})
    
# jsonify the response message with a error title
def errorResponse(message):
    return jsonify({'error':message})



# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port="5000")