#!/usr/bin/python3
"""first endpoint (route) will be to return the status of my API"""
import os
from flask import Flask
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.errorhandler(404)
def error_404(exception):
    return {"error": "Not found"}, 404


@app.errorhandler(404)
def not_found_error(error):
    """ returns a JSON-formatted 404 status code response """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_db(ctx):
    storage.close()


if os.getenv("HBNB_API_HOST"):
    host = os.getenv("HBNB_API_HOST")
else:
    host = "0.0.0.0"

if os.getenv("HBNB_API_PORT"):
    port = int(os.getenv("HBNB_API_PORT"))
else:
    port = 5000


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default=5000))
