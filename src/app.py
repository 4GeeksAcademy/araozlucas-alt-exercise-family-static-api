"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson") # Create the jackson family object


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def members():
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return response_body, 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    response_body = {}
    response_body['message'] = 'Datos del integrante de la familia'
    response_body['results'] = jackson_family.get_member(member_id)
    if response_body['results']:
        return response_body, 200
    response_body['message'] = 'Error en la peticion, id fuera de rango'
    return response_body, 400


@app.route('/members', methods=['POST'])
def add_member():
    response_body = request.get_json()
    add = jackson_family.add_member(response_body)
    return add, 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    delete_member = jackson_family.delete_member(member_id)
    return delete_member, 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
