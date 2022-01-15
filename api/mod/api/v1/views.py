import os
from flask import request
import subprocess
from api import logging
from api import app, db
from flask import Blueprint
from datetime import datetime
from api.mod.packages.prettify import termcolor
from bson.json_util import dumps

collection = db["TextTechnology"]

logging.info(
    f"{termcolor.HEADER}Application running on {datetime.now().strftime('%Y-%m-%d::%H:%M')}{termcolor.ENDC}"
)

blueprint_agent = Blueprint(
    "agent", __name__, static_folder="static", static_url_path="/static/admin"
)


@blueprint_agent.route("/")
def hello():
    logging.debug("Call from the root url")
    return "<h1 style='color:blue'>Text Technology API!</h1>"


@blueprint_agent.route("/query")
def query_example():
    # if key doesn't exist, returns None
    key = request.args.get("query")
    value = request.args.get("target")
    print(key, value)
    query = {key: {"$regex": value, "$options": "i"}}
    logging.debug(f"query ready {query}")
    results = collection.find_one(query)
    # return True

    return f"""
    <h4>{results["title"]} </h4>
    <p>{results["author"]} </p>
    <p>{results["abstract"]} </p>
    """


@blueprint_agent.route("/nash")
def keyword_year():
    key = request.args.get("keyword")
    y = request.args.get("year")
    var = {key: {"$regex": y}}
    result = collection.find(var)
    return result
