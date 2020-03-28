#!/usr/bin/env python3
import os
import sys
import configparser
from logging.config import dictConfig

import werkzeug

if not hasattr(werkzeug, "cached_property"):
    werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask, Blueprint
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy


fname = os.path.dirname(__file__)
sys.path.insert(0, fname)

config = configparser.ConfigParser()
config_filename = os.path.join(os.path.dirname(__file__), "../config.cfg")
config.read(config_filename)

#-------------------------------------------------------------------------------------#
# Logging
#-------------------------------------------------------------------------------------#

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

#-------------------------------------------------------------------------------------#
# Init Flask
#-------------------------------------------------------------------------------------#

app = Flask(__name__)
app.config["SECRET_KEY"] = config["general"].get("secret_key", "ispyb_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = config["general"]["db_uri"]
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SWAGGER_UI_JSONEDITOR"] = True

db = SQLAlchemy(app)
#-------------------------------------------------------------------------------------#
# Define api
#-------------------------------------------------------------------------------------#
authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "token"}}
blueprint = Blueprint('api', __name__, url_prefix='/ispyb/api/v1')
api = Api(
    blueprint,
    version="1.0",
    title="ISPyB",
    description="ISPyB Flask restplus server",
    doc="/doc",
    authorizations=authorizations,
    default="Main",
    default_label="Main",
)


#-------------------------------------------------------------------------------------#
# Register apis
#-------------------------------------------------------------------------------------#
from ispyb.apis.proposals import api as prop_api
from ispyb.apis.data_collections import api as dc_api

api.add_namespace(prop_api)
api.add_namespace(dc_api)

app.register_blueprint(blueprint, url_prefix='/ispyb/api/v1')

if __name__ == "__main__":
    app.run(debug=config["general"].get("debug_mode", False))
