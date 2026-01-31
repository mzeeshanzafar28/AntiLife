import subprocess
import shutil
import os
import sys

def check_tool(tool_name):
    """Check if a system tool exists."""
    return shutil.which(tool_name) is not None

def get_wireless_interfaces():
    """
    Get wireless interfaces.
    Linux: iwconfig or ip link
    Windows: netsh wlan show interfaces
    """
    interfaces = []
    if sys.platform == "linux":
        try:
            # Simple parsing of /proc/net/wireless or iwconfig
            # This is a basic implementation
            with open('/proc/net/wireless', 'r') as f:
                lines = f.readlines()
                for line in lines[2:]:
                    iface = line.split(':')[0].strip()
                    interfaces.append(iface)
        except FileNotFoundError:
            pass
    elif sys.platform == "win32":
        # Windows parsing
        try:
            output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
            for line in output.split('\n'):
                if "Name" in line:
                    interfaces.append(line.split(':')[1].strip())
        except:
            pass
            
    return interfaces or ["wlan0", "wlan1mon"] # Fallback/Demo

def enable_monitor_mode(interface):
    """Enable monitor mode on interface (Linux only helper)"""
    if sys.platform != "linux":
        return "Monitor mode requires Linux"
        
    try:
        subprocess.run(["airmon-ng", "start", interface], check=True)
        return f"Started monitor mode on {interface}"
    except Exception as e:
        return str(e)

def disable_monitor_mode(interface):
    if sys.platform != "linux":
        return
    try:
        subprocess.run(["airmon-ng", "stop", interface], check=True)
    except:
        pass
