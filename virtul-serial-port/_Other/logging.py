import logging

# Setup logging
logging.basicConfig(
    filename='C:\\path_to_log\\serial_port_service.log',  # Change path accordingly
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class SerialPortService(win32serviceutil.ServiceFramework):
    # ... (rest of the code)

    def run(self):
        try:
            logging.info("Service started.")
            # (The rest of your run logic)
            logging.info("Service is running.")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        finally:
            logging.info("Service stopped.")
