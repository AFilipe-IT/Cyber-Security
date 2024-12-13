import socket
import json
import numpy as np
import requests
import subprocess
import pyshark


# Specify the interface and capture filter
INTERFACE = 'enp0s3'  # Replace with your network interface (e.g., 'wlan0', 'lo', etc.)
UDP_PORT = 9999     # Port to capture UDP packets on


# Capture packets on the specified interface and port
capture = pyshark.LiveCapture(interface=INTERFACE, display_filter=f'udp.port == {UDP_PORT}')

print("Waiting for data...")
for packet in capture.sniff_continuously():
    if hasattr(packet, 'udp'):
        try:
            # Receive data
            data=bytes.fromhex(packet.udp.payload.replace(':', ''))

            # Decode the JSON payload
            data_list = json.loads(data.decode('utf-8'))
            print(f"Received data from {packet.ip.src}")
            
            # Convert list back to numpy array
            received_array = np.array(data_list)
            

            json_data = data_list  
            url = "http://127.0.0.1:9000/predict"
            response = requests.post(url, json=json_data)
            print(f"Predicted {response.text}")
            if response.text == "1":
                try:
                    # Check if the IP is already blocked
                    check_command = f"sudo iptables -L INPUT -v -n | grep {packet.ip.src}"
                    result = subprocess.run(
                        check_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )

                    if result.returncode == 0:
                        print(f"IP {packet.ip.src} is already blocked.")
                    else:
                        # Block the IP if not already blocked
                        command = f"sudo iptables -A INPUT -s {packet.ip.src} -j DROP"
                        subprocess.run(command, shell=True, check=True)
                        print(f"IP {packet.ip.src} has been blocked.")
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred while blocking IP {packet.ip.src}: {e}")
            print("\n")
        except Exception as e:
            print(f"Error processing packet: {e}")
