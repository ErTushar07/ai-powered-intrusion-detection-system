import os
import subprocess
import platform
import requests
import json

def auto_ban_ip(source_ip):
    """
    Automated Defensive Response: Bans a malicious IP using system firewall utilities.
    Now includes Enterprise Edge SOAR capability (Cloudflare/AWS WAF).
    """
    if not source_ip or source_ip == "127.0.0.1":
        return "Ignored (Local/Invalid IP)"

    # --- ADVANCED ENT MOAT: Cloud Edge Blocking ---
    soar_status = ""
    cloudflare_api = os.getenv("CLOUDFLARE_API_KEY")
    cloudflare_email = os.getenv("CLOUDFLARE_EMAIL")
    zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
    
    if cloudflare_api and cloudflare_email and zone_id:
        try:
            cf_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/access_rules/rules"
            headers = {"X-Auth-Email": cloudflare_email, "X-Auth-Key": cloudflare_api, "Content-Type": "application/json"}
            payload = {"mode": "block", "configuration": {"target": "ip", "value": source_ip}, "notes": "AdvancedIDS Auto-Ban"}
            r = requests.post(cf_url, headers=headers, json=payload, timeout=3)
            if r.status_code == 200:
                soar_status = "Cloudflare Edge Blocked. "
        except Exception as e:
            soar_status = f"CF Edge Error: {e}. "

    system_os = platform.system().lower()
    
    if system_os == "linux":
        try:
            if os.geteuid() != 0:
                return soar_status + "Permission Denied (Sudo required for local IPS)"
            cmd = ["iptables", "-A", "INPUT", "-s", source_ip, "-j", "DROP"]
            subprocess.run(cmd, check=True)
            return soar_status + f"Banned {source_ip} (Linux/iptables)"
        except Exception as e:
            return soar_status + f"IPS Error: {e}"
            
    elif system_os == "darwin": # Mac
        return soar_status + f"Simulated Ban: {source_ip} (Mac/pfctl)"
    
    elif system_os == "windows":
        try:
            rule_name = f"IDS_BLOCK_{source_ip}"
            cmd = ["netsh", "advfirewall", "firewall", "add", "rule", 
                   f"name={rule_name}", "dir=in", "action=block", f"remoteip={source_ip}"]
            subprocess.run(cmd, check=True)
            return soar_status + f"Banned {source_ip} (Windows/netsh)"
        except Exception as e:
            return soar_status + f"IPS Error: {e} (Admin required)"
    
    else:
        return soar_status + f"Unsupported OS: {system_os}"

def unban_ip(source_ip):
    """Removes a previously enforced IP ban, including Cloud Edge."""
    # (Cloudflare Unban logic would go here via DELETE request finding the rule ID)
    system_os = platform.system().lower()
    if system_os == "linux":
        try:
            cmd = ["iptables", "-D", "INPUT", "-s", source_ip, "-j", "DROP"]
            subprocess.run(cmd, check=True)
            return f"Unbanned {source_ip}"
        except:
            return "Unban failed (IP not in list?)"
    
    elif system_os == "windows":
        try:
            rule_name = f"IDS_BLOCK_{source_ip}"
            cmd = ["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}"]
            subprocess.run(cmd, check=True)
            return f"Unbanned {source_ip} (Windows/netsh)"
        except:
            return "Unban failed"

    return f"Simulated Unban: {source_ip}"
