# server/app/routes.py
from bson import ObjectId
from flask import Blueprint, json, jsonify, request, render_template
from controllers import device_manager, configuration_manager

# Create a blueprint for routes
api_dm = Blueprint('api', __name__, url_prefix='/api')

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# DEVICE MANAGER
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# GET /api/getdevicelist - Retrieves a list of devices
@api_dm.route('/getdevicelist', methods=['GET'])
def get_device_list():
    # Example device list
    devices = [
        {"id": 1, "name": "Device A"},
        {"id": 2, "name": "Device B"},
        {"id": 3, "name": "Device C"}
    ]
    return jsonify({"devices": devices}), 200

# POST /api/geteventchannel - Handles event channel retrieval
@api_dm.route('/geteventchannel', methods=['POST'])
def get_event_channel():
    # Example logic for event channel
    data = request.get_json()
    channel_id = data.get('channel_id')
    return jsonify({"message": f"Event channel {channel_id} retrieved successfully"}), 200

# POST /api/createinput - Handles creating input
@api_dm.route('/createinput', methods=['POST'])
def create_input():
    data = request.get_json()
    input_data = data.get('input_data')
    return jsonify({"message": "Input created successfully", "input_data": input_data}), 201

# GET /api/createoutput - Retrieves output
@api_dm.route('/createoutput', methods=['GET'])
def get_output():
    # Example logic to retrieve output
    output_id = request.args.get('output_id', 'default_id')  # Example of getting query parameters
    return jsonify({"message": f"Output {output_id} retrieved successfully"}), 200

# POST /api/createoutput - Creates output
@api_dm.route('/createoutput', methods=['POST'])
def create_output():
    data = request.get_json()
    output_data = data.get('output_data')
    return jsonify({"message": "Output created successfully", "output_data": output_data}), 201

# DELETE /api/createoutput - Deletes output
@api_dm.route('/createoutput', methods=['DELETE'])
def delete_output():
    data = request.get_json()
    output_id = data.get('output_id')
    return jsonify({"message": f"Output {output_id} deleted successfully"}), 200

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# CONFIGURATION MANAGER
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
@api_dm.route('/')
def configuration():
    return render_template('index.html')

# POST /device - Creates a new device
@api_dm.route('/config', methods=['POST'])
def create_device():
    try:
        data = request.get_json()
        
        return jsonify({"message": "Device created successfully", "device_id": configuration_manager.create_device(data)}), 201
    
    except ValueError as e:
        return jsonify({"error": e}), 404
    
# GET /device/<device_id> - Retrieves a device by its ID
@api_dm.route('/config/<device_id>', methods=['GET'])
def get_device(device_id):
    try:
        return jsonify(configuration_manager.get_device(device_id)), 200
    
    except ValueError as e:
        return jsonify({"error": e}), 404

# DELETE /device/<device_id> - Deletes a device
@api_dm.route('/config/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    success = configuration_manager.delete_device(device_id)
    if success:
        return jsonify({"message": "Device deleted successfully"}), 200
    return jsonify({"error": "Device not found"}), 404

# GET /devices - Retrieves the list of all devices
@api_dm.route('/config', methods=['GET'])
def list_devices():
    # try:
    devices = configuration_manager.list_devices()
    
    return jsonify(devices), 200

# GET /devices - Retrieves the list of all devices
@api_dm.route('/config', methods=['OPTIONS'])
def option_devices():
    response = jsonify()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response, 200
