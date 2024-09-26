import json
import logging
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
        self.logger = logging.getLogger(__name__)
        
        pluginDir = os.path.join(os.path.dirname(__file__), f"{self.__class__.plugin_name}.json")
        
        self.logger.info(f"{PluginBase.plugin_name};__init__();pluginDir={pluginDir}")
        
        super().__init__(pluginDir)
        
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