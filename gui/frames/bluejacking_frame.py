import customtkinter as ctk
from modules.bluetooth_tools import BluetoothAttacker
from tkinter import filedialog
import threading

class BluejackingFrame(ctk.CTkFrame):
    def __init__(self, master, bg_color, text_color, accent_green, accent_red):
        super().__init__(master, fg_color="transparent")
        self.attacker = BluetoothAttacker()
        
        self.lbl_title = ctk.CTkLabel(self, text="Bluejacking", font=ctk.CTkFont(size=24, weight="bold"), text_color="cyan")
        self.lbl_title.pack(pady=20, anchor="w")
        
        # Scan
        self.btn_scan = ctk.CTkButton(self, text="Scan Devices", command=self.scan, fg_color="cyan", text_color="black")
        self.btn_scan.pack(pady=10)
        
        self.combo_dev = ctk.CTkComboBox(self, values=["Scan first..."], width=300)
        self.combo_dev.pack(pady=5)
        
        # Message
        self.entry_file = ctk.CTkEntry(self, placeholder_text="Message File (Optional)")
        self.entry_file.pack(pady=5, fill="x")
        self.btn_file = ctk.CTkButton(self, text="Select File", command=self.sel_file, width=100)
        self.btn_file.pack(pady=5)
        
        self.btn_attack = ctk.CTkButton(self, text="SEND MESSAGE", command=self.attack, fg_color="cyan", text_color="black")
        self.btn_attack.pack(pady=20)
        
        self.lbl_status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.lbl_status.pack()

    def scan(self):
        self.lbl_status.configure(text="Scanning...")
        devs = self.attacker.scan_devices()
        if devs:
            self.combo_dev.configure(values=devs)
            self.combo_dev.set(devs[0])
            self.lbl_status.configure(text=f"Found {len(devs)} devices")
        else:
            self.lbl_status.configure(text="No devices found")

    def sel_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, filename)

    def attack(self):
        target = self.combo_dev.get()
        if not target or "Scan" in target:
            self.lbl_status.configure(text="Error: Select Target")
            return
            
        addr = target.split(" - ")[0]
        msg = self.attacker.start_bluejacking(addr, self.entry_file.get())
        self.lbl_status.configure(text=msg)
