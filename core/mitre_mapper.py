def map_to_mitre(label):
    """
    Maps generic Intrusion Detection labels to specific MITRE ATT&CK TTPs.
    """
    label_upper = str(label).upper()
    
    mapping = {
        "PORTSCAN": "T1046 (Network Service Discovery)",
        "DDOS": "T1498 (Network Denial of Service)",
        "DOS HULK": "T1498 (Network Denial of Service)",
        "BOT": "T1090 (Proxy) / Botnet Activity",
        "BOTNET": "T1090 (Proxy) / Botnet Activity",
        "FTP-PATATOR": "T1110 (Brute Force)",
        "SSH-PATATOR": "T1110 (Brute Force)",
        "WEB ATTACK": "T1190 (Exploit Public-Facing Application)",
        "INFILTRATION": "T1133 (External Remote Services)",
        "HEARTBLEED": "T1190 (Exploit Public-Facing Application)",
        "BRUTE FORCE": "T1110 (Brute Force)",
        "ZERO-DAY": "T1190 (Exploit Public-Facing Application)",
        "LATERAL MOVEMENT": "TA0008 (Lateral Movement)",
        "ANOMALOUS_TRAFFIC": "T1562.004 (Impair Defenses: Disable or Modify System Firewall)"
    }
    
    for key, mitre_id in mapping.items():
        if key in label_upper:
            return mitre_id
            
    return "T1071 (Application Layer Protocol) - Generic Indicator"
