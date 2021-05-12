from flask_wtf.csrf import CSRFProtect

from app import app
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextField, SelectField

class FindARDestinationForm(FlaskForm):
    csrf = CSRFProtect(app)
    myLocation = TextField('Location', description = 'Enter Location', validators=[DataRequired()])
    myDestination = SelectField('Destination', description = 'Enter Description', validators=[DataRequired()])

