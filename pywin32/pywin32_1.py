import win32file
import win32con
import threading
import time

class SerialManager:
    def __init__(self, port, 
                 baud_rate=9600, 
                 byte_size=7, 
                 parity=win32file.EVENPARITY, 
                 stop_bits=win32file.ONESTOPBIT, 
                 read_interval=50, 
                 read_multiplier=10, 
                 read_constant=100, 
                 write_multiplier=10, 
                 write_constant=100,
                 timeout: float = 1.0, 
                 max_retries: int = 3, 
                 retry_interval: float = 2.0):
        
        self.port = '\\\\.\\' + port
        self.baud_rate = baud_rate
        self.byte_size = byte_size
        self.parity = parity
        self.stop_bits = stop_bits
        self.handle = None
        self.listening = False
        self.read_thread = None
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        
        # Timeout configurations
        self.read_interval = read_interval
        self.read_multiplier = read_multiplier
        self.read_constant = read_constant
        self.write_multiplier = write_multiplier
        self.write_constant = write_constant

    def open_port(self):
        """
        Open the serial port with retry logic.
        """
        attempt = 0
        while attempt < self.max_retries:
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

                print(f"Serial port {self.port} opened successfully.")
                return True  # Success

            except Exception as e:
                print(f"Error opening serial port {self.port}: {e}")
                attempt += 1
                print(f"Retrying {attempt}/{self.max_retries} after {self.retry_interval} seconds...")
                time.sleep(self.retry_interval)
        
        print("Failed to open serial port after several attempts.")
        return False  # Failure

    def close_port(self):
        """
        Close the serial port.
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
            # Get the current timeouts
            timeouts = win32file.GetCommTimeouts(self.handle)

            # Unpack and update with class attributes
            ReadIntervalTimeout = self.read_interval
            ReadTotalTimeoutMultiplier = self.read_multiplier
            ReadTotalTimeoutConstant = self.read_constant
            WriteTotalTimeoutMultiplier = self.write_multiplier
            WriteTotalTimeoutConstant = self.write_constant

            # Pack the updated timeouts into a tuple
            updated_timeouts = (ReadIntervalTimeout, 
                                ReadTotalTimeoutMultiplier, 
                                ReadTotalTimeoutConstant,
                                WriteTotalTimeoutMultiplier, 
                                WriteTotalTimeoutConstant)

            # Set the updated timeouts
            win32file.SetCommTimeouts(self.handle, updated_timeouts)

            print("Configured timeouts successfully.")
            
        except Exception as e:
            print(f"Error configuring timeouts: {e}")

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

    def start_listening(self, callback):
        """
        Starts asynchronous listening to receive data continuously with callback.
        """
        if not self.listening:
            self.listening = True
            self.read_thread = threading.Thread(target=self.listen_for_data, args=(callback,), daemon=True)
            self.read_thread.start()
            print("Listening for new data...")

    def stop_listening(self):
        """Stop listening to data."""
        self.listening = False
        if self.read_thread:
            self.read_thread.join()

    def listen_for_data(self, callback):
        """
        Continuous loop to listen to data from the serial port and execute callback.
        """
        while self.listening:
            data = self.receive_data()
            if data:
                callback(data)  # Call the callback with received data
            time.sleep(0.1)  # Wait to avoid excessive CPU usage

# Example usage with callback
if __name__ == "__main__":
    def data_callback(data):
        print(f"Data received from callback: {data}")

    # Create SerialManager instance for COM9 port
    serial_manager = SerialManager(r'COM9')

    # Open the serial port with retries
    if serial_manager.open_port():
        # Start listening for data and provide a callback function
        serial_manager.start_listening(data_callback)

        # Send data via serial port
        serial_manager.send_data("Hello from Python!")

        # Pause for a few seconds to allow data to be received
        time.sleep(5)

        # Stop listening and close the port
        serial_manager.stop_listening()
        serial_manager.close_port()
