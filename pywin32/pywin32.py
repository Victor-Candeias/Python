import win32file
import win32con
import threading
import time

class SerialManager:
    def __init__(self, port, baud_rate=9600, byte_size=8, parity=win32file.NOPARITY, stop_bits=win32file.ONESTOPBIT, 
                 read_interval=50, read_multiplier=10, read_constant=100, write_multiplier=10, write_constant=100):
        
        self.port = '\\\\.\\' + port
        self.baud_rate = baud_rate
        self.byte_size = byte_size
        self.parity = parity
        self.stop_bits = stop_bits
        self.handle = None
        self.listening = False
        self.read_thread = None

        # define timeout configurations
        self.read_interval=read_interval
        self.read_multiplier=read_multiplier
        self.read_constant=read_constant
        self.write_multiplier=write_multiplier
        self.write_constant=write_constant
        
    def open_port(self):
        """
        Open the serial port and configure parameters and timeouts.
        """
        try:
            # Open the serial port
            self.handle = win32file.CreateFile(
                self.port,
                win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                0,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_ATTRIBUTE_NORMAL,
                None
            )

            if self.handle == win32file.INVALID_HANDLE_VALUE:
                raise Exception(f"Error opening the serial port {self.port}")

            # Configure serial port parameters
            dcb = win32file.GetCommState(self.handle)
            dcb.BaudRate = self.baud_rate
            dcb.ByteSize = self.byte_size
            dcb.Parity = self.parity
            dcb.StopBits = self.stop_bits

            win32file.SetCommState(self.handle, dcb)

            # Configure read/write timeouts
            self.set_serial_timeouts()

            print(f"Serial port {self.port} open with success.")
        except Exception as e:
            print(f"Error opening serial port {self.port}: {e}")

    def close_port(self):
        """
        Fecha a porta serial.
        """
        if self.handle:
            win32file.CloseHandle(self.handle)
            print("Serial port closed.")
            self.handle = None

    def set_serial_timeouts(self):
        """
        Configure timeouts for reading and writing.
        """
        try:
            timeouts = win32file.COMMTIMEOUTS()
            timeouts.ReadIntervalTimeout = self.read_interval
            timeouts.ReadTotalTimeoutMultiplier = self.read_multiplier
            timeouts.ReadTotalTimeoutConstant = self.read_constant
            timeouts.WriteTotalTimeoutMultiplier = self.write_multiplier
            timeouts.WriteTotalTimeoutConstant = self.write_constant
            
            win32file.SetCommTimeouts(self.handle, timeouts)
            
            print("Configured timeouts.")
            
        except Exception as e:
            print(f"Error when configuring timeouts: {e}")

    def send_data(self, data):
        """
        Sends data via the serial port.
        """
        if self.handle:
            try:
                win32file.WriteFile(self.handle, data.encode())
                print(f"Data sent: {data}")
                
            except Exception as e:
                print(f"Error sending data: {e}")
        else:
            print("The serial port is not open.")

    def receive_data(self, num_bytes=128):
        """
        Receives data from the serial port.
        """
        try:
            if self.handle and self.check_serial_connection():
                err_code, data = win32file.ReadFile(self.handle, num_bytes)
                return data.decode()
            else:
                print("The serial port is not open or has been disconnected.")
                
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

    def check_serial_connection(self):
        """
        Verifies that the serial port is connected and operating correctly.
        """
        errors = win32file.ClearCommError(self.handle)[0]
        if errors != 0:
            print(f"Connection error on the serial port: {errors}")
            return False
        return True

    def start_listening(self):
        """
        Starts asynchronous listening to receive data continuously.
        """
        if not self.listening:
            self.listening = True
            self.read_thread = threading.Thread(target=self.listen_for_data, daemon=True)
            self.read_thread.start()
            print("Listening for new data...")

    def stop_listening(self):
        """For listening to data."""
        self.listening = False
        if self.read_thread:
            self.read_thread.join()

    def listen_for_data(self):
        """
        Continuous loop to listen to data from the serial port.
        """
        while self.listening:
            data = self.receive_data()
            if data:
                print(f"Data received: {data}")
            time.sleep(0.1)  # Wait to avoid excessive CPU usage

# Código de uso deve ser fora da classe:
if __name__ == "__main__":
    # Usage example:
    # Create SerialManager instance for COM9 port
    serial_manager = SerialManager(r'COM10')

    # Open the serial port
    serial_manager.open_port()

    # Start listening for data from the serial port
    serial_manager.start_listening()

    # Send data via serial port
    serial_manager.send_data("Hello from Python!")

    # Pause for a few seconds to allow data to be received
    time.sleep(5)

    # Stop listening and close the door
    serial_manager.stop_listening()
    serial_manager.close_port()

    # import os

    # if os.name == 'nt':    #check if windows 
    # a='\\'
    # else:
    # a='/'

    # source = "C:"+a+"Users"+a+"[username]"+a+"Downloads"+a