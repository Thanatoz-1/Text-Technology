import os
from api import logging
from flask import Blueprint
from datetime import datetime
from api.mod.packages.prettify import termcolor

logging.info(
    f"{termcolor.HEADER}Application running on {datetime.now().strftime('%Y-%m-%d::%H:%M')}{termcolor.ENDC}"
)

blueprint_agent = Blueprint(
    "agent", __name__, static_folder="static", static_url_path="/static/admin"
)


@blueprint_agent.route("/")
def hello():
    return "<h1 style='color:blue'>Text Technology API!</h1>"
