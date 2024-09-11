import json
import os
from tkinter import Image
from controller.plugin_base import PluginBase
import clr

# Set the plugin_name at the base class level
PluginBase.plugin_name = os.path.splitext(os.path.basename(__file__))[0]

class NavePlugin(PluginBase):
    def __init__(self):
        """
        Initialize the Receipt plugin class by calling the base class initializer.
        """
        super().__init__()
        
        # load current configuration
        self.load_configuration()

    def load_configuration(self):
        """
        Load the plugin configuration from a JSON file.
        """
        # Path of the config file based on the plugin name
        self.configFilePath = os.path.join(os.path.dirname(__file__), f"{self.__class__.plugin_name}.json")
        
        if os.path.exists(self.configFilePath):
            with open(self.configFilePath, 'r') as file:
                data = json.load(file)
                self.logger.info(f"Loaded configuration: {data}")

                # initialize the vars
                self.receipt_assembly_qualified_name = data['receipt_assembly_qualified_name']
                self.label_assembly_qualified_name = data['label_assembly_qualified_name']
        else:
            self.logger.error(self.messages.PLUGIN_CONFIG_NOT_FOUND + self.configFilePath)

    def process(self, job):
        """
        Process the given job and handle the serial connection and data transmission.
        """
        self.logger.info(f"Processing {self.plugin_name} Job {job['job_id']}")

        # initialize ok
        status_result = "200"

        jobType = job["typeOfJob"]
        
        if (jobType == ""):
            self.logger.info("label")
            
            self._print_nave_label(job)
        else:
            self.logger.info("receipt")
            
            self._print_nave_receipt(job)
            
        self.process_json(job["printData"])
        
        pass
    
    def _print_nave_label(self, job):
        # Carregue a assembly do GAC pelo seu nome qualificado
        clr.AddReference(self.receipt_assembly_qualified_name)

        # Importe as classes do namespace da assembly
        # from NamespaceDaAssembly import NomeDaClasse

        # Crie uma instância da classe e chame o método desejado
        # objeto = NomeDaClasse()
        # resultado = objeto.MetodoQueDesejaChamar()
    
    def _print_nave_receipt(self, job):
        # Carregue a assembly do GAC pelo seu nome qualificado
        clr.AddReference(self.label_assembly_qualified_name)

        # Importe as classes do namespace da assembly
        # from NamespaceDaAssembly import NomeDaClasse

        # Crie uma instância da classe e chame o método desejado
        # objeto = NomeDaClasse()
        # resultado = objeto.MetodoQueDesejaChamar()
    
# Register the plugin
from controller.plugin_registry import PluginRegistry
PluginRegistry.register_plugin(PluginBase.plugin_name, NavePlugin())