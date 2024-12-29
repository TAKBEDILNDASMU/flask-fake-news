from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize flask app
app = Flask(__name__)

# Load Configuration
app.config.from_object('config')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

from app import routes, models
