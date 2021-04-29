import os, sys
import pytest
import tempfile

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
#         db.create_all()
#     yield client


def test_getMapArea(client):
    map_area1 = getMapArea((18.004736, -76.749702))
    map_area2 = getMapArea((18.004039, -76.747125))
    map_area3 = getMapArea((18.004881, -76.749043))
    map_area4 = getMapArea((18.004074, -76.747291))

    assert not map_area1 == None
    assert     map_area2 == None
    assert not map_area3 == None
    assert     map_area4 == None