import importlib
import logging
import os
import uuid
import threading
import time
from queue import Queue
from flask import request
from messages import Messages

class OutputJobController:
    def __init__(self):
        """
        initialize all variables and the plugins
        """
        self.jobs = {}  # save all jobs with theis status
        self.logger = logging.getLogger(__name__,)
        self.job_queue = Queue()  # queue for jobs in for processing

        # plugins directory
        self.pluginsDirectory = os.path.join(os.path.dirname(__file__), 'plugins')

        from controller.utilities import Utilities
        
        # Register all plugins
        self.plugins = Utilities.registerPlugins(self.pluginsDirectory, self.logger, "outputManager")

        self.logger.info(f"_register_all_plugins();output plugin count {len(self.plugins)}")

        # Thread for processing queue of jobs
        self.worker_thread = threading.Thread(target=self._process_queue)
        self.worker_thread.daemon = True  # allows finish this thread when main program finish
        self.worker_thread.start()

    # --------------------------------------------------------------------------------------------------
    def add_job(self, data, serverUrl):
        """
        Add new job for processing

        Args:
            data (str:json): data for processing the job

        Returns:
            class: return the job data updated with tha status
        """
        self.serverUrl = serverUrl
        self.logger.info(f"add_job();data {data}")
        self.logger.info(f"add_job();Job type {data['typeOfJob']}")

        # set job id
        jobId = str(uuid.uuid4())
        job = {**data, "message": "queued", "jobId": jobId}

        self.logger.info(f"add_job();Job {job}")

        # Add to the job list
        self.jobs[jobId] = job

        # add to the queue
        self.job_queue.put(job) 

        if job["jobMode"] == "synchronous":
            # for synchronous jobs, process and wait for finish returning the result
            result = self._process_job(job)
            return result
        else:
            # for asynchronous jobs, return that the job was accepted and start processing in background
            return {"message": "Job accepted", "jobId": jobId, "status": "200"}

    # --------------------------------------------------------------------------------------------------
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

    # --------------------------------------------------------------------------------------------------
    def _process_job(self, job):
        """
        Process the job

        Args:
            job (str:json): job data to process

        Returns:
            class: Return the job processed with status information 
        """
        # get the plugin for this job job type
        plugin = self.plugins.get(job["typeOfJob"])

        # get the job id
        jobId = job["jobId"]

        # if the plugin exist start processing
        if plugin:
            job["message"] = "Processing"

            self.logger.info(f"Processing job {job['jobId']} with plugin {plugin.get_type()}")

            if job["jobMode"] == "synchronous":
                # Synchronous processing
                result = plugin.process(job)

                self.jobs[jobId]["status"] = result

                self.jobs[jobId]["message"] = "Completed" if result == "200" else "Error"

                self.logger.info(f"Job {job['jobId']} completed with result: {result}")
            else:
                # Asynchronous processing in a separate thread
                threading.Thread(target=self._async_job_handler, args=(job, plugin)).start()
        else:
            self.jobs[jobId]["message"] = "Error"

            self.jobs[jobId]["status"] = "400"

        self.logger.error(f"job type result: {job}")
            
        return self.jobs[jobId]

    # --------------------------------------------------------------------------------------------------
    def _async_job_handler(self, job, plugin):
        """
        Handler that processes the asynchronous job and calls end_asynchronous_job at the end

        Args:
            job (str:json): job data to process
            plugin (class): Plugin that will process the job
        """
        # Process the job
        result = plugin.process(job)

        jobId = job["jobId"]

        self.jobs[jobId]["status"] = result
        
        self.jobs[jobId]["message"] = "Completed" if result == 200 else "Error"

        self.logger.info(f"end_asynchronous_job(); Job {jobId} completed with result: {result}")

        # send to websocket
        from controller.utilities import Utilities
        
        resultStatus = Messages._instance.STATUS_RESULT_OK
        
        try:
            Utilities.sendDataToClients(self.serverUrl, sessionId=self.jobs[jobId]["sessionId"], inputType=self.jobs[jobId]["typeOfJob"], message=self.jobs[jobId])
        except:
            resultStatus = Messages._instance.STATUS_RESULT_ERROR

    # --------------------------------------------------------------------------------------------------    
    def delete_job(self, data):
        """
        Delete queue jobs

        Args:
            data (str:json): data for deleting objects that are only in that status message of queued

        Returns:
            class: Return the information os the job deleting
        """
        jobId = data.get("jobId")

        if jobId in self.jobs:
            job = self.jobs[jobId]
            if job["message"] == "queued" or job["message"] == "Error":
                del self.jobs[jobId]
                self.logger.info(f"Job {jobId} deleted")
                return "Job cancelled"
            else:
                self.logger.warning(f"Job {jobId} already started or completed")
                return "Job already started or completed"
        else:
            self.logger.error(f"Job {jobId} not found")

            return "Job not found"

    # --------------------------------------------------------------------------------------------------
    def list_jobs(self, data):
        """
        List the information of all jobs

        Args:
            data (str:json): Criteria for search jobs information

        Returns:
            class: Return the information of the jabs that were found
        """
        machineId = data.get("machineId")
        sessionId = data.get("sessionId")
        filtered_jobs = {jobId: job for jobId, job in self.jobs.items() if job["machineId"] == machineId and job["sessionId"] == sessionId}
        
        self.logger.info(f"Listing jobs for machine {machineId} and session {sessionId}")
        
        return filtered_jobs

    # --------------------------------------------------------------------------------------------------
    def stop(self):
        """
        Stop all plugin job processing
        """
        for plugin in self.plugins.values():
            plugin.stop()

        # Stop the worker thread
        self.job_queue.put(None)
        self.worker_thread.join()

    # --------------------------------------------------------------------------------------------------
    def list_all_plugins(self):
        """
        List all plugins available for the output manager

        Returns:
            list: Return the list of all plugins available
        """
        result = []
        
        for plugin in self.plugins:
            result.append(str(plugin))
            
            self.logger.info(f"list_all_plugins();output plugin {plugin}")
            
        return {'output': result}