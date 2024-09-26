# app/routes.py
from flask import Blueprint, request

# create a blueprint for the API routes
api = Blueprint('api', __name__)

# ROUTES FROM API
# -----------------------------------------------------------
@api.route('/get_event_channel', methods=['POST'])
def get_event_channel():
    return {"message": "get_event_channel"}, 200

# -----------------------------------------------------------           
@api.route('/create_input', methods=['POST'])
def create_input():
    return {"message": "create_input"}, 200

# -----------------------------------------------------------
@api.route('/output_job', methods=['POST'])
def create_output():
    return {"message": "create_output"}, 200

# -----------------------------------------------------------
@api.route('/output_job', methods=['DELETE'])
def delete_output():
    return {"message": "delete_output"}, 200

# -----------------------------------------------------------
@api.route('/list_outputs', methods=['GET'])
def list_outputs():
    return {"message": "list_outputs"}, 200
        
# -----------------------------------------------------------
@api.route('/list_devices', methods=['GET'])
def list_devices():
    return {"message": "list_devices"}, 200