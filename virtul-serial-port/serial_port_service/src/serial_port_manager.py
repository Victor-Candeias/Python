import serial
import threading
from ServiceUtilities import ServiceUtilities

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
