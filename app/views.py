from app import app 
from app.models import *
from app.forms import *
from app import db
import os, datetime
from flask import abort, jsonify, request, send_file
from werkzeug.utils import secure_filename

from app import qrcode



@app.route('/')
def home():
    return jsonify({"test":"Its working"})

@app.route('/api/buildingQR/<building_id>', methods=['GET'])
def building_qr(building_id):
 
    if (not isinstance(building_id, int) and not building_id.isnumeric()): abort(400)
    
    building = Building.query.get(building_id)
    if(not building is None):
        # ceate the dictionary with the building data
        qrcode_data = {
            'building_id':building.id,
            'building_name':building.name,
            'building_type':building.b_type,
            'building_latittude':building.lattitude,
            'building_longitude':building.longitude,
            'building_info': building.info 
        }

        return send_file(qrcode(qrcode_data, mode="raw"), mimetype="image/png")
    return errorResponse("no such building found")

# Jsonify the response and add it under the data field
def successResponse(message):
    return jsonify({'data':message})
# jsonify the response message with a error title
def errorResponse(message):
    return jsonify({'error':message})


# def shutdown_server():
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()


# @app.route('/shutdown', methods=['POST'])
# def shutdown():
#     shutdown_server()
#     return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")