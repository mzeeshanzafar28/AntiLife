import customtkinter as ctk
from modules.jamming import Jammer
from modules.wifi_tools import get_wireless_interfaces

class JammingFrame(ctk.CTkFrame):
    def __init__(self, master, bg_color, text_color, accent_green, accent_red):
        super().__init__(master, fg_color="transparent")
        self.jammer = Jammer()
        
        self.lbl_title = ctk.CTkLabel(self, text="Wireless CCTV/Network Jammer", font=ctk.CTkFont(size=24, weight="bold"), text_color=accent_red)
        self.lbl_title.pack(pady=20, anchor="w")
        
        self.combo_iface = ctk.CTkComboBox(self, values=get_wireless_interfaces())
        self.combo_iface.pack(pady=5)
        
        self.entry_target = ctk.CTkEntry(self, placeholder_text="Target BSSID (Optional - Broadcast)")
        self.entry_target.pack(pady=5, fill="x")
        
        self.btn_jam = ctk.CTkButton(self, text="START JAMMING", command=self.toggle_jam, fg_color=accent_red, hover_color="#550000")
        self.btn_jam.pack(pady=20)
        
        self.lbl_status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.lbl_status.pack()

    def toggle_jam(self):
        if self.btn_jam.cget("text") == "START JAMMING":
            iface = self.combo_iface.get()
            target = self.entry_target.get()
            
            msg = self.jammer.start_jamming(iface, target)
            self.lbl_status.configure(text=msg, text_color="red")
            self.btn_jam.configure(text="STOP JAMMING", fg_color="gray")
        else:
            msg = self.jammer.stop_jamming()
            self.lbl_status.configure(text=msg, text_color="green")
            self.btn_jam.configure(text="START JAMMING", fg_color="red")
