import importlib
import logging
import os
import uuid
import threading
from queue import Queue
from flask import Blueprint, request, jsonify
from controller.plugin_registry import PluginRegistry
from controller.utilities import Utilities
from config import Config
from messages import Messages

class InputJobController:
    def __init__(self):
        """
        initialize the class
        """
        # stores all jobs
        self.jobs = {}  
        self.logger = logging.getLogger(__name__)

        # plugins directory
        self.pluginsDirectory = os.path.join(os.path.dirname(__file__), 'plugins')

        # register all plugins
        self.plugins = Utilities.registerPlugins(self.pluginsDirectory, self.logger, "inputManager")

        self.logger.info(f"_register_all_plugins();input plugin count {len(self.plugins)}")

        # start all plugin job processing
        # in the input manager all plugins are listening to events from the devices
        for plugin in self.plugins.values():
            plugin.start()

    def create_input(self, data, serverUrl):
        data = request.json
        machineId = data.get('machineId')
        sessionId = data.get('sessionId')
        inputType = data.get('inputType')
        value = data.get('value')
        extraData = data.get('extraData', {})

        if not machineId or not sessionId or not inputType or not value:
            return jsonify({'error': 'Machine ID, Session ID, Input Type, and Input Data are required'}), 400

        # builds the message to be sent
        message = {
            'machineId': machineId,
            'input_type': inputType,
            'value': value,
            'extra_data': extraData
        }

        from controller.utilities import Utilities
        
        resultStatus = Messages._instance.STATUS_RESULT_OK
        
        try:
            Utilities.sendDataToClients(serverUrl, sessionId=sessionId, inputType=inputType, message=message)
        except:
            resultStatus = Messages._instance.STATUS_RESULT_ERROR

        # return result
        return jsonify({'status': 'success', 'message': 'Input data sent to WebSocket clients'}), resultStatus

    def stop(self):
        """
        stop all plugin job processing
        """

        for plugin in self.plugins.values():
            plugin.stop()
            
        # stop the worker thread
        self.job_queue.put(None)
        self.worker_thread.join()
        
    def list_all_plugins(self):
        """
        list all plugins register in the input manager

        Returns:
            list: all register plugins
        """
        result = []
        
        for plugin in self.plugins:
            result.append(str(plugin))
            
            self.logger.info(f"list_all_plugins();input plugin {plugin}")
            
        return {'input': result}
