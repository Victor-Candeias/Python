import threading
import serial
import win32serviceutil
import win32service
import win32event
import datetime
import os
import logging
import json
from pathlib import Path

LOG_FILE_DIRECTORY = "C:\logfiles\serialportservice"
BASE_FILE_NAME = 'SerialPortService'


class ServiceUtilities:
    @staticmethod
    def get_file_name():
        """Set up logging configuration."""
        # check if dir exists
        ServiceUtilities.ensure_directory_exists(LOG_FILE_DIRECTORY)
        
        current_date = datetime.datetime.now().strftime("%y%m%d")
        log_filename = f"{current_date}_{BASE_FILE_NAME}.log"

        return "{}{}{}".format(LOG_FILE_DIRECTORY, "\\", log_filename)

    @staticmethod
    def write_log_info(message):
        """Write log info."""
        fileName = ServiceUtilities.get_file_name()
        
        with open(fileName, 'a+') as f:
            f.write("Info;" + message + "\n")
 
    @staticmethod
    def write_log_error(message):
        """Write log error."""
        with open(ServiceUtilities.get_file_name(), 'a+') as f:
            f.write("Error;" + message + "\n")
               
    @staticmethod
    def load_config():
        """Load configuration from a JSON file."""
        config_path = os.path.join(os.path.dirname(__file__), 'config\config.json')
        with open(config_path, 'r') as config_file:
            logging.info(f"Loading configuration from {config_path}.")
            return json.load(config_file)

    @staticmethod
    def ensure_directory_exists(directory_path):
        """Check if a directory exists, and create it if it does not."""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

class SerialPortManager:
    def __init__(self, real_port_name, virtual_port1_name, virtual_port2_name, baud_rate):
        self.real_port_name = real_port_name
        self.virtual_port1_name = virtual_port1_name
        self.virtual_port2_name = virtual_port2_name
        self.baud_rate = baud_rate
        self.is_running = False
        ServiceUtilities.write_log_info("SerialPortManager initialized.")

    def start(self):
        try:
            self.is_running = True
            self.real_port = serial.Serial(self.real_port_name, self.baud_rate)
            self.virtual_port1 = serial.Serial(self.virtual_port1_name, self.baud_rate)
            self.virtual_port2 = serial.Serial(self.virtual_port2_name, self.baud_rate)

            ServiceUtilities.write_log_info(f"Opened serial ports: {self.real_port_name}, {self.virtual_port1_name}, {self.virtual_port2_name} at baud rate {self.baud_rate}.")

            self.thread1 = threading.Thread(target=self.real_to_virtual)
            self.thread2 = threading.Thread(target=self.virtual_to_real)

            self.thread1.start()
            self.thread2.start()
        except Exception as e:
            ServiceUtilities.write_log_error(f"Failed to start SerialPortManager: {e}")
            self.stop()

    def real_to_virtual(self):
        while self.is_running:
            if self.real_port.in_waiting > 0:
                data = self.real_port.read(self.real_port.in_waiting)
                self.virtual_port1.write(data)
                self.virtual_port2.write(data)
                ServiceUtilities.write_log_info(f"Data sent from {self.real_port_name} to {self.virtual_port1_name} and {self.virtual_port2_name}.")

    def virtual_to_real(self):
        while self.is_running:
            if self.virtual_port1.in_waiting > 0:
                data = self.virtual_port1.read(self.virtual_port1.in_waiting)
                self.real_port.write(data)
                ServiceUtilities.write_log_info(f"Data sent from {self.virtual_port1_name} to {self.real_port_name}.")
                
            if self.virtual_port2.in_waiting > 0:
                data = self.virtual_port2.read(self.virtual_port2.in_waiting)
                self.real_port.write(data)
                ServiceUtilities.write_log_info(f"Data sent from {self.virtual_port2_name} to {self.real_port_name}.")

    def stop(self):
        try:
            self.is_running = False
            self.thread1.join()
            self.thread2.join()
            self.real_port.close()
            self.virtual_port1.close()
            self.virtual_port2.close()
            ServiceUtilities.write_log_info("Serial ports closed and threads stopped.")
        except Exception as e:
            ServiceUtilities.write_log_error(f"Failed to stop SerialPortManager: {e}")


class SerialPortService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SerialPortService"
    _svc_display_name_ = "Serial Port Service"
    _svc_description_ = "A service that creates virtual serial ports and manages communication with a real serial port."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        self.config = ServiceUtilities.load_config()
        
        ServiceUtilities.write_log_info("Service initialized.")

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.serial_port_manager.stop()
        self.is_running = False
        ServiceUtilities.write_log_info("Service stopped.")

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        ServiceUtilities.write_log_info("Service started.")
        self.run()

    def run(self):
        for line in self.config:
            real_port_name = line['real_port_name']
            virtual_port1_name = line['virtual_port1_name']
            virtual_port2_name = line['virtual_port2_name']
            baud_rate = line['baud_rate']

            # Log configuration details
            ServiceUtilities.write_log_info(f"Real Port: {real_port_name}, Virtual Ports: {virtual_port1_name}, {virtual_port2_name}, Baud Rate: {baud_rate}")
            
            self.serial_port_manager = SerialPortManager(real_port_name, virtual_port1_name, virtual_port2_name, baud_rate)
            self.serial_port_manager.start()
        
        
        # real_port_name = self.config['real_port_name']
        # virtual_port1_name = self.config['virtual_port1_name']
        # virtual_port2_name = self.config['virtual_port2_name']
        # baud_rate = self.config['baud_rate']

        # Log configuration details
        # ServiceUtilities.write_log_info(f"Real Port: {real_port_name}, Virtual Ports: {virtual_port1_name}, {virtual_port2_name}, Baud Rate: {baud_rate}")

        # self.serial_port_manager = SerialPortManager(real_port_name, virtual_port1_name, virtual_port2_name, baud_rate)
        # self.serial_port_manager.start()

        while self.is_running:
            rc = win32event.WaitForSingleObject(self.hWaitStop, 1000)
            if rc == win32event.WAIT_OBJECT_0:
                break

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(SerialPortService)
