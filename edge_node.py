import os
import time
import json
import requests
import argparse

def start_edge_node(target_url, api_key):
    """
    Mock Distributed Edge Node
    In a real deployment, this would utilize scapy/libpcap directly on the edge router,
    run the TensorFlow models locally via TFLite, and send just the telemetry.
    """
    print(f"[*] Starting AdvancedIDS Edge Node...")
    print(f"[*] Uplink Target: {target_url}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        while True:
            # Simulate analyzing edge traffic and finding an anomaly
            time.sleep(15)
            
            payload = {
                "flows": [
                    {
                        "flow_id": f"EDGE-NODE-{int(time.time())}",
                        "source_ip": "185.15.22.1",
                        "label": "BOTNET",
                        "confidence": 0.985
                    }
                ]
            }
            
            print("[+] Malicious flow identified at Edge. Syncing to Cloud Command Center...")
            response = requests.post(f"{target_url}/api/edge/ingest", headers=headers, json=payload, timeout=5)
            
            if response.status_code == 200:
                print(f"[+] Uplink Successful: {response.json().get('status')}")
            else:
                print(f"[-] Uplink Failed: {response.status_code} - {response.text}")
                
    except KeyboardInterrupt:
        print("\n[*] Halting Edge Node.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AdvancedIDS Edge Sniffer Node")
    parser.add_argument("--hub", default="http://127.0.0.1:5001", help="URL of the Central Command Center")
    parser.add_argument("--key", default="dev_edge_key", help="Edge API Authentication Key")
    
    args = parser.parse_args()
    start_edge_node(args.hub, args.key)
