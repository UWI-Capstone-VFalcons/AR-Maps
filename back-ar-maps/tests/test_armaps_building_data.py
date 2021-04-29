import os, sys

import os, sys
import pytest
import tempfile

# Allow python3 to make reference to package 
# outside the test directory
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from app import app
from app.models import *



def test_new_building():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    building = Building(name='lecture room 1', b_type='classroom', info='just a test room',latitude= 17.983453,longitude=-76.791344)
    assert building.name == 'lecture room 1'
    assert building.b_type == 'classroom'
    assert building.info == 'just a test room'
    assert building.latitude == 17.983453
    assert building.longitude == -76.791344