# controller/outputManager/output_job_controller.py
import importlib
import logging
import os
import uuid
import threading
import time
import json
from queue import Queue
from flask import request
from messages import Messages

class OutputJobController:
    def __init__(self):
        """
        initialize all variables and the plugins
        """
        self.logger = logging.getLogger(__name__,)
        self.jobs = {}  # save all jobs with the status
        self.job_queue = Queue()  # queue for jobs in for processing

        # plugins directory
        self.pluginsDirectory = os.path.join(os.path.dirname(__file__), 'plugins')

        from controller.utilities import Utilities
        
        # Register all plugins
        self.plugins = Utilities.registerPlugins(self.pluginsDirectory, self.logger, "outputManager")

        self.logger.info(f"output_job_controller.py;__init__(); self.plugins register count={len(self.plugins)}")

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
        self.logger.info(f"output_job_controller.py;add_job();data={data}")
        self.logger.info(f"output_job_controller.py;add_job();serverUrl={serverUrl}")
        
        self.serverUrl = serverUrl
        
        # set job id
        jobId = str(uuid.uuid4())
        job = {**data, "message": "queued", "jobId": jobId}

        self.logger.info(f"output_job_controller.py;add_job();Job={job}")

        # Add to the job list
        self.jobs[jobId] = job

        # add to the queue
        self.job_queue.put(job) 

        if job["jobMode"] == "asynchronous":          
            # for asynchronous jobs, return that the job was accepted and start processing in background
            return {"message": "Job accepted", "jobId": jobId, "status": "200"}
        else:
            # for synchronous jobs, process and wait for finish returning the result
            result = self._process_job(job)
            return result

    # --------------------------------------------------------------------------------------------------
    def _process_queue(self):
        """
        Start process the job queue. This is only for assincronos jobs
        """
        while True:          
            job = self.job_queue.get()
            if job is None:
                break
            
            if job["jobMode"] == "asynchronous":
                self._send_async_job_result_to_websocket(self._process_job(job))
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

        result = ""
        
        # if the plugin exist start processing
        if plugin:
            job["message"] = "Processing"

            self.logger.info(f"output_job_controller.py;_process_job();jobId={job['jobId']};plugin={plugin.get_type()}")

            # Synchronous processing
            plugin.start()
            result = json.loads(plugin.process(job))
            plugin.stop()

            result["job"]["message"] = "Completed"

            self.logger.info(f"output_job_controller.py;_process_job();jobId={job['jobId']};completed with result={result}")
                
            if job["jobMode"] == "asynchronous":
                # for testing
                time.sleep(3)
                # Asynchronous processing in a separate thread
                # threading.Thread(target=self._async_job_handler, args=(job, plugin)).start()
            else:
                self.job_queue.task_done()

        else:
            self.jobs[jobId]["message"] = "Error"

            self.jobs[jobId]["status"] = "400"

            self.logger.error(f"output_job_controller.py;_process_job();job result={job}")
            
            result = self.jobs[jobId]

        return result
    
    # --------------------------------------------------------------------------------------------------
    def _send_async_job_result_to_websocket(self, job):
        """
        Handler that processes the asynchronous job and calls end_asynchronous_job at the end

        Args:
            job (str:json): job data to process
        """
        self.logger.info(f"output_job_controller.py;end_asynchronous_job();jobInfo={job}")

        # send to websocket
        from controller.utilities import Utilities
        
        resultStatus = Messages._instance.STATUS_RESULT_OK
        
        try:
            Utilities.sendDataToClients(self.serverUrl, sessionId=job["job"]["sessionId"], inputType=job["job"]["typeOfJob"], message=job)
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
                self.logger.info(f"output_job_controller.py;delete_job();Job {jobId} deleted")
                return "Job cancelled"
            else:
                self.logger.warning(f"output_job_controller.py;delete_job();Job {jobId} already started or completed")
                return "Job already started or completed"
        else:
            self.logger.error(f"output_job_controller.py;delete_job();Job {jobId} not found")

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
        
        self.logger.info(f"output_job_controller.py;list_jobs();Listing jobs for machine {machineId} and session {sessionId}")
        
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
            
            self.logger.info(f"output_job_controller.py;list_all_plugins();output plugin {plugin}")
            
        return {'output': result}