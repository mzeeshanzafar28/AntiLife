import subprocess
import os
import signal
import time
from .wifi_tools import check_tool

class HandshakeCapturer:
    def __init__(self):
        self.process = None

    def start_capture(self, interface, bssid=None, channel=None, output_prefix="capture"):
        """
        Starts airodump-ng to capture handshake.
        If BSSID/Channel provided, targets specific AP.
        Otherwise scans all.
        """
        if not check_tool("airodump-ng"):
            return "Error: airodump-ng not found. Please install aircrack-ng suite."

        cmd = ["airodump-ng", "--write", output_prefix, "--output-format", "pcap,csv"]
        
        if bssid:
            cmd.extend(["--bssid", bssid])
        if channel:
            cmd.extend(["--channel", channel])
            
        cmd.append(interface)
        
        try:
            # We open it in a separate process. 
            # In a real GUI, we might want to capture stdout to show networks, but airodump is interactive.
            # We generally run it and let the user see the CSV updating or just run it in background.
            # For this GUI, we will attempt to run it and expect the user to stop it when they see the handshake.
            self.process = subprocess.Popen(cmd, preexec_fn=os.setsid if hasattr(os, 'setsid') else None)
            return "Capture started. Waiting for handshake..."
        except Exception as e:
            return f"Failed to start: {e}"

    def stop_capture(self):
        if self.process:
            try:
                # Send SIGINT to allow graceful exit and file writing
                if hasattr(os, 'killpg'):
                    os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
                else:
                    self.process.terminate()
                self.process.wait()
                self.process = None
                return "Capture stopped."
            except Exception as e:
                return f"Error stopping: {e}"
        return "No capture running."

    def check_handshake(self, pcap_file):
        """
        Check if pcap file contains a handshake using aircrack-ng check.
        """
        if not check_tool("aircrack-ng"):
            return False
            
        try:
            output = subprocess.check_output(["aircrack-ng", pcap_file], stderr=subprocess.STDOUT).decode()
            if "1 handshake" in output or "WPA (" in output: # Basic check
                return True
        except:
            pass
        return False
