import customtkinter as ctk
from modules.osint import lookup_mac

class OSINTFrame(ctk.CTkFrame):
    def __init__(self, master, bg_color, text_color, accent_green, accent_red):
        super().__init__(master, fg_color="transparent")
        
        self.lbl_title = ctk.CTkLabel(self, text="Client MAC OSINT", font=ctk.CTkFont(size=24, weight="bold"), text_color=accent_green)
        self.lbl_title.pack(pady=20, anchor="w")
        
        self.entry_mac = ctk.CTkEntry(self, placeholder_text="Enter MAC Address")
        self.entry_mac.pack(pady=10, fill="x")
        
        self.btn_lookup = ctk.CTkButton(self, text="LOOKUP", command=self.do_lookup, fg_color=accent_green, text_color="black")
        self.btn_lookup.pack(pady=10)
        
        self.lbl_res = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16))
        self.lbl_res.pack(pady=20)

    def do_lookup(self):
        mac = self.entry_mac.get()
        res = lookup_mac(mac)
        self.lbl_res.configure(text=res)
