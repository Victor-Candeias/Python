import win32file
import win32con
import asyncio
import threading
import time

class WindowsAsyncSerialManager:
    def __init__(self, port, baud_rate=9600, byte_size=8, parity=win32file.NOPARITY, stop_bits=win32file.ONESTOPBIT):
        self.port = f"\\\\.\\{port}"
        self.baud_rate = baud_rate
        self.byte_size = byte_size
        self.parity = parity
        self.stop_bits = stop_bits
        self.handle = None
        self.listening = False
        self.read_thread = None

    def open_port(self):
        """Open the serial port and configure parameters."""
        try:
            self.handle = win32file.CreateFile(
                self.port,
                win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                0, None,
                win32con.OPEN_EXISTING,
                win32con.FILE_ATTRIBUTE_NORMAL,
                None
            )

            if self.handle == win32file.INVALID_HANDLE_VALUE:
                raise Exception(f"Error opening the serial port {self.port}")

            print(f"Serial port {self.port} opened successfully.")
        except Exception as e:
            print(f"Error opening serial port {self.port}: {e}")

    def close_port(self):
        """Close the serial port."""
        if self.handle:
            win32file.CloseHandle(self.handle)
            print("Serial port closed.")
            self.handle = None

    def send_data(self, data):
        """Sends data asynchronously via the serial port."""
        if self.handle:
            try:
                win32file.WriteFile(self.handle, data.encode())
                print(f"Data sent: {data}")
            except Exception as e:
                print(f"Error sending data: {e}")
        else:
            print("The serial port is not open.")

    def receive_data(self, num_bytes=128):
        """Receives data asynchronously from the serial port."""
        try:
            if self.handle:
                _, data = win32file.ReadFile(self.handle, num_bytes)
                return data.decode()
            else:
                print("The serial port is not open.")
                return None
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

    async def start_listening(self, callback, interval=0.1):
        """Listen for incoming data asynchronously."""
        self.listening = True
        while self.listening:
            data = self.receive_data()
            if data:
                await callback(data)  # Call async callback function with received data
            await asyncio.sleep(interval)

    def stop_listening(self):
        """Stop listening for data."""
        self.listening = False
        if self.read_thread:
            self.read_thread.join()

async def handle_received_data(data):
    """Callback function to handle received data."""
    print(f"Received data: {data}")

async def main():
    # Create the AsyncSerialManager instance
    serial_manager = WindowsAsyncSerialManager(port='COM9')
    
    # Open the serial port
    serial_manager.open_port()

    # Start listening for incoming data (asynchronously)
    listen_task = asyncio.create_task(serial_manager.start_listening(handle_received_data))

    # Send some data asynchronously
    await asyncio.sleep(1)  # Simulate delay
    serial_manager.send_data("Hello from asyncio!")

    # Simulate the program running, you can modify as per your needs
    await asyncio.sleep(5)  # Keep the program alive for a while to receive data

    # Stop listening and close the port
    serial_manager.stop_listening()
    serial_manager.close_port()

    # Await the listening task to complete cleanly
    await listen_task

if __name__ == "__main__":
    asyncio.run(main())
