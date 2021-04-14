from flask_wtf.csrf import CSRFProtect

from app import app
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextField 

class FindARDestinationForm(FlaskForm):
    csrf = CSRFProtect(app)
    myLocation = TextField('My Location', description = 'Enter Location', validators=[DataRequired()])
    myDestination = TextField('Destination', description = 'Enter Description', validators=[DataRequired()])

