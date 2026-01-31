import customtkinter as ctk
from modules.traffic import TrafficSniffer
import threading

class TrafficFrame(ctk.CTkFrame):
    def __init__(self, master, bg_color, text_color, accent_green, accent_red):
        super().__init__(master, fg_color="transparent")
        self.sniffer = TrafficSniffer()
        
        self.lbl_title = ctk.CTkLabel(self, text="Traffic Intercept", font=ctk.CTkFont(size=24, weight="bold"), text_color=accent_green)
        self.lbl_title.pack(pady=20, anchor="w")
        
        self.entry_iface = ctk.CTkEntry(self, placeholder_text="Interface (e.g., eth0, wlan0)")
        self.entry_iface.pack(fill="x", pady=5)
        
        self.entry_file = ctk.CTkEntry(self, placeholder_text="Output File (.pcap)")
        self.entry_file.pack(fill="x", pady=5)
        
        self.btn_sniff = ctk.CTkButton(self, text="START SNIFFING", command=self.toggle_sniff, fg_color=accent_green, text_color="black")
        self.btn_sniff.pack(pady=20)
        
        self.txt_log = ctk.CTkTextbox(self)
        self.txt_log.pack(fill="both", expand=True)

    def toggle_sniff(self):
        if self.btn_sniff.cget("text") == "START SNIFFING":
            iface = self.entry_iface.get()
            out = self.entry_file.get()
            
            if not iface:
                self.txt_log.insert("end", "Error: Interface required\n")
                return
                
            msg = self.sniffer.start_sniffing(iface, out, lambda s: self.txt_log.insert("end", s+"\n"))
            self.txt_log.insert("end", msg + "\n")
            self.btn_sniff.configure(text="STOP SNIFFING", fg_color="red")
        else:
            msg = self.sniffer.stop_sniffing()
            self.txt_log.insert("end", msg + "\n")
            self.btn_sniff.configure(text="START SNIFFING", fg_color="green")
