import socket
import pickle
import numpy as np
import pandas as pd
import json
import random
from ping3 import ping
import os
import platform
import subprocess

def check_ping(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    # Ping the IP address using the system's ping command
    try:
        response = subprocess.run(['ping', param, '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode == 0:
            return True
        else:
            print(f"Couldnt connect to {ip}")
            return False
    except Exception as e:
        print(f"Ping failed: {e}")
        return False




# Configure the UDP socket
UDP_IP = "10.0.2.15"  # Receiver's IP address
UDP_PORT = 9999         # Receiver's port
is_connected = check_ping(UDP_IP)
if is_connected:
    path = './malign_traffic_sample.csv'
    _df = pd.read_csv(path)
    df=_df.sample(n=10)

    # Create a socket and send the data
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    for index, row in df.iterrows():
        # Convert dataframe to numpy array
        row_list=row.tolist()
        #data_array = np.array(row.tolist())
        data_array = np.array(row_list)
        # Convert numpy array to a list for JSON serialization
        data_list = data_array.tolist()

        # Serialize the list into a JSON string
        payload = json.dumps(data_list).encode('utf-8')
        

        sock.sendto(payload, (UDP_IP, UDP_PORT))
        print(f"Data has been sent")
    sock.close()