from scapy.all import sniff, wrpcap
import threading
import time

class TrafficSniffer:
    def __init__(self):
        self.running = False
        self.thread = None
        self.packets = []

    def start_sniffing(self, interface, output_file=None, callback=None):
        self.running = True
        self.packets = []
        self.thread = threading.Thread(target=self._sniff_loop, args=(interface, output_file, callback))
        self.thread.start()
        return "Sniffer started..."

    def _sniff_loop(self, interface, output_file, callback):
        def process_pkt(pkt):
            if not self.running: return True # Stop sniffing
            self.packets.append(pkt)
            if callback:
                try:
                    summary = pkt.summary()
                    callback(summary)
                except:
                    pass
            return False

        try:
            # We use a loop to check running state, but sniff() is blocking usually.
            # We use stop_filter to control it or timeout.
            # Using timeout is easier to control loop.
            while self.running:
                sniff(iface=interface, prn=process_pkt, store=0, timeout=1) 
        except Exception as e:
            if callback: callback(f"Error: {e}")

        if output_file and self.packets:
            wrpcap(output_file, self.packets)

    def stop_sniffing(self):
        self.running = False
        if self.thread:
            self.thread.join()
        return f"Sniffing stopped. Captured {len(self.packets)} packets."
