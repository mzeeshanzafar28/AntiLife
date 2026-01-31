import customtkinter as ctk
from modules.ssl_attack import SSLStripper

class SSLFrame(ctk.CTkFrame):
    def __init__(self, master, bg_color, text_color, accent_green, accent_red):
        super().__init__(master, fg_color="transparent")
        self.stripper = SSLStripper()
        
        self.lbl_title = ctk.CTkLabel(self, text="SSL Downgrade (Proxy)", font=ctk.CTkFont(size=24, weight="bold"), text_color=accent_red)
        self.lbl_title.pack(pady=20, anchor="w")
        
        self.entry_port = ctk.CTkEntry(self, placeholder_text="Port (8080)")
        self.entry_port.pack(pady=5)
        self.entry_port.insert(0, "8080")
        
        self.btn_start = ctk.CTkButton(self, text="START PROXY", command=self.toggle_proxy, fg_color=accent_red)
        self.btn_start.pack(pady=20)
        
        self.lbl_status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.lbl_status.pack()

    def toggle_proxy(self):
        if self.btn_start.cget("text") == "START PROXY":
            try:
                port = int(self.entry_port.get())
            except:
                port = 8080
            msg = self.stripper.start_proxy(port)
            self.lbl_status.configure(text=msg, text_color="green")
            self.btn_start.configure(text="STOP PROXY", fg_color="gray")
        else:
            msg = self.stripper.stop_proxy()
            self.lbl_status.configure(text=msg, text_color="red")
            self.btn_start.configure(text="START PROXY", fg_color="red")
