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


@pytest.fixture
def client():
    app = armaps_app

    app.config["TESTING"] = True
    app.testing = True

    # This creates an in-memory sqlite db
    # See https://martin-thoma.com/sql-connection-strings/
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        # populate the temporary database with fake data
        db.create_all()
        ma1 = MapArea(
            name="Science & Technology Faculty",
            description="The science faculty of the Universiy of the west Indies",
            latitude_1= 18.003364,
            longitude_1= -76.749843,
            latitude_2= 18.005778,
            longitude_2= -76.751507, 
            latitude_3= 18.006836,
            longitude_3= -76.749104,
            latitude_4= 18.004963,
            longitude_4= -76.748221)

        db.session.add(ma1)
        db.session.commit()
    yield client


def test_getMapArea(client):
    map_area1 = getMapArea((18.004736, -76.749702))
    map_area2 = getMapArea((18.004039, -76.747125))
    map_area3 = getMapArea((18.004881, -76.749043))
    map_area4 = getMapArea((18.004074, -76.747291))

    assert not map_area1 == None
    assert     map_area2 == None
    assert not map_area3 == None
    assert     map_area4 == None