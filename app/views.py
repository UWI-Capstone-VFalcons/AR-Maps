from app import app 
from app import models
from app import forms
from flask import render_template, request, redirect, url_for, flash


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")