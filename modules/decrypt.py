import subprocess
from .wifi_tools import check_tool

def run_decrypt(pcap_file, wordlist, bssid=None):
    """
    Run aircrack-ng to crack the handshake.
    """
    if not check_tool("aircrack-ng"):
        yield "Error: aircrack-ng not found."
        return

    cmd = ["aircrack-ng", "-w", wordlist]
    if bssid:
        cmd.extend(["-b", bssid])
    cmd.append(pcap_file)
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                   universal_newlines=True, bufsize=1)
        
        for line in process.stdout:
            yield line.strip()
            
        process.wait()
    except Exception as e:
        yield f"Error: {e}"
