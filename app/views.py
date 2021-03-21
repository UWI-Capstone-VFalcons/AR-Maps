from app import app 
from app.models import *
from app.forms import *
from . import db
import os, datetime
from flask import jsonify, request
from werkzeug.utils import secure_filename


@app.route('/')
def home():
    return {"test":"hello-world"}


# def shutdown_server():
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()


# @app.route('/shutdown', methods=['POST'])
# def shutdown():
#     shutdown_server()
#     return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")