#!/usr/bin/python3
"""contains endpoints(routes) for place objects"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from os import environ
from models import storage, CNC
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places_per_city(city_id=None):
    """
        places route to handle http method for requested places by city
    """
    city_object = storage.get('City', city_id)
    if city_object is None:
        abort(404, 'Not found')

    all_places = storage.all('Place')
    city_places = [obj.to_json() for obj in all_places.values()
                   if obj.city_id == city_id]
    return jsonify(city_places)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def places_per_city(city_id=None):
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    user_id = req_json.get("user_id")
    if user_id is None:
        abort(400, 'Missing user_id')
    user_object = storage.get('User', user_id)
    if user_object is None:
        abort(404, 'Not found')
    if req_json.get("name") is None:
        abort(400, 'Missing name')
    Place = CNC.get("Place")
    req_json['city_id'] = city_id
    new_object = Place(**req_json)
    new_object.save()
    return jsonify(new_object.to_json()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_with_id(place_id=None):
    """
        places route to handle http methods for given place
    """
    place_object = storage.get('Place', place_id)
    if place_object is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(place_object.to_json())

    if request.method == 'DELETE':
        place_object.delete()
        del place_object
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        place_object.bm_update(req_json)
        return jsonify(place_object.to_json()), 200
