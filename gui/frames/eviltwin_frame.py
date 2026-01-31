import customtkinter as ctk
from modules.evil_twin import EvilTwin
from modules.wifi_tools import get_wireless_interfaces

class EvilTwinFrame(ctk.CTkFrame):
    def __init__(self, master, bg_color, text_color, accent_green, accent_red):
        super().__init__(master, fg_color="transparent")
        self.et = EvilTwin()
        
        self.lbl_title = ctk.CTkLabel(self, text="Evil Twin Attack", font=ctk.CTkFont(size=24, weight="bold"), text_color=accent_red)
        self.lbl_title.pack(pady=20, anchor="w")
        
        self.combo_iface = ctk.CTkComboBox(self, values=get_wireless_interfaces())
        self.combo_iface.pack(pady=5)
        
        self.entry_ssid = ctk.CTkEntry(self, placeholder_text="Fake AP SSID")
        self.entry_ssid.pack(pady=5, fill="x")
        
        self.btn_start = ctk.CTkButton(self, text="START EVIL TWIN", command=self.toggle_et, fg_color=accent_red)
        self.btn_start.pack(pady=20)
        
        self.lbl_status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.lbl_status.pack()

    def toggle_et(self):
        if self.btn_start.cget("text") == "START EVIL TWIN":
            iface = self.combo_iface.get()
            ssid = self.entry_ssid.get()
            if not ssid: 
                self.lbl_status.configure(text="Error: Enter SSID")
                return

            msg = self.et.start_evil_twin(iface, ssid)
            self.lbl_status.configure(text=msg, text_color="green")
            self.btn_start.configure(text="STOP EVIL TWIN", fg_color="gray")
        else:
            msg = self.et.stop_evil_twin()
            self.lbl_status.configure(text=msg, text_color="red")
            self.btn_start.configure(text="START EVIL TWIN", fg_color="red")
