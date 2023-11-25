# NOT WORKING. NO IDEA WHAT THIS IS.
import socket

# Have to open powershell, then cd into this repo and run
#   <name of venv>\Scripts\activate
#   python my-venv\Scripts\pip.exe install scapy
# If not, it will error: Import "scapy.all" could not be resolved
from scapy.all import *
from scapy.layers.l2 import Ether

# Because no socket.AF_PACKET for Windows, trying https://stackoverflow.com/questions/39924563/python-raw-socket-to-ethernet-interface-windows/53681616#53681616 
IFACES.show()
iface = IFACES.dev_from_index(1)
print('*********Example iface:******** '); print(iface)
# or <<IFACES.dev_from_pcapname(r"\\Device_stuff")>>
socket = conf.L2socket(iface=iface)

# # Errors: socket.AF_PACKET in the first argument is not a known member of the module
# sniffer_socket = socket.socket(????, socket.SOCK_RAW, socket.ntohs(3))

# interface = "eth0"
# sniffer_socket.bind((interface, 0))

# try:
#     while True:
#         raw_data, addr = sniffer_socket.recvfrom(65535)
#         packet = Ether(raw_data)
#         print(packet.summary())

# except KeyboardInterrupt:
#     sniffer_socket.close()
