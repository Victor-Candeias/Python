
from flask import Blueprint, request, jsonify
from controller.outputManager import output_job_controller
from controller.inputManager import input_job_controller
# from controller.websocket_manager import websocket_manager #, websocket_client

# Create a blueprint for the API routes
api = Blueprint('api', __name__)

# -----------------------------------------------------------
@api.route('/get_event_channel', methods=['POST'])
def get_event_channel():
    """
    Create event channel (websockect)

    Returns:
        string: returns the websockect URI
    """
    data = request.json
    machineid = data.get('machineid')
    sessionid = data.get('sessionid')
    filters = data.get('filters', [])
    
    if not machineid or not sessionid:
        return jsonify({'error': 'Machine ID and Session ID are required'}), 400

    websocket_uri = request.host_url # websocket_manager.add_client(sessionid, "", filters)

    return jsonify({'websocket_uri': websocket_uri})

# -----------------------------------------------------------           
@api.route('/create_input', methods=['POST'])
def create_input():
    """
    Create input data from plugin (scale, barcode) or external device

    Returns:
        json: return the result
    """
    data = request.json
    data = input_job_controller.create_input(data)
    
    return data

# -----------------------------------------------------------
@api.route('/output_job', methods=['POST'])
def create_output():
    """
    Define the route for creating an output job for receipt printers, label printers, etc.
    The output job could be synchronous or asynchronous
    receive a json
        {
        "machineid":"1",
        "sessionid":"1",
        "userinfo":"1",
        "ticket_id":"1",
        "type_of_job":"receipt",
        "job_mode":"synchronous",
        "date":"2024-08-24"
        }
    Returns:
        json string: return the job id.
    """
    data = request.json
    job_id = output_job_controller.add_job(data)
    return jsonify({"job_id": job_id})

# -----------------------------------------------------------
@api.route('/output_job', methods=['DELETE'])
def delete_output():
    """
    Define the route for deleting an output job

    Returns:
        json: return the result os the delete
    """
    data = request.json
    result = output_job_controller.delete_job(data)
    return jsonify({"result": result})

# -----------------------------------------------------------
@api.route('/output_jobs', methods=['GET'])
def list_outputs():
    """
    Define the route for listing all output jobs

    Returns:
        json: return the list of all output jobs
    """
    data = request.args.to_dict()  # Use query parameters for GET request
    jobs = output_job_controller.list_jobs(data)
    return jsonify(jobs)
        
# -----------------------------------------------------------
@api.route('/devices', methods=['GET'])
def devices():
    """
    Define the route for listing all devices

    Returns:
        json: return all input and output devices
    """
    devices_list = []
    
    # append output plugins
    devices_list.append(output_job_controller.list_all_plugins())
    
    # append input plugins
    devices_list.append(input_job_controller.list_all_plugins())
    
    return jsonify(devices_list)








# Why Use routes.py?
# Separation of Concerns:

# By placing all route definitions in routes.py, you separate the routing logic from the application initialization (which typically happens in app/__init__.py). This keeps your code clean and focused.
# Modularity:

# Using Blueprints in routes.py allows you to organize your application into modular components. This is particularly beneficial in larger applications where different parts of the application can be logically separated.
# Maintainability:

# Having a single file to manage routes makes it easier to update and maintain the routes in your application.