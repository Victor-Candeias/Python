import importlib
import logging
import os
import uuid
import threading
from queue import Queue
from flask import Blueprint, request, jsonify
from controller.plugin_registry import PluginRegistry
from controller.utilities import Utilities

class InputJobController:
    def __init__(self):
        self.jobs = {}  # Armazena jobs com seu status
        self.logger = logging.getLogger(__name__)

        # plugins directory
        self.pluginsDirectory = os.path.join(os.path.dirname(__file__), 'plugins')

        # Registrar todos os plugins
        self.plugins = Utilities.registerPlugins(self.pluginsDirectory, self.logger, "inputManager")

        self.logger.info(f"_register_all_plugins();input plugin count {len(self.plugins)}")

        # Stop all plugin job processing
        for plugin in self.plugins.values():
            plugin.start()

    def create_input(self, data):
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

        from controller.websocket_manager.websocket_client import WebSocketClient

        # Send data to WebSocket
        # Create a WebSocketClient instance
        client = WebSocketClient(request.host_url)  # Replace with your server URL
        
        # Connect to the server with session ID and filters
        client.connect(session_id=sessionid, filters=[input_type])
        
        client.send_message(message)
        

        # Keep the client running to listen for events
        client.keep_running()
        #client.disconnect()

        # return result
        return jsonify({'status': 'success', 'message': 'Input data sent to WebSocket clients'}), 200

    # def add_job(self, data):
    #     self.logger.info(f"add_job();data {data}")
    #     self.logger.info(f"add_job();Job type {data['type_of_job']}")

    #     job_id = str(uuid.uuid4())
    #     job = {**data, "status": "queued", "job_id": job_id}

    #     self.logger.info(f"add_job();Job {job}")

    #     self.jobs[job_id] = job
    #     self.job_queue.put(job)  # Adiciona o job à fila

    #     return {"message": "Job accepted", "job_id": job_id}

    def stop(self):
        # Stop all plugin job processing
        for plugin in self.plugins.values():
            plugin.stop()
        # Stop the worker thread
        self.job_queue.put(None)
        self.worker_thread.join()
        
    def list_all_plugins(self):
        result = []
        
        for plugin in self.plugins:
            result.append(str(plugin))
            
            self.logger.info(f"list_all_plugins();input plugin {plugin}")
            
        return {'input': result}
