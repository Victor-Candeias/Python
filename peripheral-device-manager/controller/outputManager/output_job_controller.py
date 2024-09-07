import importlib
import logging
import os
import uuid
import threading
import time
from queue import Queue
from controller.utilities import Utilities

class OutputJobController:
    def __init__(self):
        """
        intitialize all variables and the plugins
        """
        self.jobs = {}  # save all jobs with theis status
        self.logger = logging.getLogger(__name__)
        self.job_queue = Queue()  # queue for jobs in for processing

        # plugins directory
        self.pluginsDirectory = os.path.join(os.path.dirname(__file__), 'plugins')

        # Registrar todos os plugins
        self.plugins = Utilities.registerPlugins(self.pluginsDirectory, self.logger, "outputManager")

        self.logger.info(f"_register_all_plugins();output plugin count {len(self.plugins)}")

        # Thread for processing queue of jobs
        self.worker_thread = threading.Thread(target=self._process_queue)
        self.worker_thread.daemon = True  # allows finish this thread whem main programn finish
        self.worker_thread.start()

    def add_job(self, data):
        """
        Add new job for processing

        Args:
            data (object): data for processing the job

        Returns:
            object: return the job data updated with tha status
        """
        self.logger.info(f"add_job();data {data}")
        self.logger.info(f"add_job();Job type {data['type_of_job']}")

        # set job id
        job_id = str(uuid.uuid4())
        job = {**data, "message": "queued", "job_id": job_id}

        self.logger.info(f"add_job();Job {job}")

        # Add to the job list
        self.jobs[job_id] = job

        # add to the queue
        self.job_queue.put(job) 

        if job["job_mode"] == "synchronous":
            # for sincronos jobs, process and wait for finish returning the result
            result = self._process_job(job)
            return result
        else:
            # for assincronous jobs, return that the job was accpted and start processing in background
            return {"message": "Job accepted", "job_id": job_id, "status": "200"}

    def _process_queue(self):
        """
        Start process the job queue. This is only for assincronos jobs
        """
        while True:
            job = self.job_queue.get()
            if job is None:
                break
            self._process_job(job)
            self.job_queue.task_done()

    def _process_job(self, job):
        """
        Process the job

        Args:
            job (object): job data to prcoess

        Returns:
            Object: Return the job processed with status information 
        """

        # get the plugin for this job job type
        plugin = self.plugins.get(job["type_of_job"])

        # get the job id
        job_id = job["job_id"]

        # if the plugin exist start processing
        if plugin:
            job["message"] = "Processing"

            self.logger.info(f"Processing job {job['job_id']} with plugin {plugin.get_type()}")

            if job["job_mode"] == "synchronous":
                # Sincronous processing
                result = plugin.process(job)

                self.jobs[job_id]["status"] = result

                self.jobs[job_id]["message"] = "Completed" if result == "200" else "Error"

                self.logger.info(f"Job {job['job_id']} completed with result: {result}")
            else:
                # Assincronous processing in a separete thread
                threading.Thread(target=self._async_job_handler, args=(job, plugin)).start()
        else:
            self.jobs[job_id]["message"] = "Error"

            self.jobs[job_id]["status"] = "400"

        self.logger.error(f"job type result: {job}")
            
        return self.jobs[job_id]

    def _async_job_handler(self, job, plugin):
        """
        Handler that processes the asynchronous job and calls end_asynchronous_job at the end

        Args:
            job (object): job data to process
            plugin (class instance): Plugin that will process the job
        """
        # Process the job
        result = plugin.process(job)

        # sleep 5 seconds just for test
        time.sleep(5) 

        job_id = job["job_id"]

        self.jobs[job_id]["status"] = result
        
        self.jobs[job_id]["message"] = "Completed" if result == 200 else "Error"

        self.logger.info(f"end_asynchronous_job(); Job {job_id} completed with result: {result}")

        # send to websockect

        
    def delete_job(self, data):
        """
        Delete queue jobs

        Args:
            data (object): data for deleting objects that are only in that status message of queued

        Returns:
            object: Return the information os the job deleting
        """
        job_id = data.get("job_id")

        if job_id in self.jobs:
            job = self.jobs[job_id]
            if job["message"] == "queued":
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
        """
        List the information of all jobs

        Args:
            data (object): Creteria for search jobs information

        Returns:
            object: Return the information of the jabs that were found
        """
        machine_id = data.get("machineid")
        session_id = data.get("sessionid")
        filtered_jobs = {job_id: job for job_id, job in self.jobs.items() if job["machineid"] == machine_id and job["sessionid"] == session_id}
        self.logger.info(f"Listing jobs for machine {machine_id} and session {session_id}")
        return filtered_jobs

    def stop(self):
        """
        Stop all plugin job processing
        """
        for plugin in self.plugins.values():
            plugin.stop()

        # Stop the worker thread
        self.job_queue.put(None)
        self.worker_thread.join()

    def list_all_plugins(self):
        """
        List all plugins alvailable for the output manager

        Returns:
            object: Return the list of all plugins available
        """
        result = []
        
        for plugin in self.plugins:
            result.append(str(plugin))
            
            self.logger.info(f"list_all_plugins();output plugin {plugin}")
            
        return {'output': result}