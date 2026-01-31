import customtkinter as ctk
from modules.handshake import HandshakeCapturer
from modules.wifi_tools import get_wireless_interfaces, enable_monitor_mode, disable_monitor_mode
import threading
import time

class HandshakeFrame(ctk.CTkFrame):
    def __init__(self, master, bg_color, text_color, accent_green, accent_red):
        super().__init__(master, fg_color="transparent")
        self.capturer = HandshakeCapturer()
        
        # UI Elements
        self.lbl_title = ctk.CTkLabel(self, text="Capture Handshake", font=ctk.CTkFont(size=24, weight="bold"), text_color=accent_green)
        self.lbl_title.pack(pady=20, anchor="w")
        
        # Interface Selection
        self.frm_controls = ctk.CTkFrame(self, fg_color="transparent")
        self.frm_controls.pack(fill="x", pady=10)
        
        ctk.CTkLabel(self.frm_controls, text="Interface:").pack(side="left", padx=10)
        self.combo_iface = ctk.CTkComboBox(self.frm_controls, values=get_wireless_interfaces())
        self.combo_iface.pack(side="left", padx=10)
        
        self.btn_mon = ctk.CTkButton(self.frm_controls, text="Enable Monitor Mode", command=self.toggle_monitor, fg_color=accent_red)
        self.btn_mon.pack(side="left", padx=10)
        
        # Target Config
        self.frm_target = ctk.CTkFrame(self, fg_color="#262626")
        self.frm_target.pack(fill="x", pady=10)
        
        ctk.CTkLabel(self.frm_target, text="BSSID (Optional):").grid(row=0, column=0, padx=10, pady=10)
        self.entry_bssid = ctk.CTkEntry(self.frm_target, placeholder_text="00:11:22:33:44:55")
        self.entry_bssid.grid(row=0, column=1, padx=10)
        
        ctk.CTkLabel(self.frm_target, text="Channel (Optional):").grid(row=0, column=2, padx=10)
        self.entry_chan = ctk.CTkEntry(self.frm_target, width=60)
        self.entry_chan.grid(row=0, column=3, padx=10)

        # Output Name
        ctk.CTkLabel(self.frm_target, text="Output Prefix:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_out = ctk.CTkEntry(self.frm_target)
        self.entry_out.insert(0, "handshake_capture")
        self.entry_out.grid(row=1, column=1, padx=10)

        # Actions
        self.btn_start = ctk.CTkButton(self, text="START CAPTURE", command=self.start_capture, fg_color=accent_green, text_color="black")
        self.btn_start.pack(pady=20, fill="x")
        
        self.txt_log = ctk.CTkTextbox(self, height=200)
        self.txt_log.pack(fill="both", expand=True)

    def log(self, msg):
        self.txt_log.insert("end", msg + "\n")
        self.txt_log.see("end")

    def toggle_monitor(self):
        iface = self.combo_iface.get()
        msg = enable_monitor_mode(iface)
        self.log(msg)
        # Refresh interfaces
        self.combo_iface.configure(values=get_wireless_interfaces())

    def start_capture(self):
        if self.btn_start.cget("text") == "START CAPTURE":
            iface = self.combo_iface.get()
            bssid = self.entry_bssid.get()
            chan = self.entry_chan.get()
            out = self.entry_out.get()
            
            msg = self.capturer.start_capture(iface, bssid, chan, out)
            self.log(msg)
            if "started" in msg.lower():
                self.btn_start.configure(text="STOP CAPTURE", fg_color="red")
        else:
            msg = self.capturer.stop_capture()
            self.log(msg)
            self.btn_start.configure(text="START CAPTURE", fg_color="green")
