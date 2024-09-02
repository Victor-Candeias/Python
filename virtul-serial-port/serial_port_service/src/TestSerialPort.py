from ServiceUtilities import ServiceUtilities
from serial_port_manager import SerialPortManager  # Ensure this file exists and has the class

ServiceUtilities.write_log_info("linha 1")
ServiceUtilities.write_log_info("linha 2")
ServiceUtilities.write_log_info("linha 3")

# json = ServiceUtilities.load_config()

# for x in json:
#     real_port_name = x['real_port_name']
#     virtual_port1_name = x['virtual_port1_name']
#     virtual_port2_name = x['virtual_port2_name']
#     baud_rate = x['baud_rate']
    
#     serial_port_manager = SerialPortManager(real_port_name, virtual_port1_name, virtual_port2_name, baud_rate)
#     serial_port_manager.start()
        
# x = ""
