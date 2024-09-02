import win32serviceutil
import win32service
import win32event
import win32api
import serial
import threading
import time

class SerialPortService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SerialPortService"
    _svc_display_name_ = "Serial Port Service"
    _svc_description_ = "A service that creates virtual serial ports and manages communication with a real serial port."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.run()

    def run(self):
        # Example: Serial port settings
        real_port_name = 'COM1'  # Replace with your real serial port
        virtual_port1_name = 'COM3'  # Replace with your virtual port 1
        virtual_port2_name = 'COM4'  # Replace with your virtual port 2

        real_port = serial.Serial(real_port_name, 9600)
        virtual_port1 = serial.Serial(virtual_port1_name, 9600)
        virtual_port2 = serial.Serial(virtual_port2_name, 9600)

        def real_to_virtual():
            while self.is_running:
                if real_port.in_waiting > 0:
                    data = real_port.read(real_port.in_waiting)
                    virtual_port1.write(data)
                    virtual_port2.write(data)

        def virtual_to_real():
            while self.is_running:
                if virtual_port1.in_waiting > 0:
                    data = virtual_port1.read(virtual_port1.in_waiting)
                    real_port.write(data)
                if virtual_port2.in_waiting > 0:
                    data = virtual_port2.read(virtual_port2.in_waiting)
                    real_port.write(data)

        thread1 = threading.Thread(target=real_to_virtual)
        thread2 = threading.Thread(target=virtual_to_real)

        thread1.start()
        thread2.start()

        while self.is_running:
            time.sleep(1)

        # Clean up
        real_port.close()
        virtual_port1.close()
        virtual_port2.close()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(SerialPortService)
