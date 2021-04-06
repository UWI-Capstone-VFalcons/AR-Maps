from flask_wtf.csrf import CSRFProtect

from app import app
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextField 

class FindARDestinationForm(FlaskForm):
    csrf = CSRFProtect(app)
    myLocation = TextField('Location', u'Enter Location', validators=[DataRequired()])
    myDestination = TextField('Destination', u'Enter Destination', validators=[DataRequired()])

