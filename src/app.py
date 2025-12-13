import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET', 'POST'])
def handle_members():
    
    if request.method == 'GET':
        all_family_members = jackson_family.get_all_members()
        return jsonify(all_family_members), 200
    
    if request.method == 'POST':
        new_member_data = request.get_json()

        jackson_family.add_member(new_member_data)
    
        return jsonify(new_member_data), 200

@app.route('/members/<int:member_id>', methods=['GET', 'DELETE'])
def handle_single_member(member_id):

    if request.method == 'GET':
        member_found = jackson_family.get_member(member_id)
        
        if member_found:
            return jsonify(member_found), 200
        else:
            return jsonify({"msg": "Member not found"}), 400

    if request.method == 'DELETE':
        did_delete = jackson_family.delete_member(member_id)
        
        if did_delete:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"msg": "Could not delete member"}), 400

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
