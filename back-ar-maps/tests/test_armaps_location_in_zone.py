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



def test_getMapZone(client):
    map_zone1 = getMapZone((18.005591, -76.748636), 1)
    map_zone2 = getMapZone((18.005159, -76.747934), 1)
    map_zone3 = getMapZone((18.005101, -76.749596), 1)
    map_zone4 = getMapZone((18.004561, -76.750288), 1)

    assert not map_zone1 == None
    assert     map_zone2 == None
    assert not map_zone3 == None
    assert     map_zone4 == None