#!/usr/bin/python3
"""first endpoint (route) will be to return the status of my API"""
import os
from flask import Flask
from api.v1.views import app_views
from models import storage
from models import *
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix="/api/v1")

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def error_404(exception):
    return {"error": "Not found"}, 404


@app.errorhandler(400)
def error_400(exception):
    message = exception.description
    return message, 400


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
    app.run(host=host, port=port, threaded=True)
