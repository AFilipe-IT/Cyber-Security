import pyshark
import numpy as np
import pandas as pd
import requests
import json
import subprocess

def calcular_metricas(packets):
    """
    Função que calcula as métricas a partir dos pacotes capturados.
    """
    flow_duration = 0
    fwd_packets = []
    bwd_packets = []
    fwd_packet_lengths = []
    bwd_packet_lengths = []
    fwd_iat_times = []
    bwd_iat_times = []
    packet_lengths = []

    fin_flag_count = 0
    syn_flag_count = 0
    rst_flag_count = 0
    psh_flag_count = 0
    ack_flag_count = 0
    urg_flag_count = 0
    cwe_flag_count = 0
    ece_flag_count = 0

    first_packet_time = None
    last_packet_time = None
    last_fwd_time = None
    last_bwd_time = None

    # Inicialização para variáveis adicionais
    total_fwd_bytes = 0
    total_bwd_bytes = 0
    fwd_header_length = 0
    bwd_header_length = 0
    subflow_fwd_packets = 0
    subflow_bwd_packets = 0

    def get_flag_value(flag):
        return 1 if flag == '1' or flag.lower() == 'true' else 0

    for pkt in packets:
        try:
            current_time = float(pkt.sniff_timestamp)
            if first_packet_time is None:
                first_packet_time = current_time
            last_packet_time = current_time

            length = int(pkt.length)
            packet_lengths.append(length)
            source_ip = packet.ip.src

            # Verificar porta de destino em TCP ou UDP
            destination_port = 0
            if hasattr(pkt, 'ip'):
                if hasattr(pkt.ip, 'dstport'):
                    destination_port = int(pkt.ip.dstport)

            if hasattr(pkt, 'tcp'):
                # Flags TCP
                fin_flag_count += get_flag_value(pkt.tcp.flags_fin)
                syn_flag_count += get_flag_value(pkt.tcp.flags_syn)
                rst_flag_count += get_flag_value(pkt.tcp.flags_reset)
                psh_flag_count += get_flag_value(pkt.tcp.flags_push)
                ack_flag_count += get_flag_value(pkt.tcp.flags_ack)
                urg_flag_count += get_flag_value(pkt.tcp.flags_urg)
                cwe_flag_count += get_flag_value(pkt.tcp.flags_cwe)
                ece_flag_count += get_flag_value(pkt.tcp.flags_ece)

                # Cabeçalho TCP
                fwd_header_length += int(pkt.tcp.len) if hasattr(pkt.tcp, 'len') else 0
                bwd_header_length += int(pkt.tcp.len) if hasattr(pkt.tcp, 'len') else 0

            if pkt.ip.src < pkt.ip.dst:
                fwd_packets.append(pkt)
                fwd_packet_lengths.append(length)
                total_fwd_bytes += length
                if last_fwd_time is not None:
                    fwd_iat_times.append(current_time - last_fwd_time)
                last_fwd_time = current_time
            else:
                bwd_packets.append(pkt)
                bwd_packet_lengths.append(length)
                total_bwd_bytes += length
                if last_bwd_time is not None:
                    bwd_iat_times.append(current_time - last_bwd_time)
                last_bwd_time = current_time

        except AttributeError:
            continue

    flow_duration = last_packet_time - first_packet_time if first_packet_time and last_packet_time else 0

    # Calculando Down/Up Ratio
    down_up_ratio = total_bwd_bytes / total_fwd_bytes if total_fwd_bytes > 0 else 0

    return {
        'Bwd Packet Length Std': [np.std(bwd_packet_lengths) if bwd_packet_lengths else 0],
        'Packet Length Variance': [0], 
        'Packet Length Std': [0],
        'Bwd Packet Length Mean': [np.mean(bwd_packet_lengths) if bwd_packet_lengths else 0],
        'Bwd Packet Length Max': [max(bwd_packet_lengths) if bwd_packet_lengths else 0],
        'Avg Bwd Segment Size': [np.mean(bwd_packet_lengths) if bwd_packet_lengths else 0],
        'Total Length of Fwd Packets': [sum(fwd_packet_lengths)],
        'Subflow Bwd Bytes': [total_bwd_bytes],
        'Max Packet Length': [0],#################
        'Total Length of Bwd Packets': [sum(bwd_packet_lengths)],
        'Average Packet Size': [np.mean(packet_lengths) if packet_lengths else 0],
        'Subflow Fwd Bytes': [total_fwd_bytes],
        'Packet Length Mean': [0],#####################
        'Fwd Packet Length Max': [max(fwd_packet_lengths) if fwd_packet_lengths else 0],
        'Fwd Packet Length Std': [np.std(fwd_packet_lengths) if fwd_packet_lengths else 0],
        'Destination Port': [0],
        'Fwd Packet Length Mean': [np.mean(fwd_packet_lengths) if fwd_packet_lengths else 0],
        'Avg Fwd Segment Size': [np.mean(fwd_packet_lengths) if fwd_packet_lengths else 0],
        'Bwd Header Length': [bwd_header_length],
        'Fwd Header Length': [fwd_header_length],
        'Fwd IAT Std': [np.std(fwd_iat_times) if fwd_iat_times else 0],
        'Fwd IAT Max': [max(fwd_iat_times) if fwd_iat_times else 0],
        'Init_Win_bytes_backward': [0],  ##################### Exemplo
        'Flow IAT Max': [max(fwd_iat_times + bwd_iat_times) if fwd_iat_times + bwd_iat_times else 0],
        'Bwd Packet Length Min': [min(bwd_packet_lengths) if bwd_packet_lengths else 0],
        'Init_Win_bytes_forward': [0],  ################ Exemplo
        'Total Fwd Packets': [len(fwd_packets)],
        'Fwd Header Length.1': [0],
        'Flow IAT Std': [np.std(fwd_iat_times + bwd_iat_times) if fwd_iat_times + bwd_iat_times else 0],
        'PSH Flag Count': [psh_flag_count],
    }


# Exemplo de execução
if __name__ == "__main__":
    while True:
        packets=[]
        capture = pyshark.LiveCapture(interface='enp0s3')
        print("Waiting for data...")
        for packet in capture.sniff_continuously(packet_count=3):
            print("EXTRAINDO PACOTES")
            packets.append(packet)

        data=calcular_metricas(packets)
        
        df = pd.DataFrame(data)
       
        json_data = df.to_json(orient="records")
        url = "http://127.0.0.1:9000/predictRandom"
        response = requests.post(url, json=json_data)
        print(f"Resposta {response.text}")
        if response.text == "1":
            try:
                command = f"sudo iptables -A INPUT -s {packet.ip.src} -j DROP"
                subprocess.run(command, shell=True, check=True)
                print(f"IP {packets[0].ip.src} has been blocked.")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while blocking IP {packets[0].ip.src}: {e}")
            print("\n")
        