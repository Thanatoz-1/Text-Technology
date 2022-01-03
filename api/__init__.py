import os
import logging
from flask import Flask
from api.mod.packages.dbconnect import Connector
import pymongo

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_url_path="/static")

if app.config.get("ENV") == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config.get("ENV") == "testing":
    app.config.from_object("config.TestingConfig")
elif app.config.get("ENV") == "development":
    app.config.from_object("config.DevelopmentConfig")

try:
    client = pymongo.MongoClient(os.environ.get("URL"))
    db = client[os.environ.get("DB_NAME")]
except Exception as e:
    logging.critical(f"Error connecting to Database {e}")

from api.mod.api.v1.views import blueprint_agent

app.register_blueprint(blueprint_agent, url_prefix="/app/v1")
