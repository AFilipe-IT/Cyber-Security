import socket
import pickle
import json

import os
import platform
import subprocess
from scapy.all import sendp, Ether, IP, UDP

# Define the network interface to send the packet on
interface = "enp0s3"  # Replace with your target interface (e.g., wlan0, eth0)

# Create a packet (Ethernet frame with IP and UDP layers)
packet = Ether() / IP(dst="10.0.2.15") / UDP(dport=9999) / "Payload"

# Send the packet to the specified interface
sendp(packet, iface=interface, verbose=True)