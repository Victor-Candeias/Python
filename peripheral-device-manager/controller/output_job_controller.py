import importlib
import logging
import os
import uuid
import threading
from queue import Queue
from controller.plugin_registry import PluginRegistry
from controller.plugin_base import PluginBase

class OutputJobController:
    def __init__(self):
        self.jobs = {}  # Armazena jobs com seu status
        self.plugins = {}  # Armazena os plugins
        self.logger = logging.getLogger(__name__)
        self.job_queue = Queue()  # Fila de jobs

        # Registrar todos os plugins
        self._register_all_plugins()

        # Thread para processar a fila de jobs
        self.worker_thread = threading.Thread(target=self._process_queue)
        self.worker_thread.daemon = True  # Permite encerrar o thread quando o programa principal termina
        self.worker_thread.start()

    def add_job(self, data):
        self.logger.info(f"add_job();data {data}")
        self.logger.info(f"add_job();Job type {data['type_of_job']}")

        job_id = str(uuid.uuid4())
        job = {**data, "status": "queued", "job_id": job_id}

        self.logger.info(f"add_job();Job {job}")

        self.jobs[job_id] = job
        self.job_queue.put(job)  # Adiciona o job à fila

        if job["job_mode"] == "synchronous":
            # Para jobs síncronos, processa imediatamente e retorna o resultado
            result = self._process_job(job)
            return {"job_id": job_id, "result": result}
        else:
            return {"message": "Job accepted", "job_id": job_id}

    def _process_queue(self):
        while True:
            job = self.job_queue.get()
            if job is None:
                break
            self._process_job(job)
            self.job_queue.task_done()

    def _process_job(self, job):
        plugin = self.plugins.get(job["type_of_job"])
        if plugin:
            job["status"] = "processing"
            self.logger.info(f"Processing job {job['job_id']} with plugin {plugin.get_type()}")

            if job["job_mode"] == "synchronous":
                # Processamento síncrono
                result = plugin.process(job)
                self.jobs[job["job_id"]]["status"] = "completed"
                self.logger.info(f"Job {job['job_id']} completed with result: {result}")
                return result
            else:
                # Processa o job em um thread separado
                threading.Thread(target=self._async_job_handler, args=(job, plugin)).start()
        else:
            job["status"] = "failed"
            self.logger.error(f"No plugin found for job type: {job['type_of_job']}")
            return "failed"

    def _async_job_handler(self, job, plugin):
        """Handler que processa o job assíncrono e chama end_asynchronous_job ao final."""
        result = plugin.process(job)
        self.end_asynchronous_job(job, result)

    def end_asynchronous_job(self, job, result):
        """Chama este método após o término de um job assíncrono."""
        job_id = job["job_id"]
        self.jobs[job_id]["status"] = "completed"
        self.logger.info(f"end_asynchronous_job(); Job {job_id} completed with result: {result}")

    def delete_job(self, data):
        job_id = data.get("job_id")
        if job_id in self.jobs:
            job = self.jobs[job_id]
            if job["status"] == "queued":
                del self.jobs[job_id]
                self.logger.info(f"Job {job_id} deleted")
                return "Job cancelled"
            else:
                self.logger.warning(f"Job {job_id} already started or completed")
                return "Job already started or completed"
        else:
            self.logger.error(f"Job {job_id} not found")
            return "Job not found"

    def list_jobs(self, data):
        machine_id = data.get("machineid")
        session_id = data.get("sessionid")
        filtered_jobs = {job_id: job for job_id, job in self.jobs.items() if job["machineid"] == machine_id and job["sessionid"] == session_id}
        self.logger.info(f"Listing jobs for machine {machine_id} and session {session_id}")
        return filtered_jobs

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
            
            self.logger.info(f"list_all_plugins();output plugin {plugin}")
            
        return {'output': result}
    
    def _register_all_plugins(self):
        """Automatically discover and register all output plugins in the plugins directory."""
        plugins_dir = os.path.join(os.path.dirname(__file__), 'outputPlugins')
        for filename in os.listdir(plugins_dir):
            if filename.endswith('.py') and filename not in ('plugin_base.py', '__init__.py'):
                module_name = f"controller.outputPlugins.{filename[:-3]}"
                self.logger.info(f"_register_all_plugins();module_name {module_name}")
                
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    
                    # Import PluginBase here to avoid circular import at the top
                    from controller.plugin_base import PluginBase
                    
                    if isinstance(attr, type) and issubclass(attr, PluginBase) and attr is not PluginBase:
                        plugin_instance = attr()
                        plugin_type = plugin_instance.get_type()
                        self.plugins[plugin_type] = plugin_instance
                        self.logger.info(f"Registered plugin: {plugin_type}")
                        PluginRegistry.register_plugin(plugin_type, plugin_instance)
