import os, sys
import pytest
import tempfile
import json, math, ast

# Allow python3 to make reference to package 
# outside the test directory
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from app import app as armaps_app
from app.models import *
from app.helper import *

from test_armaps_populate_test_db import client


# @pytest.fixture
# def client():
#     app = armaps_app

#     app.config["TESTING"] = True
#     app.testing = True

#     # This creates an in-memory sqlite db
#     # See https://martin-thoma.com/sql-connection-strings/
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

#     client = app.test_client()
#     with app.app_context():
#          db.create_all()
#     yield client


def test_getClosestLocation(client):
    loc_name_1 = client.get("/api/location_name/18.004736,-76.749702")
    loc_name_closest_Path_1 = closestPath(1, (18.004736, -76.749702))
    
    loc_name_1_res = ast.literal_eval(loc_name_1.data.decode("UTF-8"))
    
    assert loc_name_1.status_code == 200
    assert loc_name_1_res["data"]["name"] == loc_name_closest_Path_1.name + " path"

    # location 2
    loc_name_2 = client.get("/api/location_name/18.004881,-76.749043")
    loc_name_closest_Path_2 = closestPath(1, (18.004881, -76.749043))
    
    loc_name_2_res = ast.literal_eval(loc_name_2.data.decode("UTF-8"))
    
    assert loc_name_2.status_code == 200
    assert loc_name_2_res["data"]["name"] == loc_name_closest_Path_2.name + " path"

    # location 3
    loc_name_3 = client.get("/api/location_name/18.004039,-76.747125")

    loc_name_3_res = ast.literal_eval(loc_name_3.data.decode("UTF-8"))
    
    assert loc_name_3.status_code == 200
    assert loc_name_3_res["data"]["name"] == "Sherlock Drive Kingston, JM"