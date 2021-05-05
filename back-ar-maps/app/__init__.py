from flask import Flask
from flask_wtf.csrf import CSRFProtect 
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from flask_cors import CORS
import pymysql


app = Flask(__name__)


# Configurations

# flask-simple-geoip - get user current location
app.config.update(GEOIPIFY_API_KEY='at_Y4pp3IJV57Cz9cWhuFUPEHQRaFCXD')

# random string for secret
app.config['SECRET_KEY'] = "x9NgYaKf+&-Vr8rFN_e22UTX&GVS-T=bY5+k9p2uhQh6wTSZEPYdWD@58mWVC!Hg7*RNe*9eEW9cW&nugHzy2Y5fvAY4g@nK@=AN" 

#db confidg
# format (mysql://username:password@server/db)

# local databse 
app.config ['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://armaps:armaps@localhost/armaps"

# cloud database
# app.config ['SQLALCHEMY_DATABASE_URI'] = "postgresql://lhsqdwpcjxoewh:77ec8b70eb208802953747792eecea748a9c32faff7e9d27281e6b6f443553f2@ec2-3-91-127-228.compute-1.amazonaws.com:5432/d9gsa1neap28mn"  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # added just to suppress a warning

# files for storing
app.config['BUILDING_IMAGE_FOLDER'] = './app/static/images/building'
image_folder = app.config['BUILDING_IMAGE_FOLDER']

# add configuration to app
app.config.from_object(__name__)

# Setup db variable and CSRf token
db = SQLAlchemy(app)
csrf = CSRFProtect(app)  # used for forms and database

# qrcode setup
qrcode = QRcode(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Google API Keys
Google_API_Key = "AIzaSyB5QmIo_yG56_KI-WC91I1mmsyZ9cOZF9s"

# import the views for flask
from app import views, models