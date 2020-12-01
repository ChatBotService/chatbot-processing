from flask import Flask, render_template, request, redirect
# Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
# Models
from models.models import db, ma
from models.models import *

# APIs
from api.processing_api import ProcessingAPI

from util import processing

import os

print("Running...", flush=True)

app = Flask(__name__)
api = Api(app)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
app.config["DEBUG"] = True

# Database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db_env = os.environ.get("DB_PATH")
print(db_env)
db_uri = db_env
print("Database uri: ", flush=True)
print(db_uri, flush=True)



engine = create_engine(db_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db.init_app(app)
ma.init_app(app)

print("Initializing database...", flush=True)
# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     from models import models
#     models.init_db()

print("Database initialized", flush=True)

processing.init_sessionfactory(engine)

# APIs
api.add_resource(ProcessingAPI,"/processes", "/processes")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8083, debug=True, use_reloader=False)