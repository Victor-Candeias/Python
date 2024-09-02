from flask import Blueprint, jsonify, request
from app import input_manager
from app.input_manager import InputManager
from app.utils import WriteLog

# Define the blueprint for API routes
api = Blueprint('api', __name__)

# In-memory data stores
output_jobs = []
devices = [
    {"id": "1", "name": "Device 1", "type": "camera", "status": "online"},
    {"id": "2", "name": "Device 2", "type": "microphone", "status": "offline"}
]
event_channel = {
    "channelId": "12345",
    "name": "Main Event Channel",
    "url": "http://example.com/event-channel",
    "status": "active"
}

def init_routes(app):
    app.register_blueprint(api)

def generate_id(collection):
    return str(len(collection) + 1)

# create output job
@api.route('/output-jobs', methods=['POST'])
def create_output_job():
    data = request.json
    
    WriteLog(data)
    
    if not data or not 'name' in data or not 'source' in data or not 'destination' in data:
        return jsonify({"error": "Invalid input"}), 400

    new_job = {
        "id": generate_id(output_jobs),
        "name": data['name'],
        "type": data.get('type', 'video'),
        "source": data['source'],
        "destination": data['destination'],
        "status": data.get('status', 'pending'),
        "createdAt": "2024-08-21T12:34:56Z"
    }
    output_jobs.append(new_job)
    return jsonify(new_job), 201

# delete output job
@api.route('/output-jobs/<string:job_id>', methods=['DELETE'])
def delete_output_job(job_id):
    global output_jobs
    output_jobs = [job for job in output_jobs if job['id'] != job_id]
    return jsonify({"message": "Output job deleted successfully"}), 200

# list output job
@api.route('/output-jobs', methods=['GET'])
def list_output_jobs():
    return jsonify(output_jobs), 200

# get event channel
@api.route('/get-event-channel', methods=['GET'])
def get_event_channel():
    return jsonify(event_channel), 200

# create input
@api.route('/inputs/<string:plugin_type>', methods=['POST'])
def create_input(plugin_type):
    data = request.json
    try:
        new_input = input_manager.process_input(plugin_type, data)
    except ValueError as e:
        return jsonify({"error": str(e)})

# list all devices
@api.route('/devices', methods=['GET'])
def list_devices():
    return jsonify(devices), 200
