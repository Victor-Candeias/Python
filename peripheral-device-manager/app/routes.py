# Purpose of app/routes.py
# Define API Endpoints:

# The primary role of app/routes.py is to define the different routes that your Flask application will serve. Each route corresponds to a specific URL and is associated with a view function that handles requests to that URL.
# Organize Application Logic:

# By separating route definitions into routes.py, you keep your application organized. It helps in managing the different parts of the application by grouping related routes together.
# Handle HTTP Methods:

# Each route in routes.py can handle different HTTP methods (e.g., GET, POST, PUT, DELETE), allowing your application to support various types of operations like retrieving data, submitting forms, updating records, or deleting resources.
# Use Blueprints for Modular Design:

# In larger applications, routes.py may use Flask Blueprints to modularize the routes. Blueprints allow you to group related routes together, making the application easier to maintain and extend.

from flask import Blueprint, request, jsonify
from controller import output_job_controller
from controller import input_job_controller
from controller.device_controller import list_all_devices, create_input_job
from app.websocket_manager import ws_manager
from flask_sock import Sock

# Create a blueprint for the API routes
api = Blueprint('api', __name__)
sock = Sock()

# Create event channel
@api.route('/get_event_channel', methods=['POST'])
def get_event_channel():
    data = request.json
    machineid = data.get('machineid')
    sessionid = data.get('sessionid')
    filters = data.get('filters', [])

    if not machineid or not sessionid:
        return jsonify({'error': 'Machine ID and Session ID are required'}), 400

    ws_manager.register_client(sessionid)
    ws_manager.set_filters(sessionid, filters)
    
    websocket_uri = f"ws://{request.host}/ws/{sessionid}"
    
    # assicia
    ws_manager.associate_websocket(client_id=sessionid, ws=websocket_uri)
    
    return jsonify({'websocket_uri': websocket_uri})

# Rota WebSocket para o cliente
@sock.route('/ws/<sessionid>')
def ws_handler(ws, sessionid):
    ws_manager.associate_websocket(sessionid, ws)

    try:
        while True:
            data = ws.receive()
            if data is None:
                break

            # Exemplo de processamento: verificar se é um comando de broadcast
            if data.startswith('broadcast:'):
                # Envia mensagem para todos os clientes conectados
                message_to_broadcast = data.split('broadcast:', 1)[1].strip()
                ws_manager.broadcast_message("broadcast", message_to_broadcast)
            else:
                # Caso contrário, envia a mensagem apenas para o cliente atual
                ws_manager.send_message(sessionid, "response", f"Received: {data}")

    except Exception as e:
        print(f"WebSocket connection with client {sessionid} closed with error: {e}")
    finally:
        ws_manager.remove_connection(sessionid, ws)

# Create input             
@api.route('/create_input', methods=['POST'])
def create_input():
    data = request.json
    machineid = data.get('machineid')
    sessionid = data.get('sessionid')
    input_type = data.get('input_type')  # Ex: "scale" ou "barcode"
    value = data.get('value')  # Dados do input (peso, código de barras, etc.)
    extra_data = data.get('extra_data', {})  # Dados adicionais

    if not machineid or not sessionid or not input_type or not value:
        return jsonify({'error': 'Machine ID, Session ID, Input Type, and Input Data are required'}), 400

    # Constrói a mensagem a ser enviada
    message = {
        'machineid': machineid,
        'input_type': input_type,
        'value': value,
        'extra_data': extra_data
    }

    # Envia a mensagem via WebSocket para todos os clientes conectados com o sessionid especificado
    ws_manager.send_message(sessionid, "input_data", message)

    return jsonify({'status': 'success', 'message': 'Input data sent to WebSocket clients'}), 200

# Define the route for creating an output job
@api.route('/output_job', methods=['POST'])
def create_output():
    data = request.json
    job_id = output_job_controller.add_job(data)
    return jsonify({"job_id": job_id})

# Define the route for deleting an output job
@api.route('/output_job', methods=['DELETE'])
def delete_output():
    data = request.json
    result = output_job_controller.delete_job(data)
    return jsonify({"result": result})

# Define the route for listing all output jobs
@api.route('/output_jobs', methods=['GET'])
def list_outputs():
    data = request.args.to_dict()  # Use query parameters for GET request
    jobs = output_job_controller.list_jobs(data)
    return jsonify(jobs)
        
# Define the route for listing all devices
@api.route('/devices', methods=['GET'])
def devices():
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