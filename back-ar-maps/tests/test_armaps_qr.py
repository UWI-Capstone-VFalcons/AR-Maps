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


def test_qr_generation(client):
    api_result = client.get("/api/buildingQR/1")
    assert api_result.status_code == 200