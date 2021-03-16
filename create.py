from flask import Flask, render_template, request
import os
# Import table definitions.
from models import *

app = Flask(__name__)

# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///audio.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)

def main():
  # Create tables based on each table definition in `models`
  db.create_all()

if __name__ == "__main__":
  # Allows for command line interaction with Flask application
  with app.app_context():
    main()