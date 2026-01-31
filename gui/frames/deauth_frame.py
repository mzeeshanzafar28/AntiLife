import customtkinter as ctk
from modules.deauth import DeauthAttacker
from modules.wifi_tools import get_wireless_interfaces

class DeauthFrame(ctk.CTkFrame):
    def __init__(self, master, bg_color, text_color, accent_green, accent_red):
        super().__init__(master, fg_color="transparent")
        self.attacker = DeauthAttacker()
        
        self.lbl_title = ctk.CTkLabel(self, text="Deauthentication Attack", font=ctk.CTkFont(size=24, weight="bold"), text_color=accent_red)
        self.lbl_title.pack(pady=20, anchor="w")
        
        self.combo_iface = ctk.CTkComboBox(self, values=get_wireless_interfaces())
        self.combo_iface.pack(pady=5)
        
        self.entry_target = ctk.CTkEntry(self, placeholder_text="Target BSSID")
        self.entry_target.pack(pady=5, fill="x")
        
        self.entry_client = ctk.CTkEntry(self, placeholder_text="Client MAC (Optional - Broadcast default)")
        self.entry_client.pack(pady=5, fill="x")
        
        self.btn_attack = ctk.CTkButton(self, text="LAUNCH ATTACK", command=self.toggle_attack, fg_color=accent_red)
        self.btn_attack.pack(pady=20)
        
        self.lbl_status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.lbl_status.pack()

    def toggle_attack(self):
        if self.btn_attack.cget("text") == "LAUNCH ATTACK":
            iface = self.combo_iface.get()
            target = self.entry_target.get()
            client = self.entry_client.get() or "FF:FF:FF:FF:FF:FF"
            
            if not target:
                self.lbl_status.configure(text="Error: Target BSSID required")
                return

            msg = self.attacker.start_attack(iface, target, client)
            self.lbl_status.configure(text=msg, text_color="green")
            self.btn_attack.configure(text="STOP ATTACK", fg_color="gray")
        else:
            msg = self.attacker.stop_attack()
            self.lbl_status.configure(text=msg, text_color="red")
            self.btn_attack.configure(text="LAUNCH ATTACK", fg_color="red")
