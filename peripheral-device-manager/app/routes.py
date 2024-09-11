
from flask import Blueprint, request, jsonify
from controller.outputManager import output_job_controller
from controller.inputManager import input_job_controller
from messages import Messages

# create a blueprint for the API routes
api = Blueprint('api', __name__)

# -----------------------------------------------------------
@api.route('/get_event_channel', methods=['POST'])
def get_event_channel():
    """
    create event channel (websocket)
    
        Returns:
            string: returns the websocket URI
    """
    data = request.json
    machineId = data.get('machineId')
    sessionId = data.get('sessionId')
    
    if not machineId or not sessionId:
        return jsonify({"error": Messages._instance.ROUTES_MACHINE_ID_ERROR}), Messages._instance.STATUS_RESULT_ERROR

    websocket_uri = request.host_url

    # return the websocket uri
    return jsonify({'websocket_uri': websocket_uri})

# -----------------------------------------------------------           
@api.route('/create_input', methods=['POST'])
def create_input():
    """
    create input data from plugin (scale, barcode) or external device

    Returns:
        json: return the result
    """
    data = request.json
    data = input_job_controller.create_input(data, request.host_url)
    
    return data

# -----------------------------------------------------------
@api.route('/output_job', methods=['POST'])
def create_output():
    """
    define the route for creating an output job for receipt printers, label printers, etc.
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
    job_id = output_job_controller.add_job(data, request.host_url)
    return jsonify({"job_id": job_id})

# -----------------------------------------------------------
@api.route('/output_job', methods=['DELETE'])
def delete_output():
    """
    define the route for deleting an output job

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
    define the route for listing all output jobs

    Returns:
        json: return the list of all output jobs
    """
    
    # use query parameters for GET request
    data = request.args.to_dict()  
    jobs = output_job_controller.list_jobs(data)
    return jsonify(jobs)
        
# -----------------------------------------------------------
@api.route('/devices', methods=['GET'])
def devices():
    """
    define the route for listing all devices

    Returns:
        json: return all input and output devices
    """
    devices_list = []
    
    # append output plugins
    devices_list.append(output_job_controller.list_all_plugins())
    
    # append input plugins
    devices_list.append(input_job_controller.list_all_plugins())
    
    return jsonify(devices_list)